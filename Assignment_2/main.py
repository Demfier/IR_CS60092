"""
Title: IR Assignment 2 Solution
Name: Gaurav Sahu
Roll number: 14MF10008
"""

import os
import time
import json
import helper
import operator
import itertools
import numpy as np

import re
import nltk


INPUT_DIRS = ['Topic' + str(i) + '/' for i in [1]]
SUMMARY_SIZE = 250


def summaryDegreeCentrality(input_dirs, threshold):
    for input_dir in input_dirs:
        inverted_index = helper.build_inv_index(input_dir)
        tf_idf_vects, sentId_map = helper.build_tf_idf_vectors(input_dir,
                                                               inverted_index)
        graph, degree = helper.build_graph(tf_idf_vects, threshold)

        # Generate Summary
        i = 0
        word_count = 0
        summary = ''
        while(word_count <= SUMMARY_SIZE):
            sentence = sentId_map[list(tf_idf_vects.keys())[graph[i]]]
            print(list(tf_idf_vects.keys())[graph[i]])
            for word in sentence.split(' '):
                summary += ' ' + word
                word_count += 1
                if word_count > SUMMARY_SIZE:
                    break
            i += 1
        # print(summary, len(summary.split(' ')))


def summaryTextRank(input_dirs):
    pass


def summarize(input_dirs, method='DC'):
    if method == 'DC':
        # generate summary using degree centrality
        summary = summaryDegreeCentrality(input_dirs, threshold=0.1)
    elif method == 'TR':
        # generate summary using text rank
        summary = summaryTextRank(input_dirs)
    else:
        raise NotImplementedError


if __name__ == '__main__':
    summarize(INPUT_DIRS, method='DC')
    # summarize(INPUT_DIRS, method='TR')
