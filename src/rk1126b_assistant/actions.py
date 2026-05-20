from dataclasses import dataclass

from .config import AssistantConfig
from .intent import IntentName


@dataclass(frozen=True)
class ActionPlan:
    name: str
    command: tuple[str, ...]
    execute: bool = False


class ActionRegistry:
    def __init__(self, config: AssistantConfig | None = None):
        self.config = config or AssistantConfig()

    def plan(self, intent_name: IntentName) -> ActionPlan | None:
        if intent_name == IntentName.OPEN_STUDY_SITE:
            return ActionPlan(
                name="open_study_site",
                command=(self.config.browser_command, self.config.study_url),
                execute=not self.config.dry_run,
            )
        if intent_name == IntentName.OPEN_BROWSER:
            return ActionPlan(
                name="open_browser",
                command=(self.config.browser_command,),
                execute=not self.config.dry_run,
            )
        if intent_name == IntentName.PLAY_MUSIC:
            return ActionPlan(
                name="play_music",
                command=("mpv", str(self.config.music_file)),
                execute=not self.config.dry_run,
            )
        if intent_name == IntentName.PLAY_VIDEO:
            return ActionPlan(
                name="play_video",
                command=("mpv", str(self.config.video_file)),
                execute=not self.config.dry_run,
            )
        if intent_name == IntentName.PAUSE_MEDIA:
            return ActionPlan(name="pause_media", command=("playerctl", "play-pause"), execute=not self.config.dry_run)
        return None
