#! usr/bin/env python
import sys
import json


def mapper():
    """Take in stdin and return each hashtag with the number one"""
    for line in sys.stdin.split('/n'):
        count = 0
        try:
            entity = json.loads(tweet)
            try:
                entity = entity['entities']
                if entity is not None and (entity['hashtags'] is not None
                                           or len(entity['hashtags']) != 0):
                    for hashtags in entity['hashtags']:
                            print(hashtags['text'], 1)
            except KeyError:
                continue
        except AssertionError:
            continue


if __name__ == '__main__':
    mapper()
