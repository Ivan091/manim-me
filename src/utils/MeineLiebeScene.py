from pathlib import Path
from typing import Any

from manim import *
from manim.mobject.mobject import _AnimationBuilder
from manim.typing import Vector3D


class MeineLiebeScene(Scene):
    scene_number = Integer(0).set_color(LIGHT_GRAY).move_to(UP * 3.5 + LEFT * 7)
    use_scene_number = config.preview
    current_section_name = None

    def setup(self) -> None:
        Tex.set_default(font_size=60)
        Text.set_default(font_size=60)
        if self.use_scene_number:
            self.add(self.scene_number)

    def play(
        self,
        *args: Animation | Mobject | _AnimationBuilder,
        **kwargs: Any,
    ) -> None:
        super().play(*args, **kwargs)
        self.update_scene_number()

    def next_section(
        self,
        name: str = "unnamed",
        section_type: str = DefaultSectionType.NORMAL,
        skip_animations: bool = False,
    ) -> None:
        if self.current_section_name is not None:
            self.save_section_frame(self.current_section_name)
        self.current_section_name = name
        super().next_section(name, section_type, skip_animations)

    def update_scene_number(self):
        if self.use_scene_number:
            self.scene_number.set_value(self.scene_number.get_value() + 1)

    def save_section_frame(self, name: str | None = None) -> None:
        if name is None:
            name = self.current_section_name

        scene_dir = Path(config.get_dir("media_dir")) / "images" / self.__class__.__name__
        scene_dir.mkdir(parents=True, exist_ok=True)
        full_path = scene_dir / f"{len(self.renderer.file_writer.sections):04}_{name}.png"
        self.camera.get_image().save(full_path)
        logger.info(f"Saved section frame to: {full_path}")

    def tag_vgroup(self, group: VGroup, color: ManimColor = GREEN, direction: Vector3D = UP):
        tags = VGroup()
        for i, vm in enumerate(group):
            tags.add(
                Text(str(i), font_size=10).next_to(vm, direction).set_color(color)
            )

        self.add(tags)

    def get_all_vmobjects(self) -> list[VMobject]:
        vmobjects = []
        for item in self.mobjects:
            if isinstance(item, VMobject):
                vmobjects.append(item)
        return vmobjects
