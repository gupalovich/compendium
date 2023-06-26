from time import sleep

from core.common.entities import Pixel, Rect


def find_closest(origin: Pixel, positions: list[Pixel] | list[Rect]) -> Pixel:
    """Find the closest position to the origin"""
    min_dist = float("inf")
    closest_pos = None

    for pos in positions:
        if isinstance(pos, Rect):
            pos = pos.center

        dist = abs(abs(origin) - abs(pos))
        if dist < min_dist:
            min_dist = dist
            closest_pos = pos
    return closest_pos


def log(task: str, delay: float = 0):
    print(f"- {task}")
    if delay:
        sleep(delay)
