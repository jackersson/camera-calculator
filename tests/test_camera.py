import math
from camera.utils import *

# GT
TOLERANCE = 0.1 # almost equals value tolerance

AOV_HORIZONTAL_GT = 43.6  # degrees
FOV_HORIZONTAL_GT = 7.68  # m

AOV_VERTICAL_GT = 25.4  # degrees
FOV_VERTICAL_GT = 4.32  # m

PIXEL_DENSITY = 250 # px/m
MOTION_BLUR = 69.4 # pixels

# Params
FOCAL_LENGTH = 6 # mm
EXPOSURE_TIME = 1 / 30 # s
SENSOR_W, SENSOR_H = 4.8, 3.6 # (mm, mm)

OBJECT_SPEED = km_h_to_mm_s(30) # mm / s
DISTANCE_TO_SCENE = m_to_mm(9.6) # mm

FRAME_WIDTH, FRAME_HEIGHT = 1920, 1080 # pixels


def test_utils():
    aov_horizontal = aov(SENSOR_W, FOCAL_LENGTH)
    # print(f"AOV Horizontal {aov_horizontal} (degrees)")
    assert math.isclose(aov_horizontal, AOV_HORIZONTAL_GT, abs_tol=TOLERANCE), aov_horizontal

    fov_horizontal = fov(aov_horizontal, DISTANCE_TO_SCENE)
    # print(f"FOV Horizontal {fov_horizontal} (mm)")
    # print(f"FOV Horizontal {mm_to_m(fov_horizontal)} (m)")
    assert math.isclose(mm_to_m(fov_horizontal), FOV_HORIZONTAL_GT, abs_tol=TOLERANCE), mm_to_m(fov_horizontal)

    aov_vertical = aov_vertical_wrt_frame_size(aov_horizontal, FRAME_WIDTH, FRAME_HEIGHT)
    # print(f"AOV Vertical {aov_vertical} (degrees)")
    assert math.isclose(aov_vertical, AOV_VERTICAL_GT, abs_tol=TOLERANCE), aov_vertical

    fov_vertical = fov_vertical_wrt_frame_size(fov_horizontal, FRAME_WIDTH, FRAME_HEIGHT)
    # print(f"FOV Vertical {fov_vertical} (mm)")
    # print(f"FOV Vertical {mm_to_m(fov_vertical)} (m)")

    fov_vertical_check = fov(aov_vertical, DISTANCE_TO_SCENE)
    assert math.isclose(fov_vertical, fov_vertical_check, abs_tol=TOLERANCE), "{} != {}".format(fov_vertical, fov_vertical_check)
    assert math.isclose(mm_to_m(fov_vertical), FOV_VERTICAL_GT, abs_tol=TOLERANCE), mm_to_m(fov_vertical)


def test_camera():
    camera = Camera(focal_length=FOCAL_LENGTH,
                    sensor_shape=(SENSOR_W, SENSOR_H),
                    frame_shape=(FRAME_WIDTH, FRAME_HEIGHT))
    assert math.isclose(camera.aov_horizontal, AOV_HORIZONTAL_GT, abs_tol=TOLERANCE), camera.aov_horizontal
    assert math.isclose(camera.aov_vertical, AOV_VERTICAL_GT, abs_tol=TOLERANCE), camera.aov_vertical

    pix_density, _ = camera.get_pixel_density(DISTANCE_TO_SCENE)
    pix_density = px_mm_to_px_m(pix_density)
    assert math.isclose(pix_density, PIXEL_DENSITY, abs_tol=TOLERANCE), pix_density

    fov_w, fov_h = camera.get_fov(DISTANCE_TO_SCENE)
    assert math.isclose(mm_to_m(fov_w), FOV_HORIZONTAL_GT, abs_tol=TOLERANCE), mm_to_m(fov_w)
    assert math.isclose(mm_to_m(fov_h), FOV_VERTICAL_GT, abs_tol=TOLERANCE), mm_to_m(fov_h)

    mblur = camera.get_motion_blur(DISTANCE_TO_SCENE, OBJECT_SPEED)
    assert math.isclose(mblur, MOTION_BLUR, abs_tol=TOLERANCE), mm_to_m(fov_h)