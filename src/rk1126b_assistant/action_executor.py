import subprocess
from dataclasses import dataclass
from typing import Callable

from .actions import ActionPlan


CommandRunner = Callable[[tuple[str, ...]], object]


@dataclass(frozen=True)
class ActionExecutionResult:
    name: str
    command: tuple[str, ...]
    executed: bool
    message: str


class ActionExecutor:
    def __init__(self, runner: CommandRunner | None = None):
        self._runner = runner or self._default_runner

    def execute(self, plan: ActionPlan) -> ActionExecutionResult:
        command_text = " ".join(plan.command)
        if not plan.execute:
            return ActionExecutionResult(
                name=plan.name,
                command=plan.command,
                executed=False,
                message=f"dry-run: {command_text}",
            )

        self._runner(plan.command)
        return ActionExecutionResult(
            name=plan.name,
            command=plan.command,
            executed=True,
            message=f"executed: {command_text}",
        )

    @staticmethod
    def _default_runner(command: tuple[str, ...]) -> object:
        return subprocess.Popen(command)
