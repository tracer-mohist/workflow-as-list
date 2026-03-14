# src/workflow_as_list/executor/__init__.py
"""Executor module - interprets workflows and manages execution state.

NOTE: Executor is an interpreter, not a direct executor.
It exposes one step at a time to the Agent for progressive exposure.
"""

from .loader import WorkflowLoader
from .parser import WorkflowParser
from .state import Executor

__all__ = ["WorkflowParser", "Executor", "WorkflowLoader"]
