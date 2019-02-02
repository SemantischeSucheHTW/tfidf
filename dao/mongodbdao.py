from pymongo import MongoClient

class MongoDBDao:

    def __init__(self, config):

        c_copy = dict(config)
        db = c_copy.pop("db")
        wordindex_collection = c_copy.pop("wordindex_collection")
        pagedetails_collection = c_copy.pop("pagedetails_collection")

        self.client = MongoClient(**c_copy)
        self.db = self.client[db]
        self.wortindex_collection = self.db[wordindex_collection]
        self.pagedetails_collection = self.db[pagedetails_collection]

    def getAllWordsWithCounts(self):
        words_with_freqs = {}

        for doc in self.wortindex_collection.find({}):
            words_with_freqs[doc["word"]] = len(doc["urls_counts"])

        return words_with_freqs
    
    def getDocumentCount(self):
        return self.pagedetails_collection.count_documents({})