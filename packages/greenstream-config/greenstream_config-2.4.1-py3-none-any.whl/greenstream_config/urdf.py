from typing import List, Tuple

from urchin import Joint, Link, xyz_rpy_to_matrix

from greenstream_config.types import Camera, GreenstreamConfig
from greenstream_config.generate_greenstream_launch_description import merge_cameras

def get_camera_urdf(camera: Camera, mode : str) -> Tuple[List[Link], List[Joint]]:
    # This is the camera urdf from the gama/lookout greenstream.launch.py
    # We need to generate this from the camera config
    links = List[Link]
    joints = List[Joint]

    camera_xyz_rpy = [camera.offsets.forward, camera.offsets.left, camera.offsets.up, 
                      camera.offsets.roll, camera.offsets.pitch, camera.offsets.yaw]

    links.append(Link(name=f"{camera.name}_link", inertial=None, visuals=None, collisions=None))
    joints.append(Joint(name=f"{camera.name}_joint", parent="base_link", child=f"{camera.name}_link",
                    joint_type="fixed", origin=xyz_rpy_to_matrix(camera_xyz_rpy)))
    
    if mode != 'hardware':
        links.append(Link(name=f"{camera.name}_{camera.type}_frame", inertial=None, visuals=None, collisions=None))
        links.append(Link(name=f"{camera.name}_{camera.type}_optical_frame", inertial=None, visuals=None, collisions=None))

        #fixed transforms between camera frame and optical frame FRD -> NED
        joints.append(Joint(name=f"{camera.name}_link_to_{camera.type}_frame", parent=f"{camera.name}_link", child=f"{camera.name}_{camera.type}_frame",
                        joint_type="fixed", origin=xyz_rpy_to_matrix([0, 0, 0, 0, 0, 0])))
        joints.append(Joint(name=f"{camera.name}_{camera.type}_frame_to_optical_frame", parent=f"{camera.name}_{camera.type}_frame", child=f"{camera.name}_{camera.type}_optical_frame",
                        joint_type="fixed", origin=xyz_rpy_to_matrix([0, 0, 0, -1.570796, 0, -1.570796])))

    return (links, joints)


def get_cameras_urdf(cameras: List[Camera], config : GreenstreamConfig) -> Tuple[List[Link], List[Joint]]:

    links = List[Link]
    joints = List[Joint]
    cameras = merge_cameras(cameras, config.camera_overrides)

    #assume cameras have already been merged with overrides
    for camera in cameras:

        camera_links, camera_joints = get_camera_urdf(camera, config.mode)
        links += camera_links
        joints += camera_joints
        
    return links, joints

