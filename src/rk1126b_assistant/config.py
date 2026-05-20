from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AssistantConfig:
    study_url: str = "https://www.icourse163.org/"
    browser_command: str = "browser"
    music_file: Path = Path("demo_media/music/sample.mp3")
    video_file: Path = Path("demo_media/video/sample.mp4")
    dry_run: bool = True
