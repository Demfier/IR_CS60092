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


INPUT_DIRS = ['Topic' + str(i) + '/' for i in range(1, 6)]
SUMMARY_SIZE = 250


def summarize(input_dir, threshold=0.1, method='DC'):
    inverted_index = helper.build_inv_index(input_dir)
    tf_idf_vects, sentId_map = helper.build_tf_idf_vectors(input_dir,
                                                           inverted_index)
    if method == 'DC':
        # generate graph for degree centrality approach
        graph, degree = helper.build_graph(tf_idf_vects, threshold)
    elif method == 'TR':
        # generate graph for text rank approach
        graph, degree = helper.build_graph(tf_idf_vects, threshold, for_tr=True)
    else:
        raise NotImplementedError

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
    output_dir = 'output/{}/{}'.format(threshold, method)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with open('{}/{}.txt'.format(output_dir, input_dir.strip('/')), 'w') as deg_out:
        deg_out.write(summary)


def summarize_all(input_dirs, threshold=0.1, method='DC'):
    for input_dir in input_dirs:
        summarize(input_dir, threshold, method)


if __name__ == '__main__':
    summarize_all(INPUT_DIRS, threshold=0.1, method='DC')
    # summarize(INPUT_DIRS, method='TR')
