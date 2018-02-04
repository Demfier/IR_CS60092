"""
Title: IR Assignment 1 Solution
Name: Gaurav Sahu
Roll number: 14MF10008
"""

import os
import time
import json
import operator
import itertools
import collections

import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

STOP_WORDS = set(stopwords.words('english'))
STEMMER = PorterStemmer()
LEMMATIZER = WordNetLemmatizer()


def preprocess(text):
    """
    Processes a chunk of text.
    Steps:
      => lowercase
      => tokenize
      => stem
    """
    # to lowercase
    text = text.lower()

    # Remove puntuation
    text = text.translate(str.maketrans('', '', string.punctuation))

    # tokenize
    word_tokens = word_tokenize(text)
    word_tokens = set(word_tokens)

    # Remove stop words
    word_tokens = [word for word in word_tokens if word not in STOP_WORDS]

    # lemmtize
    # NOTE: lemmatization can increase accuracy but is too slow
    # word_tokens = [LEMMATIZER.lemmatize(word) for word in word_tokens]

    # stem
    word_tokens = [STEMMER.stem(word) for word in word_tokens]
    return(word_tokens)


def indexify(tokens, doc_id):
    """
    Builds the inverted index for tokens of a given document.
    Parameters:
        - tokens <list>: list of tokens
        - doc_id <int>: id of the document
    """
    return(dict.fromkeys(tokens, doc_id))


def build_inverted_index():
    """
    Builds inverted index of input `data`.
    It has two parts:
      - Pre-Processing of the input text
      - Build the postings list

    Returns:
        - inverted_index <dict>: The inverted index {token: posting_list}
    """
    inverted_index = {}
    data_files = os.listdir('data/alldocs')

    docID_to_file = {}
    doc_inverted_indexes = []
    for idx, file in enumerate(data_files):
        docID_to_file[idx] = file
        with open('data/alldocs/' + file) as data_file:
            text = data_file.read().strip()
        word_tokens = preprocess(text)
        # Build inverted index for the current document using `indexify`
        # `inverted_index` will be a merge of all such `doc_inverted_index`s
        doc_inverted_indexes.append(indexify(word_tokens, idx))
        print("Finished {0} => {1}".format(idx, file))

    with open('output/docID_map.json', 'w') as doc_map:
        json.dump(docID_to_file, doc_map)

    # merge all the individual document inverted indexes
    inverted_index = collections.defaultdict(list)
    for dictionary in doc_inverted_indexes:
        for k, v in dictionary.items():
            inverted_index[k].append(v)

    # sort the dictionary by tokens
    # NOTE: No need to sort the posting lists as the way they are built, they
    # are already sorted
    inverted_index = collections.OrderedDict(
        sorted(inverted_index.items(), key=operator.itemgetter(0)))
    return(inverted_index)


if __name__ == '__main__':
    inverted_index = build_inverted_index()
    with open('output/inverted_index.json', 'w') as op_file:
        json.dump(inverted_index, op_file)
