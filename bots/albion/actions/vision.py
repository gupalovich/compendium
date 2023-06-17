from core.common.entities import ImgLoader, Pixel, Rect
from core.display.vision import Vision

crop_areas = {
    "skill_panel": Rect(Pixel(480, 975), Pixel(1475, 1065)),
}
ref_images = {
    "mount_hp": ImgLoader("albion/ui/mount_hp.png", 0.95),
}


class ServiceVision(Vision):
    """Base class for service vision, which inherits from Vision. Used by bot services."""


class MountVision(ServiceVision):
    """Vision for mounts."""
