import unittest

from rk1126b_assistant.gui_model import GuiModel


class GuiModelTests(unittest.TestCase):
    def test_loads_scene_and_projects_detection_boxes(self):
        model = GuiModel(scene_name="study_desk", canvas_width=320, canvas_height=180)

        drawables = model.detection_drawables()

        self.assertEqual([item.label for item in drawables], ["phone", "book", "cup"])
        self.assertEqual(drawables[0].bbox, (215, 60, 265, 130))

    def test_submit_command_adds_response_log(self):
        model = GuiModel(scene_name="study_desk")

        entry = model.submit_command("桌上有什么")

        self.assertEqual(entry.command, "桌上有什么")
        self.assertEqual(entry.response, "当前识别到: phone, book, cup")
        self.assertIsNone(entry.action_message)
        self.assertEqual(model.logs[-1], entry)

    def test_submit_action_command_includes_dry_run_message(self):
        model = GuiModel(scene_name="study_desk")

        entry = model.submit_command("打开学习网页")

        self.assertEqual(entry.response, "已规划动作: open_study_site")
        self.assertEqual(entry.action_message, "dry-run: browser https://www.icourse163.org/")


if __name__ == "__main__":
    unittest.main()
