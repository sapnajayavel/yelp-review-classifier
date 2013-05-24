from __future__ import print_function
from collections import defaultdict
from multiprocessing import Pool
import json
import flesch_kincaid

DATA_FILENAME_FORMAT = 'yelp_phoenix_academic_dataset/yelp_academic_dataset_{}.json'
DATA_TYPE = 'review_test'
DATA_TYPE = 'review'
d = defaultdict(int)

def generate_feature_vector(s):
    review = json.loads(s.strip())
    votes = review['votes']

    valid = False
    for k, v in votes.items():
        if v >= 5:
            valid = True
            d[k] += 1

    if not valid:
        return None

    text = review['text']

    length = len(text)
    reading_ease, reading_level = flesch_kincaid.results(text)
    rating = review['stars']

    features = [
        length,
        reading_ease,
        reading_level,
        rating
    ]

    return [str(x) for x in features]

if __name__ == '__main__':
    pool = Pool(processes=8)

    total = 0
    reviews = []
    with open(DATA_FILENAME_FORMAT.format(DATA_TYPE), 'r') as f:
        features = pool.map(generate_feature_vector, f.readlines())
        with open('out', 'w') as out:
            for feature in features:
                if feature:
                    print(",".join(feature), file=out)

    print(total)
    print(d)

# def generate_feature_vector(s):
#     review = json.loads(s)
#     votes = review['votes']
#
#     valid = False
#     for k, v in votes.items():
#         if v >= 5:
#             valid = True
#             d[k] += 1
#
#     if not valid:
#         return None
#
#     text = review['text']
#
#     length = len(text)
#     reading_ease, reading_level = flesch_kincaid.results(text)
#     rating = review['stars']
#
#     features = [
#         length,
#         reading_ease,
#         reading_level,
#         rating
#     ]
#
#     return features
#
# if __name__ == '__main__':
#     total = 0
#     reviews = []
#     with open(DATA_FILENAME_FORMAT.format(DATA_TYPE), 'r') as f:
#         with open('out', 'w') as out:
#             for line in f:
#                 total += 1
#                 feature = generate_feature_vector(line.strip())
#                 if feature:
#                     print(",".join(feature), file=out)
#
#     print(total)
#     print(d)
