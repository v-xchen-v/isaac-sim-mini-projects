from omni.isaac.kit import SimulationApp

# Launch Isaac Sim in headless or GUI mode
config = {"headless": False}
simulation_app = SimulationApp(config)

from omni.isaac.core import World
from omni.isaac.core.prims.rigid_prim import RigidPrim
from build_task_layout.util_layout import LayoutBuilder   # <- import your shared LayoutBuilder

class HelloWorldTask:
    def __init__(self, layout_yaml):
        self.layout_yaml = layout_yaml
        self.layout_builder = None

    def set_up_scene(self):
        self.layout_builder = LayoutBuilder(self.layout_yaml)
        self.layout_builder.build()
        # self.world.reset()
        # self.cube_view = RigidPrim(prim_path=["/World/Cube"])
        # self.world.scene.add(self.cube_view)

    def reset(self):
        self.set_up_scene()

    def get_observations(self):
        # poses, _ = self.cube_view.get_world_pose()
        # return {"cube_pos": poses[:3].tolist()}
        return None


    def is_done(self):
        return False
