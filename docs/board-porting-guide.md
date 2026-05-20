# RV1126B 板端迁移指南

本文档记录当前 Windows 阶段完成后的板端工作清单。进入 ELF-RV1126B Debian 12 环境后，优先按本文档确认硬件、依赖和代码接入点。

## 当前 Windows 阶段已经完成

- 意图解析：`src/rk1126b_assistant/intent.py`
- 场景状态与找物逻辑：`src/rk1126b_assistant/scene.py`
- 多模态控制器：`src/rk1126b_assistant/controller.py`
- 动作规划与 dry-run 执行边界：`src/rk1126b_assistant/actions.py`、`src/rk1126b_assistant/action_executor.py`
- Windows 模拟场景：`src/rk1126b_assistant/demo_scenes.py`
- Windows Tkinter 演示界面：`src/rk1126b_assistant/gui_tk.py`
- Linux 部署占位：`deploy/linux/`

这些模块在板端仍然可以复用。板端开发的重点是把模拟输入替换为真实输入。

## 板端第一轮环境确认

在 RV1126B Debian 12 上先确认以下信息：

```sh
python3 --version
uname -a
ls /dev/video*
arecord -l
aplay -l
which chromium || which chromium-browser || which firefox
which mpv
```

需要记录：

- 摄像头设备路径，例如 `/dev/video0`
- 麦克风设备编号或 ALSA 名称
- 显示屏分辨率和是否能启动桌面环境
- 浏览器命令名称
- 播放器命令名称
- RKNN Runtime 的安装方式和示例是否能运行

## 推荐板端开发顺序

### 1. 跑通纯 Python 核心测试

把仓库拉到板端后先运行：

```sh
export PYTHONPATH=src
python3 -m unittest discover -s tests -v
```

如果纯逻辑测试失败，先修复 Python 版本或路径问题，不要急着接摄像头。

### 2. 跑通 CLI 和模拟 GUI

```sh
export PYTHONPATH=src
python3 -m rk1126b_assistant.main --scene study_desk
```

如果板端有桌面环境，再尝试：

```sh
export PYTHONPATH=src
python3 -m rk1126b_assistant.gui_tk --scene study_desk
```

这一步确认 Python 包、显示环境和基础交互没有问题。

### 3. 接入真实视觉模块

当前模拟场景来自：

```text
src/rk1126b_assistant/demo_scenes.py
```

板端需要新增真实视觉适配模块，建议文件名：

```text
src/rk1126b_assistant/vision_rknn.py
```

它的目标是输出 `SceneState`：

```python
from rk1126b_assistant.scene import Detection, SceneState


def read_scene() -> SceneState:
    return SceneState(
        frame_width=640,
        detections=[
            Detection("phone", 0.90, (100, 80, 180, 200)),
        ],
    )
```

真实实现时把摄像头采集、预处理、RKNN 推理、后处理框都封装在 `read_scene()` 内。控制器不需要知道数据来自模拟场景还是真实模型。

### 4. 接入语音识别

当前 Windows 阶段使用文本输入模拟语音识别结果。板端建议新增：

```text
src/rk1126b_assistant/asr_vosk.py
```

它的目标是输出一段中文文本：

```python
def listen_once() -> str:
    return "桌上有什么"
```

第一版不要做持续唤醒，优先做按键或界面按钮触发的短时录音。稳定后再讨论唤醒词和 Whisper-tiny 增强模式。

### 5. 替换系统动作命令

当前动作规划在：

```text
src/rk1126b_assistant/actions.py
src/rk1126b_assistant/config.py
```

板端需要确认并修改：

- `browser_command`：例如 `chromium` 或 `chromium-browser`
- `music_file`：板端实际音乐文件路径
- `video_file`：板端实际视频文件路径
- 暂停播放命令：如果没有 `playerctl`，改为 `mpv` IPC 或其他播放器控制方式

默认保持 `dry_run=True`，确认命令无误后再改为可执行模式。

### 6. GUI 选择

当前 Tkinter GUI 用于 Windows 预演。板端有两个路线：

- 继续使用 Tkinter：最快验证，适合早期调试。
- 改成 PyQt/Qt：更适合最终展示，界面能力更强。

无论选择哪种 GUI，都建议复用 `GuiModel`：

```text
src/rk1126b_assistant/gui_model.py
```

GUI 只负责显示和输入，核心逻辑继续通过 `GuiModel.submit_command()` 调用。

## 代码改造边界

板端开发时优先新增适配模块，不要直接改控制器核心：

- 新增视觉输入：`vision_rknn.py`
- 新增语音输入：`asr_vosk.py`
- 必要时新增板端入口：`board_main.py`
- 尽量保留 `intent.py`、`scene.py`、`controller.py` 的接口稳定

这样 Windows 模拟测试仍可继续运行，板端改动也更容易定位问题。

## 板端验收清单

- `python3 -m unittest discover -s tests -v` 通过
- 摄像头可采集一帧图像
- RKNN 模型能输出至少一种工位物品检测结果
- Vosk 能识别 3 到 5 条固定中文指令
- `桌上有什么` 能读取真实检测结果
- `帮我找手机` 能返回左/中/右区域
- `打开学习网页` 在 dry-run 下显示正确命令
- 真实执行模式下能打开浏览器或播放器
- 连续运行 10 分钟无崩溃

## 建议不要过早做的事情

- 不要一开始就做持续唤醒
- 不要一开始就把 Whisper-tiny 放进主流程
- 不要一开始就扩展太多识别类别
- 不要在未确认命令前开启真实系统执行
- 不要把数据集、模型权重和演示视频直接提交进 Git
