
import math

from typing import Tuple


def km_h_to_mm_s(value: int) -> float:
    """
        Converts km/h to mm/s
    """
    return (value * 10**6) / 3600

def m_to_mm(value: int) -> int:
    """
        Converts m to mm
    """
    return value * 10**3

def mm_to_m(value: int) -> float:
    """
        Converts mm to m
    """
    return value / 10**3

def px_mm_to_px_m(value: float):
    """
        Converts pixel/mm to pixel/m
    """
    return value * 10**3

def motion_blur_pixels(object_speed: float, exposure_time: float,
                       frame_side_size: int, scene_side_size: float) -> int:
    """
    Calculate motion blur in pixels given object speed, exposute time,
        frace_size_size (W or H), scene_side_size (W or H)
    Arguments:
        object_speed: mm/s
        exposure_time: s
        frame_side_size: pixels
        scene_side_size: mm

    Returns:
        value: pixels
    """
    return object_speed * exposure_time * (frame_side_size / scene_side_size)



def aov(sensor_size_size: float, focal_length: float) -> float:
    """
    Calculate angle of view in degrees

    Arguments:
        sensor_size_size: mm
        focal_lenght: mm

    Returns:
        fov: degrees
    """
    return 2 * math.degrees(math.atan(sensor_size_size / (2 * focal_length)))


def fov(aov: float, distance_to_scene: float) -> float:
    """
    Calculate Field of View (mm)
    Arguments:
        aov: degrees
        distance_to_scene: mm

    Returns:
        fov: mm
    """
    return 2 * (math.tan(math.radians(aov) / 2) * distance_to_scene)


# http://hugin.sourceforge.net/docs/manual/Field_of_View.html
def aov_vertical_wrt_frame_size(aov_horizontal: float, frame_width: int, frame_height: int) -> float:
    """
        Calculates Angle of View wrt to frame size (pixels)
    Arguments:
        aov_horizontal: degrees
        frame_width: pixels
        frame_height: pixels

    Returns:
        angle: degrees
    """
    aspect_ratio = frame_height / frame_width
    angle = math.tan(math.radians(aov_horizontal / 2))
    return 2 * math.degrees(math.atan(angle * aspect_ratio))

# fov_vertical_wrt_frame_size
def fov_vertical_wrt_frame_size(fov_horizontal: float, frame_width: int, frame_height: int) -> float:
    """
        Calculates Field of View wrt to frame size

    Arguments:
        fov_horizontal: degrees
        frame_width: pixels
        frame_heigth: pixels

    Returns:
        angle: degrees
    """
    return fov_horizontal * (frame_height / frame_width)


def fov_horizontal_wrt_frame_size(fov_vertical: float, frame_width: int, frame_height: int):
    """
        Calculates Field of View wrt to frame size

    Arguments:
        fov_horizontal: degrees
        frame_width: pixels
        frame_heigth: pixels

    Returns:
        angle: degrees
    """
    return fov_vertical * (frame_width / frame_height)


def pixel_density(frame_side_size: int, fov_side_size: float) -> float:
    """
    Returns how many pixels in 1 mm
    Arguments:
        frame_side_size: pixels
        fov_side_size: mm
    """
    return frame_side_size / fov_side_size



def scene_size(distance: float, sensor_side_size: float, focal_length: float) -> float:
    """
    Calculates scene size in mm
    Arguments:
        distance: mm
        sensor_side_size: mm
        focal_length: mm

    Returns:
        scene_size: mm
    """

    return (distance * sensor_side_size) / focal_length


class Camera:

    def __init__(self, focal_length: float, sensor_shape: Tuple[int, int],
                 frame_shape: Tuple[int, int], exposure_time: float = 1/30):
        self.focal_length = focal_length
        self.exposure_time = exposure_time
        self.sensor_shape = sensor_shape
        self.frame_shape = frame_shape

    @property
    def aov_horizontal(self):
        return aov(self.sensor_shape[0], self.focal_length)

    @property
    def aov_vertical(self):
        frame_w, frame_h = self.frame_shape
        return aov_vertical_wrt_frame_size(self.aov_horizontal, frame_w, frame_h) # aov(self.sensor_shape[0], self.focal_length)

    def get_fov(self, distance: float) -> Tuple[float, float]:
        """
        Arguments:
            distance: mm  # m, mm, cm

        Returns:
            fov_horizontal: degrees
            fov_vertial: degrees

        """
        fov_horizontal = fov(self.aov_horizontal, distance)
        fov_vertical = fov(self.aov_vertical, distance)
        return fov_horizontal, fov_vertical

    def get_motion_blur(self, distance: float, object_speed: float) -> int:
        """
        Arguments:
            distance: mm
            object_speed: mm / s
        Returns:
            motion_blur: pixels
        """
        sensor_w, sensor_h = self.sensor_shape
        frame_w, frame_h = self.frame_shape

        aov_horizontal = aov(sensor_w, self.focal_length)
        fov_horizontal = fov(aov_horizontal, distance)

        aov_vertical = aov_vertical_wrt_frame_size(aov_horizontal, frame_w, frame_h)
        fov_vertical = fov(aov_vertical, distance)

        return motion_blur_pixels(object_speed, self.exposure_time, frame_h, fov_vertical)

    def get_pixel_density(self, distance: float):
        """
        Arguments:
            distance: mm
        Returns:
            vertical_pd: pixels (vertical_pixel_density)
            horizontal_pd: pixels (horizontal_pixel_density)
        """

        fov_horizontal, fov_vertical = self.get_fov(distance)

        frame_w, frame_h = self.frame_shape
        vertical_pd = pixel_density(frame_h, fov_vertical)
        horizontal_pd = pixel_density(frame_w, fov_horizontal)

        return vertical_pd, horizontal_pd