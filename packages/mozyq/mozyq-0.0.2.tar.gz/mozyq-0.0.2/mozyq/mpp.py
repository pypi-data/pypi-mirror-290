
import cv2
import numpy as np

from mozyq.types import Images


def sharp(imgs: Images, min_score=400,) -> Images:
    for img, name in imgs:
        gray = img.numpy_view()
        gray = cv2.cvtColor(gray, cv2.COLOR_RGB2GRAY)

        score = cv2.Laplacian(gray, cv2.CV_64F).var()
        if min_score < score:
            yield img, f'sharp:{score:.2f}_{name}'


def colorful(imgs: Images, min_score=30, max_score=90):
    for img, name in imgs:
        a = img.numpy_view()

        if a.shape[2] != 3:
            continue

        (B, G, R) = cv2.split(a.astype("float"))
        # compute rg = R - G
        rg = np.absolute(R - G)
        # compute yb = 0.5 * (R + G) - B
        yb = np.absolute(0.5 * (R + G) - B)
        # compute the mean and standard deviation of both `rg` and `yb`
        (rbMean, rbStd) = (np.mean(rg), np.std(rg))
        (ybMean, ybStd) = (np.mean(yb), np.std(yb))
        # combine the mean and standard deviations
        stdRoot = np.sqrt((rbStd ** 2) + (ybStd ** 2))
        meanRoot = np.sqrt((rbMean ** 2) + (ybMean ** 2))
        # derive the "colorfulness" metric and return it
        score = stdRoot + (0.3 * meanRoot)
        if min_score < score < max_score:
            yield img, f'col:{score:.2f}_{name}'
