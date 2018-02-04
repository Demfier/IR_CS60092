"""
Title: IR Assignment 1 Solution
Name: Gaurav Sahu
Roll number: 14MF10008
"""

import re
import sys
import os
import itertools
import operator
import json
import time


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


if __name__ == '__main__':
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
