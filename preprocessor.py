from __future__ import print_function
from collections import defaultdict

import common_words
import flesch_kincaid
import sqlite3

# USEFUL_THRESHOLD = 2

def gen_feature_vec(review,
                    useful_bools,
                    useful_ratios,
                    biz_review_counts,
                    top100,
                    threshold):
    text = review['text']
    words = set(flesch_kincaid.words(text.lower()))

    useful = useful_bools[review['id']]
    length = len(text)
    reading_ease, reading_level = flesch_kincaid.results(text)
    rating = review['stars']
    useful_ratio = useful_ratios[review['user_id']] if review['user_id'] in useful_ratios else 0
    biz_review_count = biz_review_counts[review['business_id']]

    features = [
        useful,
        length,
        reading_ease,
        reading_level,
        rating,
        useful_ratio,
        biz_review_count
    ]

    for word in top100:
        features.append(1 if word in words else 0)

    #f = features
    #interaction_features = [f[i] * f[j] for i in range(len(f)) for j in range(i + 1, len(f))]
    #polynomial_features = [x ** y for x in features for y in range(2, 5)]

    #features.extend(interaction_features)
    #features.extend(polynomial_features)

    return [str(x) for x in features]

if __name__ == '__main__':
    db = sqlite3.connect('yelp.sqlite')
    db.row_factory = sqlite3.Row
    c = db.cursor()

    biz_review_counts = c.execute('''SELECT b.business_id, COUNT(*)
                                    FROM business AS b, review AS r
                                    WHERE b.business_id = r.business_id
                                    GROUP BY b.business_id
                                 ''').fetchall()
    biz_review_counts = {k:v for k,v in biz_review_counts}

    reviews = c.execute('SELECT * FROM review').fetchall()

    for USEFUL_THRESHOLD in [1, 3, 5]:
        freq = defaultdict(int)

        useful_reviews = c.execute('''SELECT r.text
                                      FROM review AS r
                                      WHERE r.useful >= ?
                                   ''', (USEFUL_THRESHOLD,)).fetchall()

        for review in useful_reviews:
            for word in flesch_kincaid.words(review['text'].lower()):
                freq[word] += 1

        top100 = sorted(freq.iteritems(), key=lambda item: -item[1])
        top100 = [k for k, v in top100 if k not in common_words.WORDS][:100]
        print(top100, len(top100))

        useful_bools = c.execute('''SELECT r.id, r.useful >= ?
                                    FROM review AS r
                                 ''', (USEFUL_THRESHOLD,)).fetchall()
        useful_bools = {k:v for k,v in useful_bools}

        useful_ratios = c.execute('''SELECT
                                       u.user_id,
                                       1.0 * SUM(CASE WHEN r.useful >= ? THEN 1 ELSE 0 END) / COUNT(*)
                                     FROM user AS u, review AS r
                                     WHERE u.user_id = r.user_id
                                     GROUP BY u.user_id
                                  ''', (USEFUL_THRESHOLD,)).fetchall()
        useful_ratios = {k:v for k,v in useful_ratios}

        with open('features_' + str(USEFUL_THRESHOLD), 'w') as f:
            for review in reviews:
                feature = gen_feature_vec(review, useful_bools, useful_ratios, biz_review_counts, top100, USEFUL_THRESHOLD)
                print(','.join(feature), file=f)

    db.close()
