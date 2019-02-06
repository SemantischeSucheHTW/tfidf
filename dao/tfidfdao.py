class TF_IDF_DAO:

    #config must contain values for the keys "wordindex_collection" and "pagedetails_collection"
    def __init__(self, config):
        pass
    
    #returns all words and how often they occur (as dict)
    def getAllWordsWithCounts(self):
        pass
    
    #returns the total amount of documents
    def getTotalDocumentCount(self):
        pass
    
    #returns a cursor for a dict of the form {_id: words}
    def getWordsFromPagedetails(self):
        pass
    
    #returns pagedetails for a given url
    def getPageDetails(self, url):
        pass