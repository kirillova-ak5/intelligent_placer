# This is a sample Python script.

# Press Ctrl+F5 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# plan
# detect objs on imag
#     binarize imag(ui)
#     findConturs on mask (1obj = 1 contur)
#     for each contur
#         find AABB
#         create AABB-sized texture
#         in contur & in mask -> tru
#         else false

# detect drown polygon
#     user choose
#     colorpiker
#     hough

# place
# for object
#     for angle 0 - 2 pi
#         for translate_x 0 - imag_max
#             for translate_y 0 - imag_max
#                 transform = transform(angle, translate)
#                 add transformed imag into try_mask

import os
import numpy as np
import imageio
from skimage.transform import resize
from skimage.color import rgb2gray
from matplotlib import pyplot as plt
from scipy.ndimage.morphology import binary_fill_holes
from skimage.morphology import binary_closing
from skimage.color import label2rgb
from skimage.feature import canny
from skimage import measure
import cv2 as cv
import random as rng

## Rotation of countours start
def cart2pol(x, y):
    theta = np.arctan2(y, x)
    rho = np.hypot(x, y)
    return theta, rho


def pol2cart(theta, rho):
    x = rho * np.cos(theta)
    y = rho * np.sin(theta)
    return x, y


def rotate_contour(cnt, angle, center, img_size):
    M = cv.moments(cnt)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])

    cnt_norm = cnt - [cx, cy]

    coordinates = cnt_norm[:, 0, :]
    xs, ys = coordinates[:, 0], coordinates[:, 1]
    thetas, rhos = cart2pol(xs, ys)

    thetas = np.rad2deg(thetas)
    thetas = (thetas + angle) % 360
    thetas = np.deg2rad(thetas)

    xs, ys = pol2cart(thetas, rhos)

    cnt_norm[:, 0, 0] = xs
    cnt_norm[:, 0, 1] = ys

    cnt_rotated = cnt_norm + [img_size[0] / 2, img_size[1] / 2]
    cnt_rotated = cnt_rotated.astype(np.int32)

    return cnt_rotated
# Rotation of countours


ref_objects = []
ref_bin_objects = []

def load_ref_objects(path, is_low = False):
    global ref_objects
    if is_low and os.path.isdir(path + "/low"):
        ref_objects = [imageio.imread(path + "/low/" + fname) for fname in os.listdir(path+"/low") if fname.endswith(".jpg")]
        return
    ref_objects = [imageio.imread(path + "/" + fname) for fname in os.listdir(path) if fname.endswith(".jpg")]
    ref_objects = ref_objects[1:12]
    if is_low:
        ref_objects = [resize(t, (256, 256 * t.shape[1] / t.shape[0])) for t in ref_objects]
        ref_objects = [t[0 : t.shape[0] - 0, 0 : t.shape[1] - 0] for t in ref_objects]
        os.mkdir(path+"/low")
        for i in range(len(ref_objects)):
            imageio.imwrite(path + "/low/" + str(i) + ".jpg",ref_objects[i])

def cv2_image_from_imageio(img):
    return (img * 255).astype(np.uint8)

def binarize(image):
    gray = rgb2gray(image)
    my_edge_map = binary_closing(canny(gray, sigma=0.4), selem=np.ones((3, 3)))
    my_edge_segmentation = binary_fill_holes(my_edge_map)

    return cv2_image_from_imageio(my_edge_segmentation)


def check_place(placement: np.ndarray):
    err_cnt = 0
    for el in placement.flat:
        if el > 255:
            err_cnt += 1
            if err_cnt > placement.shape[0] * placement.shape[1] / 5000:
                return False
    return True


def try_place(destination: np.ndarray, objects, idx):
    trans = [0, 0]
    object = objects[idx]
    rows, cols = object.shape

    print("new try")

    for angle in range(180):
        print(angle)
        for half_trans_y in range(destination.shape[0] // 2):
            for half_trans_x in range(destination.shape[1] // 2):
                trans_y = 2 * half_trans_y
                trans_x = 2 * half_trans_x
                M = cv.getRotationMatrix2D(((cols - 1) / 2.0, (rows - 1) / 2.0), angle * 2, 1)
                rotated_object = cv.warpAffine(object, M, (cols, rows))
                copy = np.ones(shape = (destination.shape[0] + 2 * object.shape[0], destination.shape[1] + 2 * object.shape[1])) * 255
                copy[object.shape[0]:object.shape[0] + destination.shape[0], object.shape[1]:object.shape[1] + destination.shape[1]] = destination
                copy[trans_y + object.shape[0]:trans_y + 2 * object.shape[0],
                trans_x + rotated_object.shape[1]:trans_x + 2 * rotated_object.shape[1]] \
                    += rotated_object
                if check_place(copy):
                    if idx == len(objects) - 1:
                        return copy
                    else:
                        rez = try_place(copy, objects, idx + 1)
                        if rez is not None:
                            return rez
    return None


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #load objects
    load_ref_objects("../item_set", True)

    #find objects
    ref_bin_objects = [binarize(t) for t in ref_objects]

    image = imageio.imread("../item_set/low/" + "2.jpg")
    img = binarize(image)
    cv.imshow('binarisation', img)


    #    for img in ref_bin_objects:
#        plt.imshow(img)
#        plt.figure()
#    plt.show()
    contours, hierarchy = cv.findContours(img, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    contours_filtered = []

    #for cnt in contours:
    #    contours_filtered.append(cnt)
    # Draw contours
    drawing = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    rects = []
    max_area_idx = 0
    max_area = cv.contourArea(contours[0])
    for i in range(len(contours)):
        ariea = cv.contourArea(contours[i])
        if hierarchy[0][i][3] != -1 or ariea <= 200:
            continue
        if ariea > max_area:
            max_area, max_area_idx = ariea, len(rects)

        contours_filtered.append(contours[i])
        rects.append(cv.minAreaRect(contours[i]))
        color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
        cv.drawContours(drawing, contours, i, color, 2, cv.LINE_8, hierarchy, 0)
        box = cv.boxPoints(rects[-1])
        box = np.int0(box)
        cv.drawContours(drawing, [box], 0, (0, 0, 255), 2)

    # Show in a window
    #rect[i] = ((rect[i][0][0], rect[i][0][1]), )
    cv.imshow('Contours', drawing)

    textures = []
    for rec in rects:
        textures.append(np.zeros((int(rec[1][1]), int(rec[1][0]))).astype(np.uint8))
        rotated_cnt = contours_filtered[len(textures) - 1]
        rotated_cnt = rotate_contour(rotated_cnt, -rec[2], rec[0], rec[1])
        cv.fillPoly(textures[-1], pts=[rotated_cnt], color=(255, 255, 255))

    polygon = textures.pop(max_area_idx)
    polygon = (255 - polygon)
    cv.imshow("poly", polygon)

    placement = polygon
    i = 0
    placement = try_place(placement, textures, 0)
#    cv.imshow("placement {idx}".format(idx=i), placement)
    if placement is None:
        print("cannot")

    if placement is not None:
        cv.imshow("placement", placement)
    cv.waitKey()



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
