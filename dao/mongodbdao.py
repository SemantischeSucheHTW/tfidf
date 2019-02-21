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

    def getAllWordsWithCounts(self):
        words_with_freqs = {}

        for doc in self.wortindex_collection.find({}):
            words_with_freqs[doc["word"]] = len(doc["urls_counts"])
            if doc["word"] == "mit":
                print("mit url count:", len(doc["urls_counts"]))
            if doc["word"] == "raub":
                print("raub url count:", len(doc["urls_counts"]))
            if doc["word"] == "die":
                print("die url count:", len(doc["urls_counts"]))

        return words_with_freqs
    
    def getTotalDocumentCount(self):
        return self.pagedetails_collection.count_documents({})
    
    def getWordsFromPagedetails(self):
        return list(self.pagedetails_collection.find({}, {"lemma_words":1}))
    
    def getPageDetails(self, url):
        details = list(self.pagedetails_collection.find({"_id":url}))
        if details:
            return details[0]
        else:
            return None