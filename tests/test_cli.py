import unittest

from rk1126b_assistant.main import run_demo_command


class CliTests(unittest.TestCase):
    def test_demo_command_returns_message(self):
        message = run_demo_command("桌上有什么")

        self.assertIn("当前未识别到工位物品", message)

    def test_demo_command_uses_named_scene(self):
        message = run_demo_command("桌上有什么", scene_name="study_desk")

        self.assertEqual(message, "当前识别到: phone, book, cup")

    def test_demo_command_finds_phone_in_named_scene(self):
        message = run_demo_command("帮我找手机", scene_name="study_desk")

        self.assertEqual(message, "phone 在画面 right 区域")


if __name__ == "__main__":
    unittest.main()
