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
