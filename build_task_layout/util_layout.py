import carb
import math
import os
import random
import numpy as np
import omni.usd
from pxr import UsdGeom, Gf, UsdPhysics, PhysxSchema

from omni.isaac.core import World
from omni.isaac.core.utils.semantics import add_update_semantics
from omni.isaac.core.utils.prims import create_prim, get_prim_at_path
from omni.isaac.core.utils.stage import get_current_stage
from omni.isaac.core.prims.rigid_prim import RigidPrim
# from omni.isaac.core.prims import SingleArticulation
from isaacsim.core.prims import SingleArticulation
from omni.isaac.core.utils.nucleus import get_assets_root_path
from isaacsim.core.utils.stage import add_reference_to_stage, get_stage_units
from isaacsim.core.utils.rotations import euler_angles_to_quat

import yaml

def _as_float(v):
    return float(v) if isinstance(v, (int, float)) else v

def _sample(val):
    """Sample from {uniform:[a,b]}, {choice:[...]}, or pass through."""
    if isinstance(val, dict):
        if "uniform" in val:
            a, b = val["uniform"]
            return random.uniform(a, b)
        if "choice" in val:
            return random.choice(val["choice"])
    return val

def _pose6_to_transform(pose):
    """pose = [x,y,z, roll,pitch,yaw] in meters/radians -> Gf.Transform"""
    x,y,z, r,p,y = pose
    t = Gf.Transform()
    t.SetTranslation(Gf.Vec3d(x,y,z))
    R = Gf.Rotation(Gf.Vec3d(1,0,0), math.degrees(r))
    R *= Gf.Rotation(Gf.Vec3d(0,1,0), math.degrees(p))
    R *= Gf.Rotation(Gf.Vec3d(0,0,1), math.degrees(y))
    t.SetRotation(R)
    return t

