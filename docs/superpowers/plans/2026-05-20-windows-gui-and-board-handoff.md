# Windows GUI And Board Handoff Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Finish the pre-board Windows demo layer and create a clear RV1126B handoff document.

**Architecture:** Keep executable behavior behind an action executor, keep GUI state in a testable model, and keep Tkinter as a thin standard-library demo shell. The board handoff document lists the Linux files, adapter points, and code that must change once RV1126B hardware is available.

**Tech Stack:** Python 3.12, standard-library `unittest`, `tkinter`, existing `AssistantController`, `SceneState`, and demo scene presets.

---

## File Structure

- Create `src/rk1126b_assistant/action_executor.py`: dry-run and injectable action execution.
- Create `src/rk1126b_assistant/gui_model.py`: UI state, command submission, detection rectangle projection, log entries.
- Create `src/rk1126b_assistant/gui_tk.py`: Tkinter demo app for Windows.
- Create `tests/test_action_executor.py`: action executor behavior tests.
- Create `tests/test_gui_model.py`: GUI state behavior tests.
- Create `tests/test_gui_tk.py`: import and command-line parser smoke tests.
- Modify `README.md`: document Windows GUI launch commands.
- Create `docs/board-porting-guide.md`: RV1126B migration checklist and code touch points.
- Modify `docs/project-proposal.md`: record that GUI demo is the pre-board milestone.

## Task 1: Action Executor

**Files:**
- Create: `tests/test_action_executor.py`
- Create: `src/rk1126b_assistant/action_executor.py`

- [ ] **Step 1: Write failing tests for dry-run and injected execution**
- [ ] **Step 2: Run `python -m unittest tests.test_action_executor -v` and verify it fails because the module is missing**
- [ ] **Step 3: Implement `ActionExecutionResult` and `ActionExecutor`**
- [ ] **Step 4: Run the action executor tests and verify they pass**

## Task 2: GUI Model

**Files:**
- Create: `tests/test_gui_model.py`
- Create: `src/rk1126b_assistant/gui_model.py`

- [ ] **Step 1: Write failing tests for scene loading, command submission, and detection box projection**
- [ ] **Step 2: Run `python -m unittest tests.test_gui_model -v` and verify it fails because the module is missing**
- [ ] **Step 3: Implement `GuiModel`, `CommandLogEntry`, and `DetectionDrawable`**
- [ ] **Step 4: Run the GUI model tests and verify they pass**

## Task 3: Tkinter Demo Shell

**Files:**
- Create: `tests/test_gui_tk.py`
- Create: `src/rk1126b_assistant/gui_tk.py`

- [ ] **Step 1: Write failing tests for GUI module import and parser defaults**
- [ ] **Step 2: Run `python -m unittest tests.test_gui_tk -v` and verify it fails because the module is missing**
- [ ] **Step 3: Implement a Tkinter app with scene selector, canvas, command input, execute checkbox, and log panel**
- [ ] **Step 4: Run the GUI Tk tests and verify they pass**

## Task 4: Documentation And Verification

**Files:**
- Modify: `README.md`
- Create: `docs/board-porting-guide.md`
- Modify: `docs/project-proposal.md`

- [ ] **Step 1: Document Windows GUI commands**
- [ ] **Step 2: Write the board handoff guide covering camera, ASR, RKNN, GUI, media commands, systemd, and validation**
- [ ] **Step 3: Run `python -m unittest discover -s tests -v`**
- [ ] **Step 4: Commit and push**

## Self-Review

- Spec coverage: This plan completes the requested pre-board work by adding a GUI demo, action execution boundary, and board migration documentation.
- Placeholder scan: Board instructions are concrete checklist items, while Linux scripts remain guarded until the board environment is confirmed.
- Type consistency: `GuiModel`, `ActionExecutor`, `ActionExecutionResult`, and `DetectionDrawable` are introduced before GUI code uses them.
