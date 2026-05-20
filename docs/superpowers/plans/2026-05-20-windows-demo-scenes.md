# Windows Demo Scenes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add Windows-testable simulated scene presets so the CLI demo can show multimodal behavior without camera, microphone, RKNN, or Linux hardware.

**Architecture:** Keep simulated detections in a dedicated `demo_scenes` module. The CLI remains a thin wrapper that loads a named scene, sends text commands to `AssistantController`, and prints the response.

**Tech Stack:** Python 3.12, standard-library `unittest`, existing `SceneState`, `Detection`, and `AssistantController`.

---

## File Structure

- Create `src/rk1126b_assistant/demo_scenes.py`: named fake desktop scenes for Windows development.
- Modify `src/rk1126b_assistant/main.py`: add `scene_name` support and a `--scene` CLI option.
- Create `tests/test_demo_scenes.py`: scene preset behavior tests.
- Modify `tests/test_cli.py`: CLI helper tests with named scene presets.
- Modify `README.md`: document simulated demo commands.
- Modify `docs/project-proposal.md`: record that Windows simulation is the current development bridge before real hardware.

## Task 1: Demo Scene Presets

**Files:**
- Create: `tests/test_demo_scenes.py`
- Create: `src/rk1126b_assistant/demo_scenes.py`

- [ ] **Step 1: Write failing demo scene tests**

Create `tests/test_demo_scenes.py` with tests that expect a `study_desk` scene to contain `phone`, `book`, and `cup`, and expect unknown scene names to fail with `ValueError`.

- [ ] **Step 2: Run tests to verify they fail**

Run: `$env:PYTHONPATH='src'; python -m unittest tests.test_demo_scenes -v`

Expected: ERROR because `rk1126b_assistant.demo_scenes` does not exist.

- [ ] **Step 3: Implement `demo_scenes.py`**

Create named presets: `empty`, `study_desk`, and `relax_desk`. Return `SceneState` objects with deterministic fake detections.

- [ ] **Step 4: Run tests to verify they pass**

Run: `$env:PYTHONPATH='src'; python -m unittest tests.test_demo_scenes -v`

Expected: PASS.

## Task 2: CLI Uses Named Scenes

**Files:**
- Modify: `tests/test_cli.py`
- Modify: `src/rk1126b_assistant/main.py`

- [ ] **Step 1: Write failing CLI scene tests**

Extend `tests/test_cli.py` so `run_demo_command("桌上有什么", scene_name="study_desk")` reports `phone`, `book`, and `cup`, and `run_demo_command("帮我找手机", scene_name="study_desk")` reports a screen region.

- [ ] **Step 2: Run tests to verify they fail**

Run: `$env:PYTHONPATH='src'; python -m unittest tests.test_cli -v`

Expected: FAIL because `run_demo_command` does not accept `scene_name`.

- [ ] **Step 3: Implement CLI scene support**

Update `run_demo_command(text, scene_name="empty")`, add `argparse` support for `--scene`, and print available scene names at startup.

- [ ] **Step 4: Run tests to verify they pass**

Run: `$env:PYTHONPATH='src'; python -m unittest tests.test_cli -v`

Expected: PASS.

## Task 3: Documentation And Verification

**Files:**
- Modify: `README.md`
- Modify: `docs/project-proposal.md`

- [ ] **Step 1: Update docs**

Document `python -m rk1126b_assistant.main --scene study_desk` and explain that scene presets are a Windows development bridge before real camera/RKNN integration.

- [ ] **Step 2: Run all tests**

Run: `$env:PYTHONPATH='src'; python -m unittest discover -s tests -v`

Expected: PASS.

- [ ] **Step 3: Commit and push**

Run:

```powershell
git add src tests README.md docs
git commit -m "feat: add windows demo scene presets"
git push
```

## Self-Review

- Spec coverage: Adds a visible simulation layer for current Windows development and leaves Linux/RV1126B hardware integration untouched.
- Placeholder scan: No empty implementation markers are used; the scenes are concrete fake data for repeatable demos.
- Type consistency: `scene_name` is the shared argument name in tests and implementation.
