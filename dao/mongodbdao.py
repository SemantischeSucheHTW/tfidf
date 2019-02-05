from pymongo import MongoClient
from dao.tfidfdao import TF_IDF_DAO

class MongoDBDao(TF_IDF_DAO):

    def __init__(self, config):
        c_copy = dict(config)
        db = c_copy.pop("db")
        wordindex_collection = c_copy.pop("wordindex_collection")
        pagedetails_collection = c_copy.pop("pagedetails_collection")

        self.client = MongoClient(**c_copy)
        self.db = self.client[db]
        self.wortindex_collection = self.db[wordindex_collection]
        self.pagedetails_collection = self.db[pagedetails_collection]

    #returns all words and how often they occur (as dict)
    def getAllWordsWithCounts(self):
        words_with_freqs = {}

        for doc in self.wortindex_collection.find({}):
            words_with_freqs[doc["word"]] = len(doc["urls_counts"])

        return words_with_freqs
    
    #returns the total amount of documents
    def getDocumentCount(self):
        return self.pagedetails_collection.count_documents({})
    
    #returns a cursor for a dict of the form {_id: words}
    def getWordsFromPagedetails(self):
        return self.pagedetails_collection.find({}, {"words":1})
    
    #returns pagedetails for a given url
    def getPageDetails(self, url):
        return self.pagedetails_collection.find({"_id":url})