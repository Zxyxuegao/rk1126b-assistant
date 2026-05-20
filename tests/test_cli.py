import unittest

from rk1126b_assistant.main import run_demo_command


class CliTests(unittest.TestCase):
    def test_demo_command_returns_message(self):
        message = run_demo_command("桌上有什么")

        self.assertIn("当前未识别到工位物品", message)


if __name__ == "__main__":
    unittest.main()
