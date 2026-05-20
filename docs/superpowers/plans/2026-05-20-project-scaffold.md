# Project Scaffold Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first Windows-testable Python scaffold for the RV1126B multimodal assistant while preparing Linux deployment placeholders.

**Architecture:** Keep hardware-dependent code behind small interfaces so Windows tests exercise command parsing, scene state, and action routing without cameras, microphones, or RKNN runtime. Linux/RV1126B files are prepared as documented deployment stubs and do not run hardware code yet.

**Tech Stack:** Python 3.12, standard-library `unittest`, `dataclasses`, `enum`, PowerShell for Windows checks, shell scripts and systemd unit placeholders for Debian/RV1126B.

---

## File Structure

- Create `pyproject.toml`: package metadata and test discovery command notes.
- Create `src/rk1126b_assistant/__init__.py`: package export marker.
- Create `src/rk1126b_assistant/config.py`: typed runtime configuration defaults.
- Create `src/rk1126b_assistant/intent.py`: command text to structured intent parser.
- Create `src/rk1126b_assistant/scene.py`: visual detection data model and scene query helpers.
- Create `src/rk1126b_assistant/actions.py`: safe action registry and dry-run system action planning.
- Create `src/rk1126b_assistant/controller.py`: orchestration between intents, scene state, and actions.
- Create `src/rk1126b_assistant/main.py`: Windows-safe CLI demo entry point.
- Create `tests/test_intent.py`: intent parser behavior tests.
- Create `tests/test_scene.py`: scene query behavior tests.
- Create `tests/test_controller.py`: multimodal controller behavior tests.
- Create `deploy/linux/README.md`: board-side deployment notes.
- Create `deploy/linux/install_debian.sh`: dependency installation placeholder with explicit guarded behavior.
- Create `deploy/linux/rk1126b-assistant.service`: systemd unit placeholder.
- Modify `docs/project-proposal.md`: record implementation scaffold decisions.
- Modify `README.md`: add Windows development and test instructions.

## Task 1: Project Metadata And Test Harness

**Files:**
- Create: `pyproject.toml`
- Create: `src/rk1126b_assistant/__init__.py`
- Create: `tests/__init__.py`
- Modify: `README.md`

- [ ] **Step 1: Write the failing import smoke test**

Create `tests/test_package_import.py`:

```python
import unittest


class PackageImportTests(unittest.TestCase):
    def test_package_exposes_version(self):
        import rk1126b_assistant

        self.assertEqual(rk1126b_assistant.__version__, "0.1.0")


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m unittest tests.test_package_import -v`

Expected: FAIL or ERROR because the `rk1126b_assistant` package is not importable yet.

- [ ] **Step 3: Write minimal package metadata**

Create `pyproject.toml`:

```toml
[project]
name = "rk1126b-assistant"
version = "0.1.0"
description = "Windows-testable scaffold for an RV1126B edge multimodal assistant."
requires-python = ">=3.10"

[tool.unittest]
start-directory = "tests"
```

Create `src/rk1126b_assistant/__init__.py`:

```python
"""RV1126B edge multimodal assistant package."""

__version__ = "0.1.0"
```

Create `tests/__init__.py`:

```python
"""Test package for rk1126b_assistant."""
```

- [ ] **Step 4: Run test to verify it passes with src path**

Run: `$env:PYTHONPATH='src'; python -m unittest tests.test_package_import -v`

Expected: PASS with 1 test.

- [ ] **Step 5: Update README with Windows test command**

Add:

```markdown
## Windows 开发测试

当前第一阶段只依赖 Python 标准库，可在 Windows 上直接运行核心逻辑测试：

```powershell
$env:PYTHONPATH="src"
python -m unittest discover -s tests -v
```
```

- [ ] **Step 6: Commit**

Run:

```powershell
git add pyproject.toml src tests README.md
git commit -m "chore: add python project scaffold"
```

## Task 2: Intent Parser

**Files:**
- Create: `src/rk1126b_assistant/intent.py`
- Create: `tests/test_intent.py`

- [ ] **Step 1: Write failing intent parser tests**