class LayoutBuilder:
    def __init__(self, layout_yaml_path):
        with open(layout_yaml_path, "r") as f:
            self.cfg = yaml.safe_load(f)
        
        # prepare the scene
        # get_assets_root_path() got https://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/Isaac/4.5
        self.assets_root = get_assets_root_path() or os.environ.get("NVIDIA_ASSETS", "")
        if not self.assets_root:
            carb.log_warn("Assets root not found. Set {NVIDIA_ASSETS} or mount Nucleus.")
        
        self.my_world = World(stage_units_in_meters=1.0)
        self.scene = self.my_world.scene
        self.stage = get_current_stage()

    def _resolve_usd(self, path):
        if "{NVIDIA_ASSETS}" in path:
            return path.replace("{NVIDIA_ASSETS}", self.assets_root)
        return path

    def apply_world(self):
        from isaacsim.core.api.objects.ground_plane import GroundPlane
        # Add Ground Plane
        GroundPlane(prim_path="/World/GroundPlane", z_position=0)

        from pxr import Sdf, UsdLux
        # Add Light Source
        stage = omni.usd.get_context().get_stage()
        distantLight = UsdLux.DistantLight.Define(stage, Sdf.Path("/DistantLight"))
        distantLight.CreateIntensityAttr(300)
        
        from isaacsim.core.utils.viewports import set_camera_view
        # Set Camera View
        set_camera_view(
            eye=[5.0, 0.0, 1.5], target=[0.00, 0.00, 1.00], camera_prim_path="/OmniverseKit_Persp"
        )  # set camera view


        # # gravity & up-axis
        # world_cfg = self.cfg.get("world", {})
        # up_axis = world_cfg.get("up_axis", "z").upper()
        # UsdGeom.SetStageUpAxis(self.stage, UsdGeom.Tokens.z if up_axis == "Z" else UsdGeom.Tokens.y)
        # g_cfg = world_cfg.get("gravity", [0, 0, -9.81])  # meters/s^2 for Isaac 4.5 defaults
        # # self.stage.SetMetadata("physics:gravityMagnitude", float(np.linalg.norm(g)))
        
        # # Set gravity on PhysicsScene
        # # Ensure a PhysicsScene exists
        # physics_scene_path = "/World/physicsScene"
        # physics_scene = UsdPhysics.Scene.Define(self.stage, physics_scene_path)

        # # Parse gravity into (direction unit vec, positive magnitude)
        # def _parse_gravity(g):
        #     # scalar: magnitude, assume -Z direction
        #     if isinstance(g, (int, float)):
        #         return Gf.Vec3f(0.0, 0.0, -1.0), float(abs(g))
        #     # 3-vector: direction + magnitude encoded
        #     if isinstance(g, (list, tuple)) and len(g) == 3:
        #         v = Gf.Vec3f(float(g[0]), float(g[1]), float(g[2]))
        #         mag = v.GetLength()
        #         if mag == 0.0:
        #             # Fallback to Earth gravity down -Z
        #             return Gf.Vec3f(0.0, 0.0, -1.0), 9.81
        #         return (v / mag), float(mag)
        #     # Fallback
        #     return Gf.Vec3f(0.0, 0.0, -1.0), 9.81

        # direction, magnitude = _parse_gravity(g_cfg)

        # # Important: gravityDirection expects a unit vector; gravityMagnitude a positive float
        # physics_scene.CreateGravityDirectionAttr().Set(direction)   # Gf.Vec3f
        # physics_scene.CreateGravityMagnitudeAttr().Set(float(np.linalg.norm(g_cfg)))   # float

        # # # enable physics
        # # UsdPhysics.Scene.Define(self.stage, "/World/physicsScene")
        
        # # Reset my world
        # self.my_world.reset()

    def spawn_articulation(self, usd_path, prim_path, pose, default_joints=None):
        usd_path = self._resolve_usd(usd_path)
        add_reference_to_stage(usd_path=usd_path, prim_path=prim_path)
        # # create_prim(prim_path, "Xform", usd_path=usd_path)
        # art = SingleArticulation(prim_path=prim_path)
        x,y,z,r,p,yaw = pose
        # # xf = _pose6_to_transform([x,y,z,r,p,yaw])
        # # prim = get_prim_at_path(prim_path)
        # # xform = UsdGeom.Xformable(prim)
        # # # xform.SetXformOps([])
        # # xform.AddTransformOp().Set(xf.GetMatrix())

        art = SingleArticulation(prim_path=prim_path)
        # art.set_world_pose(position=np.array([[0.0, 1.0, 0.0]]) / get_stage_units())
        art.set_world_pose(position=np.array([x,y,z]) / get_stage_units(), 
                           orientation=np.array(euler_angles_to_quat([r,p,yaw])))
        # # if art is None:
        # #     carb.log_error(f"Failed to create articulation at {prim_path}")
        # #     return None
        # # self.scene.add(art)
        # art.initialize()
        if default_joints:
            art.set_joint_position(default_joints)
        return art

    def spawn_rigid(self, usd, prim_path, pose, physics=None, semantics=None, scale=None):
        usd = self._resolve_usd(usd)
        
        create_prim(prim_path, "Xform", usd_path=usd)
        # support pose with named fields
        x = _sample(pose.get("x", 0))
        y = _sample(pose.get("y", 0))
        z = _sample(pose.get("z", 0))
        roll  = _sample(pose.get("roll", 0))
        pitch = _sample(pose.get("pitch", 0))
        yaw   = _sample(pose.get("yaw", 0))
        xf = _pose6_to_transform([_as_float(x), _as_float(y), _as_float(z), roll, pitch, yaw])

        # from isaacsim.core.prims import RigidPrim
        # RigidPrim(prim_paths_expr=prim_path)  # add rigid body schema
        # prim = get_prim_at_path(prim_path)
        
        from isaacsim.core.prims import GeometryPrim
        prim = GeometryPrim(prim_path)
        # the orientations should be quaternion, but here we use euler angles for simplicity
        prim.set_world_poses(positions=np.array([[x,y,z]]) / get_stage_units(), 
                             orientations=np.array([euler_angles_to_quat([roll, pitch, yaw])]))
        # prim.apply_rigid_body_apis()
        prim.apply_collision_apis()
        
        
        # Scale the rigid if specified in the yaml
        if scale is not None:
            if isinstance(scale, (int, float)):
                scale = [scale] * 3
            prim.set_local_scales(np.array([scale]))

        

        prim = get_prim_at_path(prim_path)
        # enable rigid body & material if requested
        if physics:
            # make sure it has rigid body schema
            PhysxSchema.PhysxRigidBodyAPI.Apply(prim)
            # material
            if "material" in physics:
                # quick inline material on prim (optional: create separate material prim)
                mat = physics["material"]
                static_mu  = float(mat.get("static_friction", 0.8))
                dynamic_mu = float(mat.get("dynamic_friction", 0.6))
                restitution = float(mat.get("restitution", 0.0))
                # Approximate via UsdPhysics.MaterialAPI on the prim
                mapi = UsdPhysics.MaterialAPI.Apply(prim)
                mapi.CreateStaticFrictionAttr().Set(static_mu)
                mapi.CreateDynamicFrictionAttr().Set(dynamic_mu)
                mapi.CreateRestitutionAttr().Set(restitution)
        if semantics:
            add_update_semantics(prim_path, semantics)
        # self.scene.add(RigidPrim(prim_path=prim_path))
        return prim_path

    def build(self):
        self.apply_world()
        
        # robot
        r = self.cfg["robot"]
        robot_pose = r.get("pose", [0,0,0, 0,0,0])
        robot = self.spawn_articulation(
            usd_path=r["usd"],
            prim_path=r["prim_path"],
            pose=robot_pose,
            default_joints=r.get("default_joint_positions", None)
        )
        # surfaces
        for s in self.cfg.get("surfaces", []):
            self.spawn_rigid(
                usd=s["usd"],
                prim_path=s["prim_path"],
                pose=s.get("pose", {}),
                physics={"material": {"static_friction": 0.9, "dynamic_friction": 0.7, "restitution": 0.0}},
                semantics=s.get("semantic", None),
                scale=s.get("scale", None),
            )
        
        # props
        for p in self.cfg.get("props", []):
            self.spawn_rigid(
                usd=p["usd"],
                prim_path=p["prim_path"],
                pose=p.get("pose", {}),
                physics=p.get("physics", None),
                semantics=p.get("semantic", None),
                scale=p.get("scale", None),
            )
        self.my_world.reset()
        return None