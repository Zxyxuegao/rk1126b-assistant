import unittest

from rk1126b_assistant.action_executor import ActionExecutor
from rk1126b_assistant.actions import ActionPlan


class ActionExecutorTests(unittest.TestCase):
    def test_dry_run_reports_command_without_running(self):
        calls = []
        executor = ActionExecutor(runner=lambda command: calls.append(command))
        plan = ActionPlan(name="open_study_site", command=("browser", "https://example.test"), execute=False)

        result = executor.execute(plan)

        self.assertFalse(result.executed)
        self.assertEqual(result.message, "dry-run: browser https://example.test")
        self.assertEqual(calls, [])

    def test_execute_uses_injected_runner(self):
        calls = []
        executor = ActionExecutor(runner=lambda command: calls.append(command))
        plan = ActionPlan(name="open_study_site", command=("browser", "https://example.test"), execute=True)

        result = executor.execute(plan)

        self.assertTrue(result.executed)
        self.assertEqual(result.message, "executed: browser https://example.test")
        self.assertEqual(calls, [("browser", "https://example.test")])


if __name__ == "__main__":
    unittest.main()
