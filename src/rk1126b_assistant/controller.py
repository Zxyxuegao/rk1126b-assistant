from dataclasses import dataclass

from .actions import ActionPlan, ActionRegistry
from .intent import IntentName, parse_intent
from .scene import SceneState


@dataclass(frozen=True)
class AssistantResponse:
    intent: str
    message: str
    action: ActionPlan | None = None


class AssistantController:
    def __init__(self, actions: ActionRegistry | None = None):
        self.actions = actions or ActionRegistry()

    def handle_text(self, text: str, scene: SceneState) -> AssistantResponse:
        intent = parse_intent(text)

        if intent.name == IntentName.LIST_OBJECTS:
            objects = scene.list_objects()
            message = "当前识别到: " + ", ".join(objects) if objects else "当前未识别到工位物品"
            return AssistantResponse(intent=intent.name.value, message=message)

        if intent.name == IntentName.FIND_OBJECT and intent.target:
            result = scene.find(intent.target)
            if result.found:
                return AssistantResponse(
                    intent=intent.name.value,
                    message=f"{result.label} 在画面 {result.region} 区域",
                )
            return AssistantResponse(intent=intent.name.value, message=f"未发现 {intent.target}")

        action = self.actions.plan(intent.name)
        if action:
            return AssistantResponse(intent=intent.name.value, message=f"已规划动作: {action.name}", action=action)

        if intent.name == IntentName.ENTER_STUDY_MODE:
            if scene.has_any({"book", "notebook"}):
                action = self.actions.plan(IntentName.OPEN_STUDY_SITE)
                return AssistantResponse(intent=intent.name.value, message="检测到学习资料，进入学习模式", action=action)
            return AssistantResponse(intent=intent.name.value, message="未检测到书或笔记本，请先放置学习资料")

        return AssistantResponse(intent=IntentName.UNKNOWN.value, message="未识别到可执行指令")
