import unittest

from rk1126b_assistant.demo_scenes import available_scene_names, load_demo_scene


class DemoSceneTests(unittest.TestCase):
    def test_study_desk_contains_common_objects(self):
        scene = load_demo_scene("study_desk")

        self.assertEqual(scene.list_objects(), ["phone", "book", "cup"])

    def test_available_scene_names_are_sorted(self):
        self.assertEqual(available_scene_names(), ["empty", "relax_desk", "study_desk"])

    def test_unknown_scene_name_is_rejected(self):
        with self.assertRaises(ValueError) as context:
            load_demo_scene("unknown")

        self.assertIn("unknown demo scene", str(context.exception))


if __name__ == "__main__":
    unittest.main()
