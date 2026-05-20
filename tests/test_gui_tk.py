import unittest

from rk1126b_assistant.gui_tk import build_arg_parser


class GuiTkTests(unittest.TestCase):
    def test_arg_parser_defaults_to_study_desk(self):
        args = build_arg_parser().parse_args([])

        self.assertEqual(args.scene, "study_desk")

    def test_arg_parser_accepts_relax_scene(self):
        args = build_arg_parser().parse_args(["--scene", "relax_desk"])

        self.assertEqual(args.scene, "relax_desk")


if __name__ == "__main__":
    unittest.main()
