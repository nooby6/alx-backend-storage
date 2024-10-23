#!/usr/bin/env python3
"""Contains a mongoDB document update function"""


def update_topics(mongo_collection, name, topics):
    """Updates the all documents in mongo_collection
    with `name` with the topics `topics`i

    Args:
        name (string) will be the school name to update
        topics (list[str]) will be the list of topics in the school
    """

    targets = {"name": name}
    update = {"$set": {"topics": topics}}

    mongo_collection.update_many(targets, update)
