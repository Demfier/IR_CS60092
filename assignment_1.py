"""
Title: IR Assignment 1 Solution
Name: Gaurav Sahu
Roll number: 14MF10008
"""

import os
import json
import itertools
import operator
import time

import re
import nltk
import build_inverted_index


def search(string, file):
    """
    Searches for the string in the given file and returns True/False
    accordingly
    """
    pattern = re.compile(string)
    try:
        with open(file, 'rb') as document:
            for line in document.readlines():
                if re.search(pattern, line):
                    return(True)
    except IOError as e:
        return(False)
    return(False)


def grep(pattern, directory):
    """
    Python implementation of grep - Global Regular Expression Print
    Parameters:
        - pattern <Str>: Query term to search. For pattern with multiple terms
                         it finds result for each of the query and performs a
                         logical AND on the result
        - directory <Str>: Location where to perform grep
    Returns:
        - List of at most 50 document ids where it pattern is found in the
          directory
    """
    query_terms = pattern.strip().split()
    # Get all files in the `directory`
    files = os.listdir(directory)

    minKey = ''  # Query with shortest posting list
    minLen = None  # Length of the shortest posting list

    relevant_docs = {}
    for query in query_terms:
        relevant_docs[query] = set()
        for file in files:
            if search(query, directory + '/' + file):
                relevant_docs[query].add(file)

        curr_doc_len = len(relevant_docs[query])
        if minLen is None:
            minLen = curr_doc_len
            minKey = query
        elif curr_doc_len < minLen:
            minLen = curr_doc_len
            minKey = query

    # `Merge` the results for individual query
    final_result = relevant_docs[minKey]
    for query in relevant_docs:
        if query == minKey:
            continue
        else:
            final_result = final_result.intersection(relevant_docs[query])
    # Taking only top 50 results
    return(list(final_result)[:50])


def grep_based_retrieval():
    """
    Python implementation of grep based boolean retrieval
    """

    # load input data
    with open('data/jsonified_data.json') as json_data:
        input_data = json.load(json_data)

    for qid in input_data:
        start = time.clock()
        query = input_data[qid]['input_query']
        result = grep(query, 'data/alldocs')
        input_data[qid]['system_response'] = result
        input_data[qid]['time_taken'] = time.clock() - start
        print("query {0} ({1} seconds) => {2}".format(qid,
                                                      time.clock() - start,
                                                      result))

    with open('output/bool_retrieval_json_output.json', 'w') as json_output:
        json.dump(input_data, json_output)
    return(True)


def intersection(posting_lists):
    """
    Finds intersection of multiple posting lists efficiently
    Parameters:
        - posting_lists <list> of <set>
    Returns:
        - Merged result after intersection
    """
    # sort the posting lists in increasing order of length.
    # it will be useful while finding the intersection
    posting_lists = sorted(posting_lists, key=len)

    result = posting_lists[0]
    for p_list in posting_lists[1:]:
        result = result.intersection(p_list)
    # take only top 50 results
    return(list(result)[:50])


def index_based_retrieval():
    """
    Python implementation of index based boolean retrieval.
    """

    # load input data
    with open('data/jsonified_data.json') as json_data:
        input_data = json.load(json_data)

    # load inverted index
    with open('output/inverted_index.json') as iindex:
        inverted_index = json.load(iindex)

    for qid in input_data:
        posting_lists = []
        start = time.clock()
        query = input_data[qid]['input_query']
        # do the same preprocess on query as done while building corpus
        query_tokens = build_inverted_index.preprocess(query)

        # Get the posting lists for all the tokens in query
        for token in query_tokens:
            posting_lists.append(set(inverted_index[token]))

        # get intersection of all the posting lists
        result = intersection(posting_lists)
        input_data[qid]['system_response'] = result
        input_data[qid]['time_taken'] = time.clock() - start
        print("query {0} ({1} seconds) => {2}".format(qid,
                                                      time.clock() - start,
                                                      result))

    with open('output/index_based_bool_retrieval.json', 'w') as json_output:
        json.dump(input_data, json_output)
    return(True)


if __name__ == '__main__':
    # grep_based_retrieval()
    index_based_retrieval()
