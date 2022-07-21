# -*- coding: utf-8 -*-
"""
Segment an audio file based on average amplitude.
Reference: https://groups.google.com/g/sanskrit-programmers/c/aHS3UYXA6Dc/m/WJj1KYxgAQAJ

"""

import datetime
import logging

import numpy as np
import os
import matplotlib.pyplot as plt

from tqdm import tqdm
from pydub import AudioSegment
from skimage.filters import threshold_otsu
from scipy.signal import medfilt
from more_itertools import pairwise


def moving_average(a, n=3) :
  ret = np.cumsum(a, dtype=float)
  ret[n:] = ret[n:] - ret[:-n]
  return ret[n - 1:] / n


def cut_points(t):
  t = t[:-1] ^ t[1:]
  indices = np.nonzero(t)[0]
  return indices


def save_segments(audio, indices, window_width, orig_filename):
  basename, ext = os.path.splitext(orig_filename)
  ext = ext.strip('.')
  for i, (start, stop) in enumerate(tqdm(pairwise(indices),
                                         desc='Saving segments')):
    # pydub does things in miliseconds
    start *= window_width * 1000
    stop *= window_width * 1000
    segment = audio[start:stop]
    segment.export(f'{basename}_{i}.{ext}', format=ext)


def split_file_by_amplitude(file_path, window_width, threshold_factor,
                            filter_size):
  _start = datetime.datetime.now()
  # Load the file and convert to numpy array
  audio = AudioSegment.from_file(file_path)
  samples = np.array(audio.get_array_of_samples())

  # Pad to a multiple of the window
  width = int(audio.frame_rate * window_width)
  duration = round(len(samples) / width) * width
  samples = np.pad(samples, (0, duration-len(samples)))
  # Reshape into windows
  s = samples.reshape((-1, width))
  # Compute the mean of the audio over each window and apply a moving average
  m = np.mean(np.abs(s), axis=1)
  m = moving_average(m, filter_size)
  # Determine a threshold to apply
  thresh = threshold_factor * threshold_otsu(m)
  t = m > thresh
  # Apply a median filter to remove any spurious points
  t1 = medfilt(t.astype(int), filter_size)
  indices = cut_points(t1)
  save_segments(audio, indices, window_width, file_path)
  _end = datetime.datetime.now()
  _delta = _end - _start
  logging.info(f'Took {_delta} ({_delta.total_seconds()}s) for {file_path}')


if __name__ == "__main__":

  filename = "03-1-PeriyALwAr Tiumuzi-01-02.mp3"

  # window width in seconds
  window_width = 1
  # Factor to adjust the automatically found threshold by
  threshold_factor = 0.75
  # Size of filters applied to remove spurious points
  filter_size = 5

  split_file_by_amplitude(filename, window_width, threshold_factor, filter_size)

