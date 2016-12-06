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
# from __future__ import absolute_import
# from __future__ import division
# from __future__ import print_function

import collections
import string
import os
from NGram import get_test_data

# import tensorflow as tf


def _read_words(filename):

    # Folders in wsj 00 - 24
    folder_name = 0
    sentences = []
    
    for i in xrange(25):
        if i < 10:
            folder_name = '0' + str(i)
        else:
            folder_name = str(i)
            
        # Files 01 - 99
        for j in xrange(1,100):
            if j < 10:
                file_name = '0' + str(j)
            else:
                file_name = str(j)
                
            with open(filename + folder_name + "/wsj_" + folder_name + file_name, 'r') as f:
                for line in f:
                    line = line.replace('\n', '')
                    punctuation = "!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
                    new_line = line
                    for char in line:
                        if char in punctuation:
                            new_line = new_line.replace(char, '')
                    if new_line != 'START ' and new_line != '':
                        sentences.append(new_line)
    return sentences
    
# print _read_words("dataset/treebank2/raw/wsj/")
    
def _read_test(datafolder):
    question, answer = get_test_data(datafolder)
    sentences = [question[x]['statement'] for x in question]
    return sentences

# print _read_test("dataset/MSR_Sentence_Completion_Challenge_V1/Data/")

def _build_vocab(filename):
    sentences = _read_words(filename)
    data = []
    for sentence in sentences:
        data.extend(sentence.split())

    # counter = dictionary of word, count
    counter = collections.Counter(data)
    # list of tuples of (word, count) in descending order
    count_pairs = sorted(counter.items(), key=lambda x: (-x[1], x[0]))

    # Return list of [(words),(counts)] in descending order
    words, _ = list(zip(*count_pairs))
    # Return dictionary of {word : index in counts tuple}
    word_to_id = dict(zip(words, range(len(words))))

    return word_to_id

# print(_build_vocab('dataset/treebank2/raw/wsj/'))

def _file_to_word_ids(filename, word_to_id, train = True):
    """ Return list of indices for each word to the counts tuple """
    sentences = []
    if train:
        sentences = _read_words(filename)
    else:
        sentences = _read_test(filename)
    data = []
    for sentence in sentences:
        data.extend(sentence.split())
    return [word_to_id[word] for word in data if word in word_to_id]


### TODO: format test data correctly (maybe new reader for test data itself?)
def _raw_data(data_path=None):
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

    train_path = "dataset/treebank2/raw/wsj/"
    # valid_path = os.path.join(data_path, "ptb.valid.txt")
    test_path = "dataset/MSR_Sentence_Completion_Challenge_V1/Data/"

    word_to_id = _build_vocab(train_path)  
    train_data = _file_to_word_ids(train_path, word_to_id, True)
    # valid_data = _file_to_word_ids(valid_path, word_to_id)
    test_data = _file_to_word_ids(test_path, word_to_id, False)
    vocabulary = len(word_to_id)
    return train_data, test_data, vocabulary

#train, test, vocab = _raw_data()
#print len(train), train[:10], len(test), test[:10], vocab

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
