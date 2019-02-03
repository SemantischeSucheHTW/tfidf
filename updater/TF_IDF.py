import numpy as np 

class TF_IDF:
    
    def __init__(self, dao):
        self.dao = dao
        self.term_idf = None
        self.doc_tfs = None
        self.tf_idfs = None
        
    def calcTerm_IDF(self):
        term_idf = {}

        self.n_docs = self.dao.getDocumentCount()
        term_count = self.dao.getAllWordsWithCounts()
    
        for term, count in term_count.items():
            term_idf[term] = np.log10(self.n_docs / count)
            #term_idf[term] = self.n_docs / count
            
        self.term_idf = term_idf
    
    def calcDoc_Term_TF(self):
        doc_tfs = {} #{documtent_id: {term: value}}

        for doc in self.dao.pagedetails_collection.find({}, {"words":1}):
            try:
                words = doc["words"]
                n_words = len(words)

                unique, counts = np.unique(words, return_counts=True)
                term_tf= dict(zip(unique, counts / n_words))
                doc_tfs[doc["_id"]] = term_tf
            except:
                print("TF-IDF calculation: article contains no words")
        self.doc_tfs = doc_tfs
                
    def calcTF_IDFs(self):
        self.calcTerm_IDF()
        self.calcDoc_Term_TF()

        tf_idfs = {} #{documtent_id: {term: value}}

        no_idf_count = 0

        for document_id, term_value in self.doc_tfs.items():
            c_tf_idfs = {}
            for term, tf in term_value.items():
                try:
                    c_tf_idfs[term] = tf*self.term_idf[term] #take '{documtent_id: {term: value}}' from tfs and multiply every tf score with idf score for that document
                except:
                    no_idf_count += 1
            tf_idfs[document_id] = c_tf_idfs
        
        self.tf_idfs = tf_idfs
        
        """c=0
        for i, a in self.tf_idfs.items():
            if c<10:
                print(i, ":", a)
                c+=1"""
    
    
    # input is a list of words
    def calcTF_IDF(self, user_input):
        n_words = len(user_input)
        
        unique, counts = np.unique(user_input, return_counts=True)
        term_tf = dict(zip(unique, counts / n_words))
        
        tf_idfs = {}
        no_idf_count = 0
        for term, tf in term_tf.items():
            try:
                tf_idfs[term] = tf*self.term_idf[term]
            except:
                no_idf_count += 1
                
        return tf_idfs
    
    def getResultsForInput(self, user_input, possible_docids=None, n_results=None, return_sims=False):
        tf_idf_input = self.calcTF_IDF(user_input)

        keys_a = set(tf_idf_input.keys())

        sims = []

        #determines cos similarity between input and every document in the database
        for docid, term_tf_idfs in self.tf_idfs.items():

            #only calculate cosine sim for candidate documents
            if (not possible_docids) or (docid in possible_docids):
                keys_b = set(term_tf_idfs.keys())
                intersection = keys_a & keys_b    #common words of input and respective document
                if intersection:
                    a = [] #tfidf values for respective document
                    b = [] #tfidf values for input
                    for key in intersection:
                        a.append(term_tf_idfs[key])
                        b.append(tf_idf_input[key])

                    scalar_product = np.dot(a, b)
                    d_a = np.linalg.norm(list(tf_idf_input.values()))
                    d_b = np.linalg.norm(list(term_tf_idfs.values()))

                    sim = scalar_product/(d_a*d_b)

                    sims.append((docid, sim))
        
        sims_sorted = sorted(sims, key=lambda x: x[1])[::-1]
        
        #possibly only return urls
        if not return_sims:
            sims_sorted = [s[0] for s in sims_sorted]
        
        
        #return all results, when there is no requested amount
        if not n_results:
            return sims_sorted
        
        #return all results, when there are less than requested
        if len(sims_sorted)<n_results:
            return sims_sorted
        else:   #return the specified amount of results
            return sims_sorted[:n_results]