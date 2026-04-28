from trimesh.scene.scene import Scene
from trimesh import load_scene
from ThreeDToLD.model_loaders.modelloader import Modelloader


class Trimeshloader(Modelloader):
    def __init__(self, use_step_options=False,
                 tol_linear: int | float = None,
                 tol_angular: int | float = None,
                 tol_relative: bool = False):
        self.use_step_options = use_step_options
        if self.use_step_options:
            self.tol_linear = tol_linear
            self.tol_angular = tol_angular
            self.tol_relative = tol_relative

    def load_model(self, file) -> tuple[Scene, dict]:
        if self.use_step_options:
            return load_scene(file,
                              tol_linear=self.tol_linear,
                              tol_angular=self.tol_angular,
                              tol_relative=self.tol_relative), {}
        return load_scene(file), {}
