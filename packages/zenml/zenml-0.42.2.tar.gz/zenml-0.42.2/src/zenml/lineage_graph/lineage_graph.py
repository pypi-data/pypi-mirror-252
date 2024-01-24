#  Copyright (c) ZenML GmbH 2022. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at:
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#  or implied. See the License for the specific language governing
#  permissions and limitations under the License.
"""Class for lineage graph generation."""

from typing import List, Optional, Tuple, Union

from pydantic import BaseModel

from zenml.enums import ExecutionStatus
from zenml.lineage_graph.edge import Edge
from zenml.lineage_graph.node import (
    ArtifactNode,
    ArtifactNodeDetails,
    StepNode,
    StepNodeDetails,
)
from zenml.models import PipelineRunResponseModel, StepRunResponseModel

ARTIFACT_PREFIX = "artifact_"
STEP_PREFIX = "step_"


class LineageGraph(BaseModel):
    """A lineage graph representation of a PipelineRunResponseModel."""

    nodes: List[Union[StepNode, ArtifactNode]] = []
    edges: List[Edge] = []
    root_step_id: Optional[str] = None
    run_metadata: List[Tuple[str, str, str]] = []

    def generate_step_nodes_and_edges(
        self, step: StepRunResponseModel
    ) -> None:
        """Generates the step nodes and the edges between them.

        Args:
            step: The step to generate the nodes and edges for.
        """
        step_id = STEP_PREFIX + str(step.id)
        if self.root_step_id is None:
            self.root_step_id = step_id
        step_config = step.config.dict()
        if step_config:
            step_config = {
                key: value
                for key, value in step_config.items()
                if key not in ["inputs", "outputs", "parameters"] and value
            }
        self.nodes.append(
            StepNode(
                id=step_id,
                data=StepNodeDetails(
                    execution_id=str(step.id),
                    name=step.name,  # redundant for consistency
                    status=step.status,
                    entrypoint_name=step.config.name,  # redundant for consistency
                    parameters=step.config.parameters,
                    configuration=step_config,
                    inputs={k: v.uri for k, v in step.inputs.items()},
                    outputs={k: v.uri for k, v in step.outputs.items()},
                    metadata=[
                        (m.key, str(m.value), str(m.type))
                        for m in step.metadata.values()
                    ],
                ),
            )
        )

        for artifact_name, artifact in step.outputs.items():
            artifact_id = ARTIFACT_PREFIX + str(artifact.id)
            self.nodes.append(
                ArtifactNode(
                    id=artifact_id,
                    data=ArtifactNodeDetails(
                        execution_id=str(artifact.id),
                        name=artifact_name,
                        status=step.status,
                        is_cached=step.status == ExecutionStatus.CACHED,
                        artifact_type=artifact.type,
                        artifact_data_type=artifact.data_type.import_path,
                        parent_step_id=str(step.id),
                        producer_step_id=str(artifact.producer_step_run_id),
                        uri=artifact.uri,
                        metadata=[
                            (m.key, str(m.value), str(m.type))
                            for m in artifact.metadata.values()
                        ],
                    ),
                )
            )
            self.edges.append(
                Edge(
                    id=step_id + "_" + artifact_id,
                    source=step_id,
                    target=artifact_id,
                )
            )

        for artifact_name, artifact in step.inputs.items():
            artifact_id = ARTIFACT_PREFIX + str(artifact.id)
            self.edges.append(
                Edge(
                    id=step_id + "_" + artifact_id,
                    source=artifact_id,
                    target=step_id,
                )
            )

    def generate_run_nodes_and_edges(
        self, run: PipelineRunResponseModel
    ) -> None:
        """Generates the run nodes and the edges between them.

        Args:
            run: The PipelineRunResponseModel to generate the lineage graph for.
        """
        self.run_metadata = [
            (m.key, str(m.value), str(m.type)) for m in run.metadata.values()
        ]
        for step in run.steps.values():
            self.generate_step_nodes_and_edges(step)