Create `tests/test_intent.py`:

```python
import unittest

from rk1126b_assistant.intent import IntentName, parse_intent


class IntentParserTests(unittest.TestCase):
    def test_parses_open_study_site(self):
        intent = parse_intent("打开学习网页")

        self.assertEqual(intent.name, IntentName.OPEN_STUDY_SITE)
        self.assertEqual(intent.target, "study_site")

    def test_parses_find_phone(self):
        intent = parse_intent("帮我找手机")

        self.assertEqual(intent.name, IntentName.FIND_OBJECT)
        self.assertEqual(intent.target, "phone")

    def test_unknown_command_is_safe(self):
        intent = parse_intent("删除所有文件")

        self.assertEqual(intent.name, IntentName.UNKNOWN)
        self.assertIsNone(intent.target)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `$env:PYTHONPATH='src'; python -m unittest tests.test_intent -v`

Expected: ERROR because `rk1126b_assistant.intent` does not exist.

- [ ] **Step 3: Implement minimal intent parser**

Create `src/rk1126b_assistant/intent.py`:

```python
from dataclasses import dataclass
from enum import StrEnum


class IntentName(StrEnum):
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
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `$env:PYTHONPATH='src'; python -m unittest tests.test_intent -v`

Expected: PASS with 3 tests.

- [ ] **Step 5: Commit**

Run:

```powershell
git add src/rk1126b_assistant/intent.py tests/test_intent.py
git commit -m "feat: add safe intent parser"
```

## Task 3: Scene State

**Files:**
- Create: `src/rk1126b_assistant/scene.py`
- Create: `tests/test_scene.py`

- [ ] **Step 1: Write failing scene tests**

Create `tests/test_scene.py`:

```python
import unittest

from rk1126b_assistant.scene import Detection, SceneState


class SceneStateTests(unittest.TestCase):
    def test_lists_unique_objects_by_confidence(self):
        scene = SceneState(
            detections=[
                Detection("cup", 0.82, (0, 0, 10, 10)),
                Detection("phone", 0.91, (10, 0, 20, 10)),
                Detection("cup", 0.73, (0, 0, 12, 12)),
            ]
        )

        self.assertEqual(scene.list_objects(), ["phone", "cup"])

    def test_finds_object_position_region(self):
        scene = SceneState(
            frame_width=300,
            detections=[Detection("phone", 0.9, (210, 20, 270, 80))],
        )

        result = scene.find("phone")

        self.assertTrue(result.found)
        self.assertEqual(result.region, "right")

    def test_reports_missing_object(self):
        scene = SceneState(detections=[])

        result = scene.find("book")

        self.assertFalse(result.found)
        self.assertEqual(result.label, "book")


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `$env:PYTHONPATH='src'; python -m unittest tests.test_scene -v`

Expected: ERROR because `rk1126b_assistant.scene` does not exist.

- [ ] **Step 3: Implement scene state**

Create `src/rk1126b_assistant/scene.py`:

```python
from dataclasses import dataclass, field
from time import time


BBox = tuple[int, int, int, int]


@dataclass(frozen=True)
class Detection:
    label: str
    confidence: float
    bbox: BBox

    @property
    def center_x(self) -> float:
        x1, _, x2, _ = self.bbox
        return (x1 + x2) / 2


@dataclass(frozen=True)
class FindResult:
    label: str
    found: bool
    region: str | None = None
    confidence: float | None = None
    bbox: BBox | None = None


@dataclass
class SceneState:
    detections: list[Detection] = field(default_factory=list)
    frame_width: int = 640
    updated_at: float = field(default_factory=time)

    def list_objects(self) -> list[str]:
        best: dict[str, float] = {}
        for detection in self.detections:
            best[detection.label] = max(best.get(detection.label, 0.0), detection.confidence)
        return [label for label, _ in sorted(best.items(), key=lambda item: item[1], reverse=True)]

    def find(self, label: str) -> FindResult:
        matches = [item for item in self.detections if item.label == label]
        if not matches:
            return FindResult(label=label, found=False)

        best = max(matches, key=lambda item: item.confidence)
        return FindResult(
            label=label,
            found=True,
            region=self._region_for(best),
            confidence=best.confidence,
            bbox=best.bbox,
        )

    def has_any(self, labels: set[str]) -> bool:
        return any(item.label in labels for item in self.detections)

    def _region_for(self, detection: Detection) -> str:
        third = self.frame_width / 3
        if detection.center_x < third:
            return "left"
        if detection.center_x < third * 2:
            return "center"
        return "right"
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `$env:PYTHONPATH='src'; python -m unittest tests.test_scene -v`

