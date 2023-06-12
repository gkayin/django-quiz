from django.db import models
from django.contrib.auth.models import User

from pymongo import MongoClient

class Levelup(models.Model):
    title = models.CharField(max_length=100)
    memo = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class MongoConnection(object):

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client['localdb']

class MongoCollection(MongoConnection):
    """A Generic Mongo Object class with common methods for querying MongoDB collections.
    """
    def __init__(self, collection):
        """
        :param collection:  The MongoDB collection to query against.
        """
        super(MongoCollection, self).__init__()
        self._collection = self.db[collection]