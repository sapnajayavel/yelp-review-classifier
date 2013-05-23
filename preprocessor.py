#!/bin/python

from config import DATASET_DIR, FN_PREFIX

FILENAME_FORMAT = 'yelp_phoenix_academic_dataset/yelp_academic_dataset_{}.json'
DATA_TYPE = 'review_test'

def generate_feature_vector(s):
    return s

if __name__ == '__main__':
    with open(FILENAME_FORMAT.format(DATA_TYPE), 'r') as f:
        for line in f:
            print generate_feature_vector(line.strip())
