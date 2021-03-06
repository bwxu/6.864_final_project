# References: https://github.com/tensorflow/tensorflow/blob/master/tensorflow/models/rnn/ptb/reader.py

# python LSTM.py --data_path=. --model small --backwards True

"""Utilities for parsing text files."""
# from __future__ import absolute_import
# from __future__ import division
# from __future__ import print_function

import collections
from NGram import get_test_data
import os
import string
import tensorflow as tf

# Goes through the WSJ corpus and reads all of the sentences
#   Parameters: path of folder of the wsj corpus
#   Returns: list of sentences
def _read_words(filename, backwards):

    # Folders in wsj 00 - 24
    folder_name = 0
    sentences = []
    
    for i in range(25):
        if i < 10:
            folder_name = '0' + str(i)
        else:
            folder_name = str(i)
            
        # Files 01 - 99
        for j in range(1,100):
            if j < 10:
                file_name = '0' + str(j)
            else:
                file_name = str(j)
                
            with open(filename + folder_name + "/wsj_" + folder_name + file_name, 'r', errors='ignore') as f:
                for line in f:
                    line = line.replace('\n', '')
                    new_line = replace_punctuation_marks(line)
                    if new_line != 'START ' and new_line != '':
                        if backwards:
                            sentences.append(reverse_words_in_string(new_line))
                        else:
                            sentences.append(new_line)

    return sentences

# return new sentence without punctuation; doesn't change original sentence
def replace_punctuation_marks(old_sentence):
    new_sentence = old_sentence
    punctuation = "!\"#$%&()*+,-./:;<=>?@[\]^_`{|}~"
    for char in old_sentence:
        if char in punctuation:
            new_sentence = new_sentence.replace(char, '')
    return new_sentence

# reverses words in a sentence string
def reverse_words_in_string(sentence):
    sentence_list = sentence.split()
    sentence_list.reverse()
    return ' '.join(sentence_list)
    
# print _read_words("dataset/treebank2/raw/wsj/")
    
# Goes through Test Data and reads all of the sentences
#   Parameters: folder containing the challenge questions and answers
#   Returns: list of sentences in the format 'I have seen it on him , and could _____ to it.'
def _read_test(datafolder):
    question, answer = get_test_data(datafolder)
    sentences = [question[x]['statement'] for x in question]
    return sentences

# returns tuple:
#     sentence with first 5 answer choices with sentence from beginning to blank
#     sentence with first 5 answer choices with reversed sentence from end to blank
def _read_test_stop_at_blank(datafolder, backwards=False):
    question, answer = get_test_data(datafolder)
    sentences = [question[x]['statement'] for x in question]
    n = len(sentences)
    new_sentences = []
    for i in range(1, len(question) + 1):
        sentence = question[str(i)]['statement']
        forward_sentence, backward_sentence = sentence.split('_____')

        word_choices = ""
        for choice in "abcde":
            word_choice = question[str(i)][choice] + " "
            word_choices += word_choice

        if backwards:
            reversed_backward_sentence = reverse_words_in_string(replace_punctuation_marks(backward_sentence))
            new_reversed_backward_sentence = word_choices + reversed_backward_sentence
            new_sentences.append(new_reversed_backward_sentence)
        else:
            new_forward_sentence = word_choices + replace_punctuation_marks(forward_sentence)
            new_sentences.append(new_forward_sentence)
    return new_sentences

# fill in blank with choices
def fill_in_choices(datafolder):
    question, answer = get_test_data(datafolder)
    sentences = [question[x]['statement'] for x in question]
    n = len(sentences)

    new_sentences = []
    for i in range(1, n):
        for choice in "abcde":
            word_choice = question[str(i)][choice]
            sentence = question[str(i)]['statement']
            sentence = sentence.replace('_____', word_choice)
            # replace punctuation marks using logic above
            new_sentence = replace_punctuation_marks(sentence)
            new_sentences.extend(new_sentence)
    return new_sentences

# print _read_test("dataset/MSR_Sentence_Completion_Challenge_V1/Data/")

# Reads all words in document and creates a word to id mapping
#   Parameters: filename of document to be read
#   Returns: dictionary of unique words mapped to an integer id
def _build_vocab(filename):
    sentences = _read_words(filename, backwards=False)
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

# Converts a text document into a list of ids that map to the original words
#   Parameters: filename indicating the document location (if train) or folder location (if not train)
#               train boolean determining whether or not this is the training set
#   Returns: list with integers representing the mapping of words to their ids
#            list of sentences still in letter form
def _file_to_word_ids(filename, word_to_id, train=True, backwards=False):
    """ Return list of indices for each word to the counts tuple """
    sentences = []
    if train:
        sentences = _read_words(filename, backwards)
    else:
        sentences = _read_test_stop_at_blank(filename, backwards)
    data = []
    for sentence in sentences:
        data.extend(sentence.split())
    return [word_to_id[word] for word in data if word in word_to_id], sentences, [[word_to_id[word] for word in sentence.split() if word in word_to_id] for sentence in sentences]

# Maps train and test set to the corresponding ids
#   Parameters: data_path: path to your repo of 6.864_project (can just leave at None)
#   Returns: Mapped version of train data, test data, and the length of the vocabulary
def _raw_data(data_path=None, backwards=False):
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
    test_path = "dataset/SAT_Questions/"
    question, answer = get_test_data(test_path)

    word_to_id = _build_vocab(train_path)  
    train_data, train_sentences, train_data_in_list_of_lists = _file_to_word_ids(train_path, word_to_id, True, backwards)
    test_data, test_sentences, test_data_in_list_of_lists  = _file_to_word_ids(test_path, word_to_id, False, backwards)
    vocabulary = len(word_to_id)
    return word_to_id, train_data, test_sentences, test_data_in_list_of_lists, question, answer

def _producer(raw_data, batch_size, num_steps, name=None):
    """Iterate on the raw data.
    This chunks up raw_data into batches of examples and returns Tensors that
    are drawn from these batches.
    Args:
        raw_data: one of the raw data outputs from raw_data.
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
