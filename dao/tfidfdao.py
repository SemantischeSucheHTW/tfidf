class TF_IDF_DAO:

    #config must contain values for the keys "wordindex_collection" and "pagedetails_collection" ...
    #... and db information (host, db, username, password)
    def __init__(self, config):
        pass
    
    #returns all words and how often they occur (as dict)
    def getAllWordsWithCounts(self):
        pass
    
    #returns the total amount of documents
    def getTotalDocumentCount(self):
        pass
    
    #returns a list of dicts of the form {_id: words}
    def getWordsFromPagedetails(self):
        pass
    
    #returns a pagedetails dict for a given url
    #returns None if there are no pagedetails for the given url
    def getPageDetails(self, url):
        pass