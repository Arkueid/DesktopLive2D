from ui.components.design.motion_editor_design import MotionEditorDesign
from core.model3json import Model3Json


class MotionEditor(MotionEditorDesign):

    def __init__(self, model3Json: Model3Json):
        super().__init__(model3Json)

    