import unittest

from rk1126b_assistant.intent import IntentName, parse_intent


class IntentParserTests(unittest.TestCase):
    def test_parses_open_study_site(self):
        intent = parse_intent("打开学习网页")

        self.assertEqual(intent.name, IntentName.OPEN_STUDY_SITE)
        self.assertEqual(intent.target, "study_site")

    def test_parses_find_phone(self):
        intent = parse_intent("帮我找手机")

        self.assertEqual(intent.name, IntentName.FIND_OBJECT)
        self.assertEqual(intent.target, "phone")

    def test_unknown_command_is_safe(self):
        intent = parse_intent("删除所有文件")

        self.assertEqual(intent.name, IntentName.UNKNOWN)
        self.assertIsNone(intent.target)


if __name__ == "__main__":
    unittest.main()
