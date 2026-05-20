from dataclasses import dataclass
from enum import Enum


class IntentName(str, Enum):
    OPEN_BROWSER = "open_browser"
    OPEN_STUDY_SITE = "open_study_site"
    PLAY_MUSIC = "play_music"
    PLAY_VIDEO = "play_video"
    PAUSE_MEDIA = "pause_media"
    LIST_OBJECTS = "list_objects"
    FIND_OBJECT = "find_object"
    ENTER_STUDY_MODE = "enter_study_mode"
    ENTER_RELAX_MODE = "enter_relax_mode"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class Intent:
    name: IntentName
    raw_text: str
    target: str | None = None


_OBJECT_ALIASES = {
    "手机": "phone",
    "水杯": "cup",
    "杯子": "cup",
    "书": "book",
    "笔记本": "notebook",
    "鼠标": "mouse",
    "键盘": "keyboard",
}


def parse_intent(text: str) -> Intent:
    normalized = "".join(text.strip().split())
    if not normalized:
        return Intent(IntentName.UNKNOWN, text)

    if "打开学习网页" in normalized or "打开课程网站" in normalized:
        return Intent(IntentName.OPEN_STUDY_SITE, text, "study_site")
    if "打开浏览器" in normalized:
        return Intent(IntentName.OPEN_BROWSER, text, "browser")
    if "播放音乐" in normalized:
        return Intent(IntentName.PLAY_MUSIC, text, "music")
    if "播放视频" in normalized:
        return Intent(IntentName.PLAY_VIDEO, text, "video")
    if "暂停" in normalized:
        return Intent(IntentName.PAUSE_MEDIA, text, "media")
    if "桌上有什么" in normalized or "桌面有什么" in normalized:
        return Intent(IntentName.LIST_OBJECTS, text)
    if "进入学习模式" in normalized or "我准备学习了" in normalized:
        return Intent(IntentName.ENTER_STUDY_MODE, text, "study")
    if "进入休闲模式" in normalized or "进入娱乐模式" in normalized:
        return Intent(IntentName.ENTER_RELAX_MODE, text, "relax")

    if "找" in normalized:
        for alias, target in _OBJECT_ALIASES.items():
            if alias in normalized:
                return Intent(IntentName.FIND_OBJECT, text, target)

    return Intent(IntentName.UNKNOWN, text)
