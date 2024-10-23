#!/usr/bin/env python3
"""Contains a function for listing MongoDB documents"""


def list_all(mongo_collection):
    """Returns all documents in the given MongoDB collection"""
    cursor = mongo_collection.find({})
    if cursor.collection.estimated_document_count():
        return cursor
    return []
