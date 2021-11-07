import paddle
import paddle.nn.functional as F
import numpy as np
import cv2


def rot90(x, k=1):
    """rotate batch of images by 90 degrees k times"""
    try:
        x = paddle.to_tensor(x).numpy()
    except:
        x = x.numpy()
    rot = np.rot90(x, k, (2, 3))
    return paddle.to_tensor(rot)


def hflip(x):
    """flip batch of images horizontally"""
    return x.flip([3])


def vflip(x):
    """flip batch of images vertically"""
    return x.flip([2])


def hshift(x,shifts=0):
    return paddle.roll(x, int(shifts*x.shape[3]), axis=3)


def vshift(x,shifts=0):
    return paddle.roll(x, int(shifts*x.shape[2]), axis=2)


def sum(x1, x2):
    """sum of two tensors"""
    return x1 + x2


def add(x, value):
    """add value to tensor"""
    return x + value


def max(x1, x2):
    """compare 2 tensors and take max values"""
    return paddle.max(paddle.concat([x1, x2]))


def min(x1, x2):
    """compare 2 tensors and take min values"""
    return paddle.min(paddle.concat([x1, x2]))


def multiply(x, factor):
    """multiply tensor by factor"""
    return x * factor


def scale(x, scale_factor, interpolation="nearest", align_corners=False):
    """scale batch of images by `scale_factor` with given interpolation mode"""
    h, w = x.shape[2:]
    new_h = int(h * scale_factor)
    new_w = int(w * scale_factor)
    return F.interpolate(
        x, size=(new_h, new_w), mode=interpolation, align_corners=align_corners
    )


def resize(x, size, interpolation="nearest", align_corners=False):
    """resize batch of images to given spatial size with given interpolation mode"""
    return F.interpolate(x, size=size, mode=interpolation, align_corners=align_corners)


def crop(x, x_min=None, x_max=None, y_min=None, y_max=None):
    """perform crop on batch of images"""
    return x[:, :, y_min:y_max, x_min:x_max]


def crop_lt(x, crop_h, crop_w):
    """crop left top corner"""
    return x[:, :, 0:crop_h, 0:crop_w]


def crop_lb(x, crop_h, crop_w):
    """crop left bottom corner"""
    return x[:, :, -crop_h:, 0:crop_w]


def crop_rt(x, crop_h, crop_w):
    """crop right top corner"""
    return x[:, :, 0:crop_h, -crop_w:]


def crop_rb(x, crop_h, crop_w):
    """crop right bottom corner"""
    return x[:, :, -crop_h:, -crop_w:]


def center_crop(x, crop_h, crop_w):
    """make center crop"""

    center_h = x.shape[2] // 2
    center_w = x.shape[3] // 2
    half_crop_h = crop_h // 2
    half_crop_w = crop_w // 2

    y_min = center_h - half_crop_h
    y_max = center_h + half_crop_h + crop_h % 2
    x_min = center_w - half_crop_w
    x_max = center_w + half_crop_w + crop_w % 2

    return x[:, :, y_min:y_max, x_min:x_max]


def _disassemble_keypoints(keypoints):
    x = keypoints[:, 0]
    y = keypoints[:, 1]
    return x, y


def _assemble_keypoints(x, y):
    return paddle.stack([x, y], axis=-1)


def keypoints_hflip(keypoints):
    x, y = _disassemble_keypoints(keypoints)
    return _assemble_keypoints(1. - x, y)


def keypoints_vflip(keypoints):
    x, y = _disassemble_keypoints(keypoints)
    return _assemble_keypoints(x, 1. - y)


def keypoints_hshift(keypoints,shifts):
    x, y = _disassemble_keypoints(keypoints)
    return _assemble_keypoints((x + shifts) % 1, y)


def keypoints_vshift(keypoints,shifts):
    x, y = _disassemble_keypoints(keypoints)
    return _assemble_keypoints(x, (y + shifts) % 1)

def keypoints_pad(keypoints,pad ):
    x, y = _disassemble_keypoints(keypoints)
    return _assemble_keypoints(x*x/(x+pad[0]), y*y/(y + pad[0]))

def keypoints_rot90(keypoints, k=1):

    if k not in {0, 1, 2, 3}:
        raise ValueError("Parameter k must be in [0:3]")
    if k == 0:
        return keypoints
    x, y = _disassemble_keypoints(keypoints)

    if k == 1:
        xy = [y, 1. - x]
    elif k == 2:
        xy = [1. - x, 1. - y]
    elif k == 3:
        xy = [1. - y, x]

    return _assemble_keypoints(*xy)



def adjust_contrast(x,contrast_factor=0.5):
    table = np.array([(i - 74) * contrast_factor + 74
                      for i in range(0, 256)]).clip(0, 255).astype('uint8')
    if len(x.shape) == 3 and x.shape[2] == 1:
        return cv2.LUT(x, table)[:, :, np.newaxis]
    else:
        return cv2.LUT(x, table)



def adjust_brightness(x,brightness_factor=1):
    table = np.array([i * brightness_factor
                      for i in range(0, 256)]).clip(0, 255).astype('uint8')

    if len(x.shape) == 3 and x.shape[2] == 1:
        return cv2.LUT(x, table)[:, :, np.newaxis]
    else:
        return cv2.LUT(x, table)


def saturationtransform(x,value=1):
    return x.transforms.SaturationTransform(value)


def pad(x,pad=0,mode='constant',value=0):
    return F.pad(x,pad,mode,value)

