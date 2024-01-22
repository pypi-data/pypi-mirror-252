from typing import List, Optional, Tuple
from greenstream_config.types import Camera, CameraOverride, GreenstreamConfig, Mode, Variant
import launch
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from math import tan, radians

MODES_TO_OVERRIDE = [Mode.HARDWARE]
ROS_THROTTLE_TIME = 1  # Publish every 1 second
ROS_PUBLISH_TOPIC = "perception/frames"  # eg) /{namespace}/perception/frames/bow or /{namespace}/perception/frames/port
logger = launch.logging.get_logger("gama_greenstream")

def focal_length(sensor_width_mm: float, fov: float):
    return sensor_width_mm / (2 * tan(radians(fov) / 2))

# ------------------------------------------------------

def join_camera_elements(*elements: str):
    return " ! ".join(elements)


def construct_camera_string(camera: Camera, namespace: str) -> str:
    """
    Returns the camera string for a given camera.
    This will add both a webrtcsink and a rosimagesink to the camera.
    """
    webrtc_sink = join_camera_elements(
        "queue",
        f'webrtcsink  meta="meta, name={camera.name}, namespace={namespace}, order={camera.order}"',
    )
    ros_topic = f"{ROS_PUBLISH_TOPIC}/{camera.name}"
    ros_frame_id = f"{namespace}_{camera.name}_{camera.type}_optical_frame"
    throttle_time_ns = int(ROS_THROTTLE_TIME * 1e9)
    ros_sink = join_camera_elements(
        "queue",
        f"rosimagesink ros-topic={ros_topic} ros-name='gst_rosimagesink_{camera.name}' ros-namespace='{namespace}' ros-frame-id='{ros_frame_id}' throttle-time={throttle_time_ns}",
    )
    return join_camera_elements(
        *camera.elements, f"tee name=t t. ! {ros_sink} t. ! {webrtc_sink}"
    )


def merge_cameras(
    cameras: List[Camera], overrides: List[Optional[CameraOverride]]
) -> List[Camera]:
    """
    The gama_vessel may contain camera overrides.
    If it does, we need to merge them with the default cameras.
    """
    overriden_cameras: List[Camera] = cameras
    for idx, override in enumerate(overrides):
        # If override is null/None, we don't want to override the default camera
        if override:
            logger.info(f"Overriding camera {idx} - {override.name}")
            if idx < len(overriden_cameras):
                overriden_cameras[idx] = override

                #applies changes to the camera only if attribute is not None
                Camera(
                    name=override.name or cameras[idx].name,
                    order=override.order or cameras[idx].order,
                    elements=override.elements or cameras[idx].elements,
                    offsets=override.offsets or cameras[idx].offsets,
                    pixel_width=override.pixel_width or cameras[idx].pixel_width,
                    pixel_height=override.pixel_height or cameras[idx].pixel_height,
                    sensor_width_mm=override.sensor_width_mm or cameras[idx].sensor_width_mm,
                    sensor_height_mm=override.sensor_height_mm or cameras[idx].sensor_height_mm,
                    focal_length_mm=override.focal_length_mm or cameras[idx].focal_length_mm,
                    fov=override.fov or cameras[idx].fov,
                    camera_frame_topic=override.camera_frame_topic or cameras[idx].camera_frame_topic,
                    camera_info_topic=override.camera_info_topic or cameras[idx].camera_info_topic,
                    camera_info_ext_topic=override.camera_info_ext_topic or cameras[idx].camera_info_ext_topic,
                    type=override.type or cameras[idx].type,
                )
            #DO NOT ADD NEW CAMERAS ON OVERRRIDE ARRAY IF CAMERA IS NOT ALREADY DEFINED
            # else:
            #     overriden_cameras.append(
            #         Camera(
            #             name=override.name,
            #             order=override.order,
            #             elements=override.elements,
            #             offsets=override.offsets,
            #             pixel_width=override.pixel_width,
            #             pixel_height=override.pixel_height,
            #             sensor_width_mm=override.sensor_width_mm,
            #             sensor_height_mm=override.sensor_height_mm,
            #             focal_length_mm=override.focal_length_mm,
            #             fov=override.fov,
            #             camera_frame_topic=override.camera_frame_topic,
            #             camera_info_topic=override.camera_info_topic,
            #             camera_info_ext_topic=override.camera_info_ext_topic,
            #             type=override.type,
            #         ))

    return overriden_cameras


def get_cameras(config: GreenstreamConfig) -> List[Camera]:
    """
    Returns the cameras for the current vessel configuration.
    """
    cameras = config.cameras
    if not cameras:
        raise Exception(
            f"Could not find camera configuration for mode {config.mode} and variant {config.variant}"
        )
    if config.camera_overrides:
        if config.mode in MODES_TO_OVERRIDE:
            return merge_cameras(cameras, config.camera_overrides)
        else:
            logger.warn(
                f"camera overrides are only supported in {', '.join([item.value for item in MODES_TO_OVERRIDE])} mode"
            )

    return cameras



def generate_greenstream_launch_description(config: GreenstreamConfig):
    logger.info("Starting greenstream....")

    camera_processes: List[ExecuteProcess] = []
    cameras = get_cameras(config)
    
    #create camera nodes to publish to
    camera_node = List[Node]
    for idx, camera in enumerate(cameras):
        camera_str = construct_camera_string(camera, config.namespace_vessel)

        logger.info(f"Camera: {camera.name}")
        logger.info(f"Camera {idx}: {camera_str}")

        camera_node.append(Node(
            name=f"camera_{camera.name}",
            package="camera_info",
            executable="camera_info_node",
            parameters=[
                {
                    "use_sim_time": LaunchConfiguration("use_sim_time"),
                    "frame_id": f"{config.namespace_vessel}_{camera.name}_{camera.type}_optical_frame",
                    "focal_length_mm": focal_length(camera.sensor_width_mm, camera.fov),
                    "sensor_width_mm": camera.sensor_width_mm,
                    "sensor_height_mm": camera.sensor_height_mm,
                    "pixel_width": camera.pixel_width,
                    "pixel_height": camera.pixel_height,
                }
            ],
            remappings=[
                ("camera_info", f"{camera.camera_info_topic}"),
                ("camera_info_ext", f"{camera.camera_info_ext_topic}"),
                ("camera_frame", f"{camera.camera_frame_topic}")
            ],
            ros_arguments=["--log-level", LaunchConfiguration("log_level")],
            output="both",
        ))

        camera_processes.append(
            ExecuteProcess(
                name=f"greenstream-camera-{idx}",
                cmd=["greenstream", "camera", camera_str],
                output="screen",
            )
        )

    return launch.LaunchDescription(
        [
            ExecuteProcess(
                name="greenstream-ui", cmd=["greenstream", "ui", "--port", f"{config.ui_port}"], output="screen"
            ),
            ExecuteProcess(
                name="greenstream-signalling",
                cmd=["greenstream", "signalling", "--port", f"{config.signalling_server_port}"],
                output="screen",
            ),
            *camera_processes,
            *camera_node,
        ]
    )