from enum import Enum


class TaskOrderBy(str, Enum):
    DUE_DATE = "due_date"
    PRIORITY = "priority"
