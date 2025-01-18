from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class UserDTO:
    id: str
    name: str
    default_duration: int

@dataclass
class CommandHistoryDTO:
    id: int
    user_id: str
    command: str

@dataclass
class PriorityLevelDTO:
    id: int
    name: str

@dataclass
class TaskDTO:
    id: int
    user_id: str
    priority_level_id: int
    name: str
    duration: int
    due_date: str
    rhythm: int
    today: bool

@dataclass
class GetTaskDTO:
    id: int
    userId: UserDTO
    priorityLevel: PriorityLevelDTO
    name: str
    duration: int
    dueDate: str
    rhythm: int
    today: bool

@dataclass
class AsapTaskDTO:
    id: int
    user_id: str
    name: str
    deleted: int

@dataclass
class GetAsapTaskDTO:
    id: int
    userId: UserDTO
    name: str
    deleted: int