import argparse
import tkinter as tk
from tkinter import ttk

from .demo_scenes import available_scene_names
from .gui_model import GuiModel


class WindowsDemoApp:
    def __init__(self, root: tk.Tk, model: GuiModel):
        self.root = root
        self.model = model
        self.root.title("RV1126B Multimodal Assistant Demo")

        self.scene_var = tk.StringVar(value=model.scene_name)
        self.command_var = tk.StringVar(value="桌上有什么")

        self._build_layout()
        self._redraw_scene()
        self._append_log("系统", "Windows 模拟演示已启动")

    def _build_layout(self) -> None:
        self.root.columnconfigure(0, weight=3)
        self.root.columnconfigure(1, weight=2)
        self.root.rowconfigure(0, weight=1)

        self.canvas = tk.Canvas(self.root, width=self.model.canvas_width, height=self.model.canvas_height, bg="#f7f3ea")
        self.canvas.grid(row=0, column=0, sticky="nsew", padx=12, pady=12)

        side = ttk.Frame(self.root, padding=12)
        side.grid(row=0, column=1, sticky="nsew")
        side.columnconfigure(0, weight=1)
        side.rowconfigure(5, weight=1)

        ttk.Label(side, text="模拟场景").grid(row=0, column=0, sticky="w")
        scene_box = ttk.Combobox(side, textvariable=self.scene_var, values=available_scene_names(), state="readonly")
        scene_box.grid(row=1, column=0, sticky="ew", pady=(4, 12))
        scene_box.bind("<<ComboboxSelected>>", lambda _event: self._change_scene())

        ttk.Label(side, text="指令输入").grid(row=2, column=0, sticky="w")
        entry = ttk.Entry(side, textvariable=self.command_var)
        entry.grid(row=3, column=0, sticky="ew", pady=(4, 8))
        entry.bind("<Return>", lambda _event: self._submit_command())

        button_row = ttk.Frame(side)
        button_row.grid(row=4, column=0, sticky="ew", pady=(0, 12))
        ttk.Button(button_row, text="发送", command=self._submit_command).pack(side="left")
        ttk.Button(button_row, text="重绘场景", command=self._redraw_scene).pack(side="left", padx=(8, 0))

        self.log = tk.Text(side, width=42, height=18, state="disabled")
        self.log.grid(row=5, column=0, sticky="nsew")

    def _change_scene(self) -> None:
        self.model.set_scene(self.scene_var.get())
        self._redraw_scene()
        self._append_log("场景", self.scene_var.get())

    def _redraw_scene(self) -> None:
        self.canvas.delete("all")
        self.canvas.create_rectangle(16, 16, self.model.canvas_width - 16, self.model.canvas_height - 16, outline="#d6cab8")
        self.canvas.create_text(24, 24, anchor="nw", text=f"scene: {self.model.scene_name}", fill="#4f5d75")

        colors = {
            "phone": "#2d6cdf",
            "book": "#2a9d8f",
            "cup": "#e76f51",
            "mouse": "#6d597a",
            "notebook": "#457b9d",
            "keyboard": "#5c677d",
        }
        for item in self.model.detection_drawables():
            x1, y1, x2, y2 = item.bbox
            color = colors.get(item.label, "#2b2d42")
            self.canvas.create_rectangle(x1, y1, x2, y2, outline=color, width=3)
            self.canvas.create_text(x1 + 4, y1 + 4, anchor="nw", text=f"{item.label} {item.confidence:.2f}", fill=color)

    def _submit_command(self) -> None:
        command = self.command_var.get().strip()
        if not command:
            return

        entry = self.model.submit_command(command)
        self._append_log("用户", entry.command)
        self._append_log("助手", entry.response)
        if entry.action_message:
            self._append_log("动作", entry.action_message)

    def _append_log(self, role: str, message: str) -> None:
        self.log.configure(state="normal")
        self.log.insert("end", f"[{role}] {message}\n")
        self.log.see("end")
        self.log.configure(state="disabled")


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="RV1126B assistant Tkinter demo")
    parser.add_argument("--scene", default="study_desk", choices=available_scene_names())
    return parser


def main() -> int:
    args = build_arg_parser().parse_args()
    root = tk.Tk()
    model = GuiModel(scene_name=args.scene)
    WindowsDemoApp(root, model)
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
