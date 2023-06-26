from core.common.entities import Img, Pixel, Polygon, Rect


def map_crop() -> Polygon:
    origin = Pixel(962, 585)
    radius = Pixel(560, 420)
    region = Polygon(
        points=[
            Pixel(origin.x - radius.x, origin.y),
            Pixel(origin.x, origin.y - radius.y),
            Pixel(origin.x + radius.x, origin.y),
            Pixel(origin.x, origin.y + radius.y),
        ]
    )
    return region


def minimap_crop() -> Rect:
    origin = Pixel(1710, 910)
    radius = 65
    region = Rect(
        left_top=Pixel(origin.x - radius, origin.y - radius),
        right_bottom=Pixel(origin.x + radius, origin.y + radius),
    )
    return region


def extract_map(img: Img, save_path: str = "") -> Img:
    save_path = save_path or "albion/maps/map.png"
    img.crop(map_crop())
    img.save(save_path)
    return img


def extract_minimap(img: Img, save_path: str = "") -> Img:
    save_path = save_path or "albion/temp/minimap.png"
    img.crop(minimap_crop())
    img.save(save_path)
    return img