Expected: PASS with 3 tests.

- [ ] **Step 5: Commit**

Run:

```powershell
git add src/rk1126b_assistant/scene.py tests/test_scene.py
git commit -m "feat: add scene state queries"
```

## Task 4: Action Registry And Controller

**Files:**
- Create: `src/rk1126b_assistant/actions.py`
- Create: `src/rk1126b_assistant/config.py`
- Create: `src/rk1126b_assistant/controller.py`
- Create: `tests/test_controller.py`

- [ ] **Step 1: Write failing controller tests**

Create `tests/test_controller.py`:

```python
import unittest

from rk1126b_assistant.controller import AssistantController
from rk1126b_assistant.scene import Detection, SceneState


class ControllerTests(unittest.TestCase):
    def test_lists_visible_objects(self):
        controller = AssistantController()
        scene = SceneState(detections=[Detection("phone", 0.9, (1, 1, 20, 20))])

        response = controller.handle_text("桌上有什么", scene)

        self.assertEqual(response.intent, "list_objects")
        self.assertEqual(response.message, "当前识别到: phone")

    def test_finds_phone_and_reports_region(self):
        controller = AssistantController()
        scene = SceneState(
            frame_width=300,
            detections=[Detection("phone", 0.9, (210, 20, 270, 80))],
        )

        response = controller.handle_text("帮我找手机", scene)

        self.assertEqual(response.intent, "find_object")
        self.assertEqual(response.message, "phone 在画面 right 区域")

    def test_open_study_site_returns_dry_run_action(self):
        controller = AssistantController()
        scene = SceneState()

        response = controller.handle_text("打开学习网页", scene)

        self.assertEqual(response.intent, "open_study_site")
        self.assertEqual(response.action.name, "open_study_site")
        self.assertFalse(response.action.execute)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `$env:PYTHONPATH='src'; python -m unittest tests.test_controller -v`

Expected: ERROR because `rk1126b_assistant.controller` does not exist.

- [ ] **Step 3: Implement config, actions, and controller**

Create `src/rk1126b_assistant/config.py`:

```python
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AssistantConfig:
    study_url: str = "https://www.icourse163.org/"
    browser_command: str = "browser"
    music_file: Path = Path("demo_media/music/sample.mp3")
    video_file: Path = Path("demo_media/video/sample.mp4")
    dry_run: bool = True
```

Create `src/rk1126b_assistant/actions.py`:

```python
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
```

Create `src/rk1126b_assistant/controller.py`:

```python
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
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `$env:PYTHONPATH='src'; python -m unittest tests.test_controller -v`

Expected: PASS with 3 tests.

- [ ] **Step 5: Run all tests**

Run: `$env:PYTHONPATH='src'; python -m unittest discover -s tests -v`

Expected: PASS with all tests.

- [ ] **Step 6: Commit**

Run:

```powershell
git add src/rk1126b_assistant/actions.py src/rk1126b_assistant/config.py src/rk1126b_assistant/controller.py tests/test_controller.py
git commit -m "feat: add multimodal controller core"
```

## Task 5: CLI Demo And Linux Deployment Placeholders

**Files:**
- Create: `src/rk1126b_assistant/main.py`
- Create: `deploy/linux/README.md`
- Create: `deploy/linux/install_debian.sh`
- Create: `deploy/linux/rk1126b-assistant.service`
- Modify: `docs/project-proposal.md`
- Modify: `README.md`

- [ ] **Step 1: Write failing CLI smoke test**

