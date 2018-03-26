"""
Title: IR Assignment 2 Solution
Name: Gaurav Sahu
Roll number: 14MF10008
"""
import os
import json
import math
import string
import operator
import collections
import numpy as np

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

from bs4 import BeautifulSoup

STOP_WORDS = set(stopwords.words('english'))
STEMMER = PorterStemmer()


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


def build_inv_index(input_dir):
    """
    Builds inverted index of input `data`.
    It has two parts:
      - Pre-Processing of the input text
      - Build the postings list

    Returns:
        - inverted_index <dict>: The inverted index {token: posting_list}
    """
    data_files = os.listdir(input_dir)

    docID_to_file = {}
    doc_inverted_indexes = []
    for idx, doc in enumerate(data_files):
        docID_to_file[idx] = doc
        html_data = open(input_dir + doc, 'r').read().strip()
        soup = BeautifulSoup(html_data, 'lxml')
        word_tokens = preprocess(soup.body.get_text())
        # Build inverted index for the current document using `indexify`
        # `inverted_index` will be a merge of all such `doc_inverted_index`s
        doc_inverted_indexes.append(indexify(word_tokens, idx))
        print("Finished {0} => {1}".format(idx, doc))

    with open('output/{}_docID_map.json'.format(input_dir), 'w') as doc_map:
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


def vectorize(sentence, t_id, idf):
    vector = {}

    word_tokens = preprocess(sentence)
    for word in word_tokens:
        try:
            vector[t_id[word]] += 1
        except KeyError:
            vector[t_id[word]] = 1
    vector = {key: vector[key] * idf[key] for key in vector}
    return(vector)


def build_tf_idf_vectors(input_dir, inverted_index):
    """
    Finds tf-idf vector of the sentences
    """
    N = len(os.listdir(input_dir))
    idf = {}
    t_id = {}

    for idx, term in enumerate(inverted_index.keys()):
        t_id[term] = idx
        idf[t_id[term]] = math.log(
            float(N) / len(inverted_index[term])) / math.log(10)

    sent_map = {}
    vect_sent_map = {}
    for doc_id, doc in enumerate(os.listdir(input_dir)):
        html_data = open(input_dir + doc, 'r').read().strip()
        soup = BeautifulSoup(html_data, 'lxml')
        content = ''
        for para in soup.findAll('p'):
            content += para.text
        tokenized_sentences = nltk.tokenize.sent_tokenize(content)
        for sent_id, sentence in enumerate(tokenized_sentences):
            vector = vectorize(sentence, t_id, idf)
            if len(vector) != 0:
                sent_map['d{}s{}'.format(doc_id, sent_id)] = sentence
                vect_sent_map['d{}s{}'.format(doc_id, sent_id)] = vector
    return(vect_sent_map, sent_map)


def cosine_similarity(vect1, vect2):
    """
    Finds cosine similarity between two vectors vect1 and vect2
    """
    d_vec1 = sum([value**2 for value in vect1.values()])
    d_vec2 = sum([value**2 for value in vect2.values()])
    n_vec = sum([vect1[key] * vect2[key]
                 for key in set(vect1.keys()).intersection(set(vect2.keys()))])
    c_sim = float(n_vec) / (math.sqrt(d_vec1 * d_vec2))
    return c_sim


def build_graph(tf_idf_vectors, threshold=0.1):
    """
    Builds graph for degree centrality approach using tf-idf vectors
    """
    total_sentences = len(tf_idf_vectors.keys())

    # initialize cosine matrix
    c_mat = np.zeros((total_sentences, total_sentences))
    adjusted_mat = np.zeros((total_sentences, total_sentences))
    for i, s_id1 in enumerate(tf_idf_vectors):
        for j, s_id2 in enumerate(tf_idf_vectors):
            c_mat[i][j] = cosine_similarity(
                tf_idf_vectors[s_id1], tf_idf_vectors[s_id2])
            if c_mat[i][j] >= threshold:
                adjusted_mat[i][j] = 1

    # degree of centrality
    degree = np.sum(adjusted_mat, axis=0)
    final_mat = np.argsort(degree)[::-1]
    return(final_mat, degree)
