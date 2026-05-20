from .scene import Detection, SceneState


_SCENES = {
    "empty": SceneState(detections=[]),
    "study_desk": SceneState(
        detections=[
            Detection("phone", 0.95, (430, 120, 530, 260)),
            Detection("book", 0.91, (190, 160, 380, 330)),
            Detection("cup", 0.83, (40, 120, 130, 260)),
        ],
        frame_width=640,
    ),
    "relax_desk": SceneState(
        detections=[
            Detection("phone", 0.92, (420, 140, 530, 280)),
            Detection("cup", 0.88, (60, 120, 150, 260)),
            Detection("mouse", 0.76, (300, 240, 380, 310)),
        ],
        frame_width=640,
    ),
}


def available_scene_names() -> list[str]:
    return sorted(_SCENES)


def load_demo_scene(name: str) -> SceneState:
    try:
        return _SCENES[name]
    except KeyError as exc:
        valid = ", ".join(available_scene_names())
        raise ValueError(f"unknown demo scene '{name}', expected one of: {valid}") from exc
