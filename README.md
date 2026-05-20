# 基于 RV1126B 的端侧多模态人机交互终端

本项目面向校园工位、学习桌面和个人工作台等轻量场景，基于 ELF-RV1126B 开发板构建一个可离线运行的端侧多模态人机交互终端。

系统通过语音识别理解用户指令，通过视觉模型感知工位常见物品，并调用本地浏览器、播放器等系统软件完成学习、娱乐和找物等任务，形成“语音输入、视觉理解、系统执行、界面反馈”的闭环交互。

## 项目文档

- [项目方案](docs/project-proposal.md)
- [RV1126B 板端迁移指南](docs/board-porting-guide.md)

## 第一版目标

- 使用 YOLOv5n + RKNN 在 RV1126B NPU 上完成工位物品检测。
- 使用 Vosk 小型中文离线 ASR 和规则意图解析完成固定语音指令识别。
- 使用 PyQt 构建本地 GUI，显示摄像头画面、检测结果、语音文本和执行状态。
- 支持打开学习网页、播放本地音乐、播放本地视频、暂停播放等系统控制动作。
- 支持“桌上有什么”“帮我找手机”等语音触发的视觉查询。

## Windows 开发测试

当前第一阶段只依赖 Python 标准库，可在 Windows 上直接运行核心逻辑测试：

```powershell
$env:PYTHONPATH="src"
python -m unittest discover -s tests -v
```

## 当前代码范围

第一阶段代码只实现可在 Windows 测试的核心逻辑：语音文本到意图、视觉检测结果查询、动作白名单规划和 CLI demo。摄像头、麦克风、RKNN、GUI 和播放器真实控制将在 RV1126B 环境确认后接入。

## CLI Demo

```powershell
$env:PYTHONPATH="src"
python -m rk1126b_assistant.main
```

可以通过 `--scene` 选择 Windows 模拟桌面场景，不需要摄像头也能演示多模态逻辑：

```powershell
$env:PYTHONPATH="src"
python -m rk1126b_assistant.main --scene study_desk
```

可用场景：

- `empty`：空桌面，用于验证无检测结果时的反馈。
- `study_desk`：包含 `phone`、`book`、`cup`，用于演示“桌上有什么”“帮我找手机”“我准备学习了”。
- `relax_desk`：包含 `phone`、`cup`、`mouse`，用于演示生活娱乐场景。

## Windows GUI Demo

可以启动 Tkinter 图形界面，左侧显示模拟检测框，右侧输入指令并查看响应日志：

```powershell
$env:PYTHONPATH="src"
python -m rk1126b_assistant.gui_tk --scene study_desk
```

这个 GUI 仍然使用模拟视觉结果，不依赖摄像头、麦克风、RKNN 或 Linux 环境。

## GitHub 远程仓库配置

仓库创建后，将下面命令中的占位符替换为你的 GitHub 仓库地址：

```powershell
git remote add origin https://github.com/Zxyxuegao/rk1126b-assistant.git
git branch -M main
git push -u origin main
```

如果你使用 SSH：

```powershell
git remote add origin git@github.com:Zxyxuegao/rk1126b-assistant.git
git branch -M main
git push -u origin main
```

## 建议目录

```text
docs/                 项目文档
src/                  主程序代码
models/               模型配置与占位说明
scripts/              训练、转换、部署脚本
demo_media/           演示用媒体说明或小型样例
```

大型数据集、模型权重、录制视频和运行日志不建议直接提交到 Git 仓库，已在 `.gitignore` 中默认排除。
