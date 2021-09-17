from __future__ import division
import numpy as np
from numpy.lib.utils import deprecate
from utils import *
from skimage import io, morphology
import cv2
from copy import deepcopy
from pprint import pprint
import matplotlib.pyplot as plt


@deprecate
def blur_param(img: np.array) -> float:
    H, W = img.shape
    Dh_pre, Dh_cur, Zh = 0, 0, 0
    for i in range(H):
        Dh_pre = int(img[i, 1]) - int(img[i, 0])
        for j in range(1, W - 1):
            Dh_cur = int(img[i, j + 1]) - int(img[i, j])
            if Dh_pre * Dh_cur < 0:
                Zh += 1
            Dh_pre = Dh_cur
    Zh = Zh / (H * (W - 2))
    Dv_pre, Dv_cur, Zv = 0, 0, 0
    for j in range(W):
        Dv_pre = int(img[1, j]) - int(img[0, j])
        for i in range(1, H - 1):
            Dv_cur = int(img[i + 1, j]) - int(img[i, j])
            if Dv_pre * Dv_cur < 0:
                Zv += 1
            Dv_pre = Dv_cur
    Zv = Zv / ((H - 2) * W)
    return (Zh + Zv) / 2


def blur_fft(img: np.array, size: int = 60) -> float:
    h, w = img.shape
    ci, cj = h // 2, w // 2
    fft = np.fft.fft2(img)
    shift = np.fft.fftshift(fft)
    shift[ci - size:ci + size, cj - size:cj + size] = 0
    shift = np.fft.ifftshift(shift)
    recon = np.fft.ifft2(shift)
    magnitude = 20 * np.log(np.abs(recon))
    return 50-np.mean(magnitude)


# @runtime
def blur_level(seq: list[np.array]) -> list[float]:
    blur = []
    for frame in seq:
        blur.append(blur_fft(frame))
    return blur


# @runtime
def freeze_detect(seq: list[np.array]) -> list[int]:
    m_image = 30
    f_cut = 0.02
    a = 2.5
    b = 1.25
    c = 0.1
    m_drop = 0.015
    N = len(seq)
    ti = []  # temporal information
    for t in range(1, N):
        diff = np.abs(seq[t] - seq[t - 1])
        diff[diff < m_image] = 0
        ti.append(np.mean(np.power(diff, 2)))
    # print(ti)
    ti_sort = ti.copy()
    ti_sort.sort()
    # print(ti_sort)
    l = int(np.ceil(f_cut * (N - 1)))
    r = int(np.floor((1 - f_cut) * (N - 1)))
    # print(l, r)
    ti_avg = np.mean(ti_sort[l:r + 1])
    dfact = max(a + b * np.log(ti_avg), c)
    # print(dfact)
    drops = [1 if x <= dfact * m_drop else 0 for x in ti]
    return drops


# @runtime
def noise_level(seq: list[np.array],
                thres: int = 40,
                size: int = 8) -> list[float]:
    N = len(seq)
    noise = []
    for t in range(1, N):
        diff = np.abs(seq[t] - seq[t - 1])
        m1 = diff > thres
        m2 = morphology.remove_small_objects(m1, connectivity=2, min_size=size)
        m = np.logical_or(np.logical_not(m1), m2)
        diff[m] = 0
        noise.append(diff.mean())
    return noise


def vimport(filename: str, numfrm: int = 200) -> list[np.array]:
    cap = cv2.VideoCapture(filename)
    fps = cap.get(cv2.CAP_PROP_FPS)
    dims = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    print(fps, dims, frames)
    Fn,Fb,Ff=[],[],[]
    F = []
    num = 0
    success, frame = cap.read()
    while success:
        F.append(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
        if len(F) == numfrm:
            num += 1
            Fn.append(np.mean(noise_level(F)))
            Fb.append(np.mean(blur_level(F)))
            Ff.append(sum(freeze_detect(F)))
            F = []
            print(f'Frame Batch No.{num}')
        success, frame = cap.read()
    cap.release()
    # print(f'Successfully import {len(F)} frames.')
    return Fn,Fb,Ff


if __name__ == '__main__':
    F = mp4_import('./video.mp4')  #example video
    Fn = noise_level(F)
    Fb = blur_level(F)
    Ff = freeze_detect(F)
    print(np.mean(Fn), np.std(Fn), np.max(Fn), np.min(Fn))
    print(np.argmax(Fn),np.argmin(Fn))
    print(np.mean(Fb), np.std(Fb), np.max(Fb), np.min(Fb))
    print(np.argmax(Fb),np.argmin(Fb))
    print(np.mean(Ff), np.std(Ff), np.max(Ff), np.min(Ff))
    print(np.argmax(Ff),np.argmin(Ff))
    with open("result.txt", 'w') as f:
        f.write(str(Fn))
        f.write(str(Fb))
        f.write(str(Ff))

