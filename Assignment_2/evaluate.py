"""
Title: IR Assignment 2 Solution
Name: Gaurav Sahu
Roll number: 14MF10008
"""
from __future__ import division
import os
import six
from itertools import chain
import collections
from nltk.tokenize import word_tokenize


REF_SUMMARY_DIR = 'GroundTruth/'
MACHINE_SUMMARY_DIR = 'output/'
THRESHOLDS = [0.1, 0.2, 0.3]
METHODS = ['TR']


def _ngrams(words, n):
    queue = collections.deque(maxlen=n)
    for w in words:
        queue.append(w)
        if len(queue) == n:
            yield tuple(queue)


def _ngram_counts(words, n):
    return collections.Counter(_ngrams(words, n))


def _ngram_count(words, n):
    return max(len(words) - n + 1, 0)


def _counter_overlap(counter1, counter2):
    result = 0
    for k, v in six.iteritems(counter1):
        result += min(v, counter2[k])
    return result


def _safe_divide(numerator, denominator):
    if denominator > 0:
        return numerator / denominator
    else:
        return 0


def _safe_f1(matches, recall_total, precision_total, alpha):
    recall_score = _safe_divide(matches, recall_total)
    precision_score = _safe_divide(matches, precision_total)
    denom = (1.0 - alpha) * precision_score + alpha * recall_score
    if denom > 0.0:
        return (precision_score * recall_score) / denom
    else:
        return 0.0


def rouge_n(peer, models, n, alpha):
    """
    Compute the ROUGE-N score of a peer with respect to one or more models, for
    a given value of `n`.
    """
    matches = 0
    recall_total = 0
    peer_counter = _ngram_counts(peer, n)
    for model in models:
        model_counter = _ngram_counts(model, n)
        matches += _counter_overlap(peer_counter, model_counter)
        recall_total += _ngram_count(model, n)
    precision_total = len(models) * _ngram_count(peer, n)
    return _safe_f1(matches, recall_total, precision_total, alpha)


def rouge_1(peer, models, alpha):
    """
    Compute the ROUGE-1 (unigram) score of a peer with respect to one or more
    models.
    """
    return rouge_n(peer, models, 1, alpha)


def rouge_2(peer, models, alpha):
    """
    Compute the ROUGE-2 (bigram) score of a peer with respect to one or more
    models.
    """
    return rouge_n(peer, models, 2, alpha)


def get_unigram_count(tokens):
    count_dict = dict()
    for t in tokens:
        if t in count_dict:
            count_dict[t] += 1
        else:
            count_dict[t] = 1

    return count_dict


beta = 1


def my_lcs_grid(x, y):
    n = len(x)
    m = len(y)

    table = [[0 for i in range(m + 1)] for j in range(n + 1)]

    for j in range(m + 1):
        for i in range(n + 1):
            if i == 0 or j == 0:
                cell = (0, 'e')
            elif x[i - 1] == y[j - 1]:
                cell = (table[i - 1][j - 1][0] + 1, '\\')
            else:
                over = table[i - 1][j][0]
                left = table[i][j - 1][0]

                if left < over:
                    cell = (over, '^')
                else:
                    cell = (left, '<')

            table[i][j] = cell

    return table


def my_lcs(x, y, mask_x):
    table = my_lcs_grid(x, y)
    i = len(x)
    j = len(y)

    while i > 0 and j > 0:
        move = table[i][j][1]
        if move == '\\':
            mask_x[i - 1] = 1
            i -= 1
            j -= 1
        elif move == '^':
            i -= 1
        elif move == '<':
            j -= 1

    return mask_x


def rouge_l(ref_sents, cand_sents):
    lcs_scores = 0.0
    cand_unigrams = get_unigram_count(chain(*cand_sents))
    ref_unigrams = get_unigram_count(chain(*ref_sents))
    for cand_sent in cand_sents:
        cand_token_mask = [0 for t in cand_sent]
        cand_len = len(cand_sent)
        for ref_sent in ref_sents:
            # aligns = []
            # lcs(ref_sent, cand_sent, aligns)
            my_lcs(cand_sent, ref_sent, cand_token_mask)

            # for i in aligns:
            #     ref_token_mask[i] = 1
        # lcs = []
        cur_lcs_score = 0.0
        for i in range(cand_len):
            if cand_token_mask[i]:
                token = cand_sent[i]
                if cand_unigrams[token] > 0 and ref_unigrams[token] > 0:
                    cand_unigrams[token] -= 1
                    ref_unigrams[token] -= 1
                    cur_lcs_score += 1

                    # lcs.append(token)

        # print ' '.join(lcs)

        lcs_scores += cur_lcs_score

    # print "lcs_scores: %d" % lcs_scores
    ref_words_count = sum(len(s) for s in ref_sents)
    # print "ref_words_count: %d" % ref_words_count
    cand_words_count = sum(len(s) for s in cand_sents)
    # print "cand_words_count: %d" % cand_words_count

    precision = lcs_scores / cand_words_count
    recall = lcs_scores / ref_words_count
    f_score = (1 + beta ** 2) * precision * recall / (recall +
                                                            beta ** 2 * precision + 1e-7) + 1e-6  # prevent underflow
    return precision, recall, f_score


if __name__ == '__main__':
    # Find rouge-1 for all thresholds
    ref_summaries = os.listdir(REF_SUMMARY_DIR)
    for file in ref_summaries:
        ref_sum_text = open(REF_SUMMARY_DIR + file, 'r').read()
        machine_summs = []
        for threshold in [0.3]:
            for method in METHODS:
                output_dir = MACHINE_SUMMARY_DIR + str(threshold) + '/' + method
                if len(os.listdir()) != 0:
                    machine_summs.append(output_dir + '/' + file)
        machine_sum_texts = []
        for sum_file in machine_summs:
            machine_sum_texts.append(open(sum_file, 'r').read())
        print('Results for {}'.format(file))
        print(rouge_1(ref_sum_text, machine_sum_texts, 0.5))
        print(rouge_2(ref_sum_text, machine_sum_texts, 0.5))
        print(rouge_l([ref_sum_text], machine_sum_texts)[2])
