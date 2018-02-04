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

if __name__ == '__main__':
    # Evaluate boolean retrieval system ==> <Start>
    with open('output/bool_retrieval_json_output.json') as data:
        boolean_data = json.load(data)

    bool_total_time = 0
    bool_performance = {}
    for qid in boolean_data:
        result = stats(set(boolean_data[qid]['system_response']),
                       set(boolean_data[qid]['ground_truth']))
        bool_total_time += boolean_data[qid]['time_taken']

        if bool_performance == {}:
            bool_performance['precision'] = [result['precision']]
            bool_performance['recall'] = [result['recall']]
        else:
            bool_performance['precision'].append(result['precision'])
            bool_performance['recall'].append(result['recall'])

    qw_precision = bool_performance['precision']  # query wise prec
    qw_recall = bool_performance['recall']  # query wise rec
    # Does the macro averaging of P an R
    bool_performance['precision'] = sum(qw_precision) / len(qw_precision)
    bool_performance['recall'] = sum(qw_recall) / len(qw_recall)
    print(bool_performance, bool_total_time)
    # Evaluate boolean retrieval system ==> <End>
