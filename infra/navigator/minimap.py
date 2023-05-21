import cv2
import mss
import numpy as np

from infra.vision.opencv import opencv


def Screen_Shot(left=0, top=0, width=1920, height=1080):
    stc = mss.mss()
    scr = stc.grab({"left": left, "top": top, "width": width, "height": height})
    stc.close()
    img = np.array(scr)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert to RGB color space

    return img


# Load the image
image = Screen_Shot(0, 0, 1920, 1080)

# Define the points of the rhombic shape
points = np.array([(1550, 910), (1710, 795), (1880, 910), (1720, 1020)])

# Create a binary mask with the rhombic shape
mask = np.zeros(image.shape[:2], dtype=np.uint8)
cv2.fillPoly(mask, [points], 255)

# Apply the mask to the image
masked_image = cv2.bitwise_and(image, image, mask=mask)

# Crop out the minimap region
minimap = masked_image[
    min(points[:, 1]) : max(points[:, 1]), min(points[:, 0]) : max(points[:, 0])
]

# Resize the minimap to 640x640
minimap = cv2.resize(minimap, None, fx=5, fy=5)
minimap = opencv.cvt_img_rgb(minimap)

# Display the results
cv2.imshow("Resized MiniMap", minimap)
cv2.waitKey(0)
cv2.destroyAllWindows()
