import argparse

from .controller import AssistantController
from .demo_scenes import available_scene_names, load_demo_scene


def run_demo_command(text: str, scene_name: str = "empty") -> str:
    controller = AssistantController()
    response = controller.handle_text(text, load_demo_scene(scene_name))
    return response.message


def main() -> int:
    parser = argparse.ArgumentParser(description="RV1126B assistant Windows demo")
    parser.add_argument("--scene", default="empty", choices=available_scene_names())
    args = parser.parse_args()

    print("RV1126B assistant Windows demo. Type a command, or empty input to exit.")
    print(f"Scene: {args.scene}. Available scenes: {', '.join(available_scene_names())}")
    while True:
        text = input("> ").strip()
        if not text:
            return 0
        print(run_demo_command(text, scene_name=args.scene))


if __name__ == "__main__":
    raise SystemExit(main())
