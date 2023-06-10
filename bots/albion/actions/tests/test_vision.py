# from core.vision.utils import load_img

# from ..vision import find_mount, find_skill


# def test_find_mount():
#     search_img = load_img("albion/tests/3.png")
#     result = find_mount(search_img)
#     assert len(result) == 1


# def test_find_mount_half_hp():
#     search_img = load_img("albion/tests/2.png")
#     result = find_mount(search_img)
#     assert len(result) == 1


# def test_find_skill_teleport():
#     search_img = load_img("albion/tests/5.png")
#     result = find_skill(search_img, "town_teleport")
#     assert len(result) == 1


# def test_find_skill_teleport_with_no_result():
#     search_img = load_img("albion/tests/3.png")
#     result = find_skill(search_img, "town_teleport")
#     assert len(result) == 0
