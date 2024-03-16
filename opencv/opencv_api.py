# 一些常用的opencv方法封装

import cv2
import numpy as np
from scipy import ndimage
from skimage import transform as tf
from skimage import filters
from skimage import measure
from skimage import feature
from skimage import segmentation


class OpencvApi(object):
    def __init__(self):
        pass

    # 读取图片
    def read_img(self, img_path):
        img = cv2.imread(img_path)
        return img

    # 保存图片
    def save_img(self, img, save_path):
        cv2.imwrite(save_path, img)

    # 显示图片
    def show_img(self, img, title="img"):
        cv2.imshow(title, img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # 图片缩放
    def resize_img(self, img, scale):
        img = cv2.resize(img, (int(img.shape[1] * scale), int(img.shape[0] * scale)))
        return img

    # 图片旋转
    def rotate_img(self, img, angle, center=None, scale=1.0):
        (h, w) = img.shape[:2]
        if center is None:
            center = (w // 2, h // 2)
        # 旋转矩阵
        M = cv2.getRotationMatrix2D(center, angle, scale)
        # 旋转
        img = cv2.warpAffine(img, M, (w, h))
        return img

    # 图片平移
    def translate_img(self, img, x, y):
        M = np.float32([[1, 0, x], [0, 1, y]])
        img = cv2.warpAffine(img, M, (img.shape[1], img.shape[0]))
        return img

    # 图片翻转
    def flip_img(self, img, flip_code):
        img = cv2.flip(img, flip_code)
        return img

    # 图片膨胀
    def dilate_img(self, img, kernel_size):
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        img = cv2.dilate(img, kernel, iterations=1)
        return img

    # 图片腐蚀
    def erode_img(self, img, kernel_size):
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        img = cv2.erode(img, kernel, iterations=1)
        return img

    # 图片开运算
    def opening_img(self, img, kernel_size):
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
        return img

    # 图片闭运算
    def closing_img(self, img, kernel_size):
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
        return img

    # 图片形态学梯度
    def morphology_gradient_img(self, img, kernel_size):
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        img = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel)
        return img

    # 图片顶帽
    def tophat_img(self, img, kernel_size):
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        img = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel)
        return img

    # 图片黑帽
    def blackhat_img(self, img, kernel_size):
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        img = cv2.morphologyEx(img, cv2.MORPH_BLACKHAT, kernel)
        return img

    # 图片边缘检测
    def canny_img(self, img, threshold1, threshold2):
        img = cv2.Canny(img, threshold1, threshold2)
        return img

    # 图片轮廓检测
    def findContours_img(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img, contours, hierarchy = cv2.findContours(
            img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )
        return img, contours, hierarchy

    # 图片轮廓绘制
    def drawContours_img(self, img, contours, contourIdx, color, thickness):
        img = cv2.drawContours(img, contours, contourIdx, color, thickness)
        return img

    # 图片轮廓面积
    def contourArea_img(self, contours, contourIdx):
        area = cv2.contourArea(contours[contourIdx])
        return area

    # 图片轮廓周长
    def arcLength_img(self, contours, contourIdx):
        perimeter = cv2.arcLength(contours[contourIdx], True)
        return perimeter

    # 图片轮廓近似
    def approxPolyDP_img(self, contours, contourIdx, epsilon):
        approx = cv2.approxPolyDP(contours[contourIdx], epsilon, True)
        return approx

    # 图片轮廓凸包
    def convexHull_img(self, contours, contourIdx):
        hull = cv2.convexHull(contours[contourIdx])
        return hull

    # 图片轮廓凸缺陷
    def convexityDefects_img(self, contours, contourIdx):
        hull = cv2.convexHull(contours[contourIdx], returnPoints=False)
        defects = cv2.convexityDefects(contours[contourIdx], hull)
        return defects

    # 图片轮廓各种外接图形 0-矩形 1-圆形 2-三角形 3-椭圆形 4-直线
    def bounding_img(self, contours, contourIdx, boundingType):
        if boundingType == 0:
            x, y, w, h = cv2.boundingRect(contours[contourIdx])
            return x, y, w, h
        elif boundingType == 1:
            (x, y), radius = cv2.minEnclosingCircle(contours[contourIdx])
            return (x, y), radius
        elif boundingType == 2:
            triangle = cv2.minEnclosingTriangle(contours[contourIdx])
            return triangle
        elif boundingType == 3:
            ellipse = cv2.fitEllipse(contours[contourIdx])
            return ellipse
        elif boundingType == 4:
            [vx, vy, x, y] = cv2.fitLine(
                contours[contourIdx], cv2.DIST_L2, 0, 0.01, 0.01
            )
            return [vx, vy, x, y]

    # 图片直方图均衡化
    def equalizeHist_img(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.equalizeHist(img)
        return img

    # 图片直方图
    def calcHist_img(self, img, channels, mask, histSize, ranges):
        hist = cv2.calcHist([img], channels, mask, histSize, ranges)
        return hist

    # 图片直方图反向投影
    def calcBackProject_img(self, img, channels, hist, ranges, scale):
        backProject = cv2.calcBackProject([img], channels, hist, ranges, scale)
        return backProject

    # 图片直方图比较
    def compareHist_img(self, hist1, hist2, method):
        similarity = cv2.compareHist(hist1, hist2, method)
        return similarity

    # 图片模板匹配
    def matchTemplate_img(self, img, template, method):
        result = cv2.matchTemplate(img, template, method)
        return result

    # 图片模板匹配最大值
    def minMaxLoc_img(self, result):
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)
        return minVal, maxVal, minLoc, maxLoc

    # 图片阈值分割
    def threshold_img(self, img, thresh, maxval, type):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, img = cv2.threshold(img, thresh, maxval, type)
        return img

    # 图片自适应阈值分割
    def adaptiveThreshold_img(
        self, img, maxValue, adaptiveMethod, thresholdType, blockSize, C
    ):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.adaptiveThreshold(
            img, maxValue, adaptiveMethod, thresholdType, blockSize, C
        )
        return img

    # 图片各种阈值分割 Otsu、Yen、Li、Isodata、Triangle、Mean、Minimum、Maximum、Percentile、Local、Niblack、Sauvola、Wolf、Nick、Bradley、Adaptive
    def threshold_img(self, img, method, block_size, offset):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if method == "Otsu":
            img = filters.threshold_otsu(img)
        elif method == "Yen":
            img = filters.threshold_yen(img)
        elif method == "Li":
            img = filters.threshold_li(img)
        elif method == "Isodata":
            img = filters.threshold_isodata(img)
        elif method == "Triangle":
            img = filters.threshold_triangle(img)
        elif method == "Mean":
            img = filters.threshold_mean(img)
        elif method == "Minimum":
            img = filters.threshold_minimum(img)
        elif method == "Maximum":
            img = filters.threshold_maximum(img)
        elif method == "Percentile":
            img = filters.threshold_percentile(img)
        elif method == "Local":
            img = filters.threshold_local(img, block_size)
        elif method == "Niblack":
            img = filters.threshold_niblack(img, window_size=block_size, k=offset)
        elif method == "Sauvola":
            img = filters.threshold_sauvola(img, window_size=block_size, k=offset)
        elif method == "Wolf":
            img = filters.threshold_wolf(img, window_size=block_size, k=offset)
        elif method == "Nick":
            img = filters.threshold_nick(img, window_size=block_size, k=offset)
        elif method == "Bradley":
            img = filters.threshold_bradley(img, window_size=block_size, k=offset)
        elif method == "Adaptive":
            img = filters.threshold_adaptive(img, block_size, offset)
        return img

    # 图片分水岭分割
    def watershed_img(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        distance = ndimage.distance_transform_edt(img)
        local_maxi = feature.peak_local_max(
            distance, indices=False, footprint=np.ones((3, 3)), labels=img
        )
        markers = measure.label(local_maxi)
        labels_ws = segmentation.watershed(-distance, markers, mask=img)
        return labels_ws


def main():
    opencv_api = OpencvApi()
    img = opencv_api.read_img("test.jpg")
    opencv_api.show_img(img)
    img = opencv_api.resize_img(img, 0.5)
    opencv_api.show_img(img)
    img = opencv_api.rotate_img(img, 45)
    opencv_api.show_img(img)
    img = opencv_api.translate_img(img, 100, 100)
    opencv_api.show_img(img)
    img = opencv_api.flip_img(img, 0)
    opencv_api.show_img(img)
    img = opencv_api.dilate_img(img, 3)
    opencv_api.show_img(img)
    img = opencv_api.erode_img(img, 3)
    opencv_api.show_img(img)
    img = opencv_api.opening_img(img, 3)
    opencv_api.show_img(img)
    img = opencv_api.closing_img(img, 3)
    opencv_api.show_img(img)
    img = opencv_api.morphology_gradient_img(img, 3)
    opencv_api.show_img(img)
    img = opencv_api.tophat_img(img, 3)
    opencv_api.show_img(img)
    img = opencv_api.blackhat_img(img, 3)
    opencv_api.show_img(img)
    img = opencv_api.canny_img(img, 100, 200)
    opencv_api.show_img(img)
    img, contours, hierarchy = opencv_api.findContours_img(img)
    opencv_api.show_img(img)
    img = opencv_api.drawContours_img(img, contours, 0, (0, 0, 255), 3)
    opencv_api.show_img(img)
    area = opencv_api.contourArea_img(contours, 0)
    print("area:", area)  # 0.0
    perimeter = opencv_api.arcLength_img(contours, 0)
    print("perimeter:", perimeter)  # 0.0
    approx = opencv_api.approxPolyDP_img(contours, 0, 0.01)
    print("approx:", approx)  # [[[0 0]]]
    hull = opencv_api.convexHull_img(contours, 0)
    print("hull:", hull)  # [[[0 0]]]
    defects = opencv_api.convexityDefects_img(contours, 0)
    print("defects:", defects)  # "None
    x, y, w, h = opencv_api.bounding_img(contours, 0, 0)
    print("x, y, w, h:", x, y, w, h)  # "0 0 0 0
    (x, y), radius = opencv_api.bounding_img(contours, 0, 1)
    print("x, y, radius:", x, y, radius)  # "0.0 0.0 0.0
    triangle = opencv_api.bounding_img(contours, 0, 2)
    print("triangle:", triangle)  # "None
    ellipse = opencv_api.bounding_img(contours, 0, 3)
    print("ellipse:", ellipse)  # "None
    [vx, vy, x, y] = opencv_api.bounding_img(contours, 0, 4)
    print("vx, vy, x, y:", vx, vy, x, y)  # "0.0 0.0 0.0 0.0
    img = opencv_api.equalizeHist_img(img)
    opencv_api.show_img(img)
    hist = opencv_api.calcHist_img(img, [0], None, [256], [0, 256])
    print("hist:", hist)  # "[[0.]]
    backProject = opencv_api.calcBackProject_img(img, [0], hist, [0, 256], 1.0)
    print("backProject:", backProject)  # "[[0.]]
    similarity = opencv_api.compareHist_img(hist, hist, 0)
    print("similarity:", similarity)  # "1.0
    result = opencv_api.matchTemplate_img(img, img, 0)
    print("result:", result)  # "[[0.]]
    minVal, maxVal, minLoc, maxLoc = opencv_api.minMaxLoc_img(result)
    print(
        "minVal, maxVal, minLoc, maxLoc:", minVal, maxVal, minLoc, maxLoc
    )  # "0.0 0.0 (0, 0) (0, 0)
    img = opencv_api.threshold_img(img, 127, 255, cv2.THRESH_BINARY)
    opencv_api.show_img(img)
    img = opencv_api.adaptiveThreshold_img(
        img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )
    opencv_api.show_img(img)
    img = opencv_api.threshold_img(img, "Otsu", 0, 0)
    opencv_api.show_img(img)

    img = opencv_api.watershed_img(img)
    opencv_api.show_img(img)


if __name__ == "__main__":
    main()
