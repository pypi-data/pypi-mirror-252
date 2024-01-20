from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, TypedDict

from forloop_common_structures.core.edge import Edge
from forloop_common_structures.core.node import Node
from forloop_common_structures.core.variable import Variable
from forloop_modules.queries.db_model_templates import JobStatusEnum


@dataclass
class NodeJob:
    pipeline_uid: str  # TODO: Remove when PrototypeJobs are implemented
    node: Node

    uid: Optional[str] = None
    machine_uid: Optional[str] = None  # TODO: Remove when PrototypeJobs are implemented
    status: JobStatusEnum = JobStatusEnum.QUEUED
    created_at: datetime = field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    message: Optional[str] = None
    pipeline_job_uid: Optional[int] = None

    def __post_init__(self):
        # Deserialize dict into a Node if NodeJob is instantiated from a JSON
        if isinstance(self.node, dict):
            self.node = Node(**self.node)

        # Deserialize into Enum if instantiated from JSON
        if isinstance(self.status, str):
            self.status = JobStatusEnum(self.status)

    def __str__(self) -> str:
        """Create string representation of the class used in logging."""
        return f"{type(self).__name__}:{self.uid}"


class PipelineElements(TypedDict):
    nodes: list[Node]
    edges: list[Edge]
    variables: list[Variable]


@dataclass
class PipelineJob:
    pipeline_uid: str
    pipeline_elements: PipelineElements  # TODO: Discuss and remove (?) when PrototypeJobs are implemented - current pipeline on the backend should be used

    uid: Optional[str] = None
    machine_uid: Optional[str] = None
    status: JobStatusEnum = JobStatusEnum.QUEUED
    created_at: datetime = field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    message: Optional[str] = None

    def __post_init__(self) -> None:
        # Deserialize into Enum if instantiated from JSON
        if isinstance(self.status, str):
            self.status = JobStatusEnum(self.status)

        # Deserialize a dict with nodes/edges/variables dicts
        self._deserialize_pipeline_elements()

    # TODO: Discuss and remove (?) when PrototypeJobs are implemented - current pipeline on the backend should be used
    def _deserialize_pipeline_elements(self) -> None:
        """Deserialize nodes, edges, variables into list of objects in case the Job was instantiated from JSON."""
        name_mapping = {"nodes": Node, "edges": Edge, "variables": Variable}
        deserialized_elements: PipelineElements = {"nodes": [], "edges": [], "variables": []}

        for element_type, elements in self.pipeline_elements.items():
            # Iterate over Nodes/Edges/Variables groups if instantiated as dicts
            if elements and isinstance(elements[0], dict):
                object_cls = name_mapping[element_type]
                deserialized_elements[element_type] = [
                    object_cls(**element) for element in elements
                ]

        self.pipeline_elements = deserialized_elements

    def __str__(self) -> str:
        """Create string representation of the class used in logging."""
        return f"{type(self).__name__}:{self.uid}"


@dataclass
class OperationJob:
    prototype_job_uid: int
    node: Node

    uid: Optional[str] = None
    status: JobStatusEnum = JobStatusEnum.QUEUED
    created_at: datetime = field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    message: Optional[str] = None

    def __post_init__(self):
        # Deserialize dict into a Node if NodeJob is instantiated from a JSON
        if isinstance(self.node, dict):
            self.node = Node(**self.node)

        # Deserialize into Enum if instantiated from JSON
        if isinstance(self.status, str):
            self.status = JobStatusEnum(self.status)

    def __str__(self) -> str:
        """Create string representation of the class used in logging."""
        return f"{type(self).__name__}:{self.uid}"


@dataclass
class PrototypeJob:
    pipeline_uid: str
    machine_uid: Optional[str] = None
    uid: Optional[str] = None
    status: JobStatusEnum = JobStatusEnum.QUEUED
    created_at: datetime = field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    def __post_init__(self) -> None:
        # Deserialize into Enum if instantiated from JSON
        if isinstance(self.status, str):
            self.status = JobStatusEnum(self.status)

    def __str__(self) -> str:
        """Create string representation of the class used in logging."""
        return f"{type(self).__name__}:{self.uid}"
