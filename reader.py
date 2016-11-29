# Copyright 2015 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

# From https://github.com/tensorflow/tensorflow/blob/master/tensorflow/models/rnn/ptb/reader.py

"""Utilities for parsing text files."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import os

import tensorflow as tf


def _read_words(filename):
  with tf.gfile.GFile(filename, "r") as f:
    return f.read().decode("utf-8").replace(string.punctuation, "<eos>").split()


def _build_vocab(filename):
  data = _read_words(filename)
  reverse_data = data[::-1]

  counter = collections.Counter(data)
  reverse_counter = collections.Counter(reverse_data)
  count_pairs = sorted(counter.items(), key=lambda x: (-x[1], x[0]))
  reverse_pairs = sorted(reverse_counter.items(), key=lambda x: (-x[1], x[0]))

  words, _ = list(zip(*count_pairs)) + list(zip(*reverse_pairs))
  word_to_id = dict(zip(words, range(len(words))))

  return word_to_id


def _file_to_word_ids(filename, word_to_id):
  data = _read_words(filename)
  return [word_to_id[word] for word in data if word in word_to_id]


def bidirectional_raw_data(data_path=None):
  """Load training/test raw data from data directory "data_path".
  Reads text files, converts strings to integer ids,
  and performs mini-batching of the inputs.
  Args:
    data_path: string path to the directory where simple-examples.tgz has
      been extracted.
  Returns:
    tuple (train_data, test_data, vocabulary)
    where each of the data objects can be passed to Iterator.
  """

  train_path = os.path.join(data_path, "dataset/holmes_Training_Data.tar")
  # valid_path = os.path.join(data_path, "ptb.valid.txt")
  test_path = os.path.join(data_path, "dataset/MSR_Sentence_Completion_Challenge_V1.tar")

  word_to_id = _build_vocab(train_path)
  train_data = _file_to_word_ids(train_path, word_to_id)
  # valid_data = _file_to_word_ids(valid_path, word_to_id)
  test_data = _file_to_word_ids(test_path, word_to_id)
  vocabulary = len(word_to_id)
  return train_data, test_data, vocabulary


def bidirectional_producer(raw_data, batch_size, num_steps, name=None):
  """Iterate on the raw data.
  This chunks up raw_data into batches of examples and returns Tensors that
  are drawn from these batches.
  Args:
    raw_data: one of the raw data outputs from bidirectional_raw_data.
    batch_size: int, the batch size.
    num_steps: int, the number of unrolls.
  Returns:
    A pair of Tensors, each shaped [batch_size, num_steps]. The second element
    of the tuple is the same data time-shifted to the right by one.
  Raises:
    tf.errors.InvalidArgumentError: if batch_size or num_steps are too high.
  """
  with tf.name_scope(name, "Producer", [raw_data, batch_size, num_steps]):
    raw_data = tf.convert_to_tensor(raw_data, name="raw_data", dtype=tf.int32)

    data_len = tf.size(raw_data)
    batch_len = data_len // batch_size
    data = tf.reshape(raw_data[0 : batch_size * batch_len],
                      [batch_size, batch_len])

    epoch_size = (batch_len - 1) // num_steps
    assertion = tf.assert_positive(
        epoch_size,
        message="epoch_size == 0, decrease batch_size or num_steps")
    with tf.control_dependencies([assertion]):
      epoch_size = tf.identity(epoch_size, name="epoch_size")

    i = tf.train.range_input_producer(epoch_size, shuffle=False).dequeue()
    x = tf.slice(data, [0, i * num_steps], [batch_size, num_steps])
    y = tf.slice(data, [0, i * num_steps + 1], [batch_size, num_steps])
    return x, y