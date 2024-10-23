#!/usr/bin/env python3
"""Contains a mongoDB query function"""


def schools_by_topic(mongo_collection, topic):
    """Returns a list of schools with the topic `topic`"""
    return mongo_collection.find({"topics": topic})
