from dataclasses import dataclass, field

from .action_executor import ActionExecutor
from .controller import AssistantController
from .demo_scenes import load_demo_scene
from .scene import Detection, SceneState


@dataclass(frozen=True)
class DetectionDrawable:
    label: str
    confidence: float
    bbox: tuple[int, int, int, int]


@dataclass(frozen=True)
class CommandLogEntry:
    command: str
    response: str
    action_message: str | None = None


@dataclass
class GuiModel:
    scene_name: str = "empty"
    canvas_width: int = 640
    canvas_height: int = 360
    controller: AssistantController = field(default_factory=AssistantController)
    executor: ActionExecutor = field(default_factory=ActionExecutor)
    logs: list[CommandLogEntry] = field(default_factory=list)

    def scene(self) -> SceneState:
        return load_demo_scene(self.scene_name)

    def set_scene(self, scene_name: str) -> None:
        self.scene_name = scene_name

    def detection_drawables(self) -> list[DetectionDrawable]:
        scene = self.scene()
        return [self._project_detection(scene, detection) for detection in scene.detections]

    def submit_command(self, command: str) -> CommandLogEntry:
        response = self.controller.handle_text(command, self.scene())
        action_message = None
        if response.action:
            action_message = self.executor.execute(response.action).message

        entry = CommandLogEntry(command=command, response=response.message, action_message=action_message)
        self.logs.append(entry)
        return entry

    def _project_detection(self, scene: SceneState, detection: Detection) -> DetectionDrawable:
        scale_x = self.canvas_width / scene.frame_width
        scale_y = self.canvas_height / 360
        x1, y1, x2, y2 = detection.bbox
        return DetectionDrawable(
            label=detection.label,
            confidence=detection.confidence,
            bbox=(
                round(x1 * scale_x),
                round(y1 * scale_y),
                round(x2 * scale_x),
                round(y2 * scale_y),
            ),
        )
