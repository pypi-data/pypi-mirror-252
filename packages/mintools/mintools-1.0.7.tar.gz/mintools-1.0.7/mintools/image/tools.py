import cv2
import numpy as np


def mask2color(mask, colorList):
    """
    :param mask: 2D array, each pixel is a class index
    :param colorList: list of color, such as [[255,0,0], [0,255,0]] in BGR format
    """
    max_value = np.max(mask)
    src_color = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    for i in range(1, 1 + max_value):
        src_color[np.where(mask == i)] = colorList[i - 1]
    return src_color

# if __name__ == '__main__':
#     aa = get_image_names(path, base_path=path)
#     bb = 0
