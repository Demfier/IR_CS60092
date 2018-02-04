"""
Title: IR Assignment 1 Solution
Name: Gaurav Sahu
Roll number: 14MF10008
"""

import itertools
import operator
import json


def jsonify_data():
    big_json_data = {}
    # Read input data and ground truth output
    with open('data/query.txt') as ip_data:
        queries = ip_data.read().splitlines()
    with open('data/output.txt') as op_data:
        ground_truth = op_data.read().splitlines()

    for query in queries:
        try:
            (qid, qry) = query.split('  ')
            big_json_data[qid] = {'input_query': qry}
        except ValueError:
            pass

    ground_truth = map(lambda x: tuple(x.strip().split(' ')), ground_truth)
    # group the groud truth
    ground_truth = itertools.groupby(ground_truth, key=operator.itemgetter(0))
    for qid, g in ground_truth:
        try:
            big_json_data[qid]['ground_truth'] = [f[1] for f in g]
        except KeyError:
            pass
    return(big_json_data)


if __name__ == '__main__':
    big_json_data = jsonify_data()
    with open('data/jsonified_data.json', 'w') as big_d:
        json.dump(big_json_data, big_d)
