#!/usr/bin/env python3
"""Contains a mongoDB insertion function"""


def insert_school(mongo_collection, **kwargs):
    """Inserts a new document based on kwargs into mongo_collection

    Returns:
        the new _id
    """
    insertion = mongo_collection.insert_one(kwargs)
    return insertion.inserted_id`
