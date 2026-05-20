import unittest

from rk1126b_assistant.scene import Detection, SceneState


class SceneStateTests(unittest.TestCase):
    def test_lists_unique_objects_by_confidence(self):
        scene = SceneState(
            detections=[
                Detection("cup", 0.82, (0, 0, 10, 10)),
                Detection("phone", 0.91, (10, 0, 20, 10)),
                Detection("cup", 0.73, (0, 0, 12, 12)),
            ]
        )

        self.assertEqual(scene.list_objects(), ["phone", "cup"])

    def test_finds_object_position_region(self):
        scene = SceneState(
            frame_width=300,
            detections=[Detection("phone", 0.9, (210, 20, 270, 80))],
        )

        result = scene.find("phone")

        self.assertTrue(result.found)
        self.assertEqual(result.region, "right")

    def test_reports_missing_object(self):
        scene = SceneState(detections=[])

        result = scene.find("book")

        self.assertFalse(result.found)
        self.assertEqual(result.label, "book")


if __name__ == "__main__":
    unittest.main()
