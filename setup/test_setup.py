# test_setup.py
# How to use:
# omni_python setup/test_setup.py

import numpy as np
from omni.isaac.kit import SimulationApp

# Launch Isaac Sim in headless or GUI mode
config = {"headless": False}
simulation_app = SimulationApp(config)

from omni.isaac.core import World
from omni.isaac.core.objects import DynamicCuboid, GroundPlane
from pxr import Gf, UsdLux

# Create world
world = World(stage_units_in_meters=1.0)

# Ground at z = 0
ground = GroundPlane(
    prim_path="/World/Ground",
    name="ground",
    physics_material=None,  # use default
    visible=True
)
world.scene.add(ground)

# Add a dynamic cube, falling above the ground
cube = world.scene.add(
    DynamicCuboid(
        prim_path="/World/TestCube",
        name="cube",
        position=[0.0, 0.0, 1.0],
        size=0.1,
        color=np.array([0.0, 0.0, 1.0], dtype=np.float32),  # <-- key fix
    )
)


# Simple light (helps if the viewport looks dark)
stage = world.scene.stage
distant = UsdLux.DistantLight.Define(stage, "/World/KeyLight")
distant.CreateIntensityAttr(3000)
distant.AddTranslateOp().Set(Gf.Vec3f(1.0, -2.0, 3.0))

# Reset and step the world
world.reset()
print("✅ Isaac Sim world initialized, stepping simulation...")

for i in range(120):
    world.step(render=True)
    if i % 30 == 0:
        pos, _ = cube.get_world_pose()
        print(f"Step {i}: cube at {pos}")

print("✅ Simulation ran successfully.")
simulation_app.close()
