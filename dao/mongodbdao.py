from pymongo import MongoClient

from dao.indexdao import IndexDao


class MongoDBDao(IndexDao):

    def __init__(self, config):

        c_copy = dict(config)
        db = c_copy.pop("db")
        wordindex_collection = c_copy.pop("wordindex_collection")
        pagedetails_collection = c_copy.pop("pagedetails_collection")

        self.client = MongoClient(**c_copy)
        self.db = self.client[db]
        self.wortindex_collection = self.db[wordindex_collection]
        self.pagedetails_collection = self.db[pagedetails_collection]

    def getUrlsAndCountsfromKey(self, searchKey):
        assert isinstance(searchKey, str)
        docs = self.wortindex_collection.find({ "word": searchKey.lower() })
        urls_counts = []
        for doc in docs:
            for url_count in doc["urls_counts"]:
                urls_counts.append( (url_count["url"], url_count["count"]) )

        return urls_counts

    def getAllWordsWithCounts(self):
        words_with_freqs = {}

        for doc in self.wortindex_collection.find({}):
            words_with_freqs[doc["word"]] = len(doc["urls_counts"])

        return words_with_freqs
    
    def getDocumentCount(self):
        return self.pagedetails_collection.count_documents({})
    
    
    
    
    
    
    
    
    def get_all(self):
        d = {}
        for l in self.words_by_length_collection.find({}):
            d[l["len"]]=l["words"]
        return d
        
    def delete_all(self):
        self.words_by_length_collection.delete_many({})
        