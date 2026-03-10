import os
from trimesh.scene.scene import Scene
from ThreeDToLD.model_loaders.modelloader import Modelloader
from ThreeDToLD.model_loaders.trimeshloader import Trimeshloader
from ThreeDToLD.model_loaders.threemfloader import Threemfloader


class Autoloader(Modelloader):

    def load_model(self, file) -> tuple[Scene, dict]:
        _, file_extension = os.path.splitext(file)

        if file_extension == ".3mf":
            loader = Threemfloader()
        else:
            loader = Trimeshloader()

        return loader.load_scene(file)
