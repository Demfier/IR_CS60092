"""
Title: Evaluation Script for Assignment 1 Solution
Name: Gaurav Sahu
Roll number: 14MF10008
"""

import json


def stats(retrieved, relevant):
    """
    Parameters:
        - retrieved <set>: documents retrieved by the system
        - relevant <set>: actually relevant documents (ground truth)
    Returns:
        - performance <dict>: precision and recall
    """
    tp = len(relevant.intersection(retrieved))

    if len(retrieved) == 0:
        return({'precision': 0, 'recall': 0})
    precision = float(tp) / len(retrieved)
    recall = float(tp) / len(relevant)
    return({'precision': precision, 'recall': recall})


def evaluate(system='grep'):
    """
    Evaluates the different retreival systems built. By default evaluates the
    grep based boolean retrieval system
    """
    if system == 'grep':
        with open('output/bool_retrieval_json_output.json') as system:
            data = json.load(system)
    elif system == 'index':
        with open('output/index_based_bool_retrieval.json') as system:
            data = json.load(system)
    elif system == 'lucene_index':
        with open('output/lucene_index_based_retrieval.json') as system:
            data = json.load(system)

    total_time = 0
    performance = {}
    for qid in data:
        result = stats(set(data[qid]['system_response']),
                       set(data[qid]['ground_truth']))
        total_time += data[qid]['time_taken']

        if performance == {}:
            performance['precision'] = [result['precision']]
            performance['recall'] = [result['recall']]
        else:
            performance['precision'].append(result['precision'])
            performance['recall'].append(result['recall'])

    qw_precision = performance['precision']  # query wise prec
    qw_recall = performance['recall']  # query wise rec
    # Does the macro averaging of P an R
    performance['precision'] = sum(qw_precision) / len(qw_precision)
    performance['recall'] = sum(qw_recall) / len(qw_recall)
    return(performance['precision'], performance['recall'], total_time)

if __name__ == '__main__':
    print("The Precsion, Recall and Total Time for search for systems:\n")
    print("Grep based: {0}".format(evaluate()))
    print("Index based: {0}".format(evaluate(system='index')))
    print("Index based (Lucene): {0}".format(evaluate(system='lucene_index')))