Create `tests/test_cli.py`:

```python
import unittest

from rk1126b_assistant.main import run_demo_command


class CliTests(unittest.TestCase):
    def test_demo_command_returns_message(self):
        message = run_demo_command("桌上有什么")

        self.assertIn("当前未识别到工位物品", message)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `$env:PYTHONPATH='src'; python -m unittest tests.test_cli -v`

Expected: ERROR because `rk1126b_assistant.main` does not exist.

- [ ] **Step 3: Implement CLI demo entry point**

Create `src/rk1126b_assistant/main.py`:

```python
from .controller import AssistantController
from .scene import SceneState


def run_demo_command(text: str) -> str:
    controller = AssistantController()
    response = controller.handle_text(text, SceneState())
    return response.message


def main() -> int:
    print("RV1126B assistant Windows demo. Type a command, or empty input to exit.")
    while True:
        text = input("> ").strip()
        if not text:
            return 0
        print(run_demo_command(text))


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run CLI test**

Run: `$env:PYTHONPATH='src'; python -m unittest tests.test_cli -v`

Expected: PASS with 1 test.

- [ ] **Step 5: Add Linux deployment placeholders**

Create `deploy/linux/README.md`:

```markdown
# RV1126B Debian 部署占位说明

这些文件用于后续在 ELF-RV1126B Debian 12 环境中部署。当前 Windows 阶段不直接运行板端脚本。

后续需要确认：

- 摄像头设备路径，例如 `/dev/video0`
- 麦克风设备名称
- RKNN Runtime 安装路径
- Chromium 或其他浏览器命令
- `mpv` 或板端可用播放器
```

Create `deploy/linux/install_debian.sh`:

```sh
#!/usr/bin/env sh
set -eu

echo "This script is a guarded placeholder for ELF-RV1126B Debian setup."
echo "Review package names on the board before enabling installation commands."
exit 0
```

Create `deploy/linux/rk1126b-assistant.service`:

```ini
[Unit]
Description=RV1126B Multimodal Assistant
After=network-online.target sound.target

[Service]
Type=simple
WorkingDirectory=/opt/rk1126b-assistant
Environment=PYTHONPATH=/opt/rk1126b-assistant/src
ExecStart=/usr/bin/python3 -m rk1126b_assistant.main
Restart=on-failure
RestartSec=3

[Install]
WantedBy=multi-user.target
```

- [ ] **Step 6: Update docs**

Add README sections:

```markdown
## 当前代码范围

第一阶段代码只实现可在 Windows 测试的核心逻辑：语音文本到意图、视觉检测结果查询、动作白名单规划和 CLI demo。摄像头、麦克风、RKNN、GUI 和播放器真实控制将在 RV1126B 环境确认后接入。

## CLI Demo

```powershell
$env:PYTHONPATH="src"
python -m rk1126b_assistant.main
```
```

Add to `docs/project-proposal.md` under the technical route section:

```markdown
第一阶段工程实现采用 Windows 可测试核心与 Linux 部署占位分离的方式。Windows 端先验证意图解析、场景查询和动作规划；RV1126B 端后续再接入摄像头、麦克风、RKNN Runtime、PyQt 和系统播放器。
```

- [ ] **Step 7: Run all tests**

Run: `$env:PYTHONPATH='src'; python -m unittest discover -s tests -v`

Expected: PASS with all tests.

- [ ] **Step 8: Commit**

Run:

```powershell
git add src/rk1126b_assistant/main.py tests/test_cli.py deploy README.md docs/project-proposal.md
git commit -m "chore: add cli demo and linux deployment placeholders"
```

## Self-Review

- Spec coverage: The plan covers the first-stage scaffold, Windows-testable core logic, Linux deployment placeholders, and documentation updates requested by the user.
- Placeholder scan: Linux files are intentionally labeled as guarded placeholders, with explicit non-destructive behavior and concrete follow-up hardware facts to confirm.
- Type consistency: `IntentName`, `Intent`, `Detection`, `SceneState`, `ActionPlan`, and `AssistantResponse` are defined before use and referenced consistently.
