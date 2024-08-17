from pathlib import Path
from typing import cast

import cv2
import imagehash
import mediapipe as mp
import numpy as np
from mediapipe.tasks.python import BaseOptions, vision
from mediapipe.tasks.python.components.containers.bounding_box import \
    BoundingBox
from mediapipe.tasks.python.components.containers.detections import (
    Detection, DetectionResult)
from PIL import Image

from mozyq.types import COCO, Images

# !wget -q -O efficientdet.tflite -q https://storage.googleapis.com/mediapipe-models/object_detector/efficientdet_lite0/int8/1/efficientdet_lite0.tflite


def load_images(pool: Path) -> Images:
    for file in pool.iterdir():
        img = mp.Image.create_from_file(str(file))

        yield img, file.name


def area(obj):
    return obj.width * obj.height


def margin_ratio_ltrb(bbox: BoundingBox, img: mp.Image):
    w, h = img.width, img.height

    return (
        bbox.origin_x / w,
        bbox.origin_y / h,
        (w - bbox.origin_x + bbox.width) / w,
        (h - bbox.origin_y + bbox.height) / h)


def has_category(detection: Detection, objects: list[COCO]):
    return any([
        cat.category_name in objects
        for cat in detection.categories])


def img_hash(imgs: Images, hash_size=16):
    hs = set()
    for img, name in imgs:
        hash = imagehash.phash(
            Image.fromarray(img.numpy_view()),
            hash_size)
        if hash not in hs:
            hs.add(hash)
            yield img, name


def object(
        imgs: Images,
        *,
        include: list[COCO] = [],
        exclude: list[COCO] = [],
        min_include_area=.1,
        min_include_margin=.1,
        min_exclude_area=.0,
        score_threshold=.7):

    base_options = BaseOptions(model_asset_path='efficientdet.tflite')
    options = vision.ObjectDetectorOptions(
        base_options=base_options,
        score_threshold=score_threshold)

    detector = vision.ObjectDetector.create_from_options(options)

    for img, name in imgs:
        exclude_ar = 0.0

        res = detector.detect(img)
        res = cast(DetectionResult, res)

        ex = [
            detection
            for detection in res.detections
            if has_category(detection, exclude)]

        if ex:
            max_exclude = max(
                ex,
                key=lambda d: area(d.bounding_box))

            exclude_ar = area(max_exclude.bounding_box) / area(img)

        if min_exclude_area < exclude_ar:
            continue

        if not include:
            yield img, name
            continue

        include_ar = 0.0
        include_mr = 0.0

        inc = [
            detection
            for detection in res.detections
            if has_category(detection, include)]

        if not inc:
            continue

        max_include = max(
            inc,
            key=lambda d: area(d.bounding_box))

        include_ar = area(max_include.bounding_box) / area(img)
        include_mr = min(margin_ratio_ltrb(max_include.bounding_box, img))

        if min_include_area < include_ar and min_include_margin < include_mr:
            yield img, f'obj:{include_ar:.2f}_{name}'


def face(
        imgs: Images,  *,
        min_detection_confidence=.8,
        min_area=.1,
        max_area=.6,
        min_margin=.1):

    options = vision.FaceDetectorOptions(
        base_options=BaseOptions(model_asset_path='detector.tflite'),
        min_detection_confidence=min_detection_confidence)

    detector = vision.FaceDetector.create_from_options(options)

    for img, name in imgs:
        res = detector.detect(img)
        res = cast(DetectionResult, res)

        detections = res.detections

        if not detections:
            continue

        max_detection = max(
            detections,
            key=lambda d: area(d.bounding_box))

        bbox = max_detection.bounding_box
        bbox = cast(BoundingBox, bbox)

        ar = area(bbox) / area(img)
        mr = min(margin_ratio_ltrb(bbox, img))

        if min_area < ar < max_area and mr > min_margin:
            yield img,  f'{ar:.2f}_{mr:.2f}_{max_detection.categories[0].score:.2f}_{name}'


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
