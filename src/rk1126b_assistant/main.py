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
