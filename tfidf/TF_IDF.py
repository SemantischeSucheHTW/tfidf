import numpy as np 

#README
#1. create an instance, this automatically builds the TF-IDF vector for every document
#2. call instance.getResultsForInput(...) or instance.getSimilarArticles(...)
class TF_IDF:
    
    #the dao need a connection to the collections wordindex and pagedetails
    def __init__(self, dao, verbose=True):
        self.dao = dao
        self.verbose=verbose
        
        self.term_idfs = None #terms are lemmatized
        self.doc_term_tfs = None #terms are not lemmatized!!??
        self.doc_term_tf_idfs = None #dict of dicts {documtent_id: {term: value}}
        
        self.calcTF_IDFs()
        
        
    def calcTerm_IDFs(self):
        term_idfs = {}

        self.n_docs = self.dao.getTotalDocumentCount() + 1
        term_count = self.dao.getAllWordsWithCounts()
    
        for term, count in term_count.items():
            term_idfs[term] = np.log10(self.n_docs / count)
            #term_idf[term] = self.n_docs / count
            
        self.term_idfs = term_idfs
    
    
    #takes a list of words
    #returns a dict {term: tf, ...}
    #throws an error if the wordlist is empty
    def getTermFrequencies(self, words):
        words_with_abs_counts = np.unique(words, return_counts=True)
        max_count = np.max(words_with_abs_counts[1])
        tfs = words_with_abs_counts[1]/max_count

        term_tf = dict(zip(words_with_abs_counts[0], tfs))
        return term_tf
    
    
    ###old implementation
    #takes a list of words
    #returns a dict {term: tf, ...}
    #throws an error if the wordlist is empty
    def getTermFrequencies_old(self, words):
        n_words = len(words)
        unique, counts = np.unique(words, return_counts=True)
        term_tf= dict(zip(unique, counts / n_words))
        return term_tf
    
    
    def calcDoc_Term_TFs(self):
        doc_term_tfs = {} #{documtent_id: {term: value}}

        for doc in self.dao.getWordsFromPagedetails():
            try:
                words = doc["words"]  #get list of words for each document
                
                term_tf = self.getTermFrequencies(words)
                
                doc_term_tfs[doc["_id"]] = term_tf
            except:
                if self.verbose:
                    print("TF-IDF module: initial TF calculation: article with url", {doc["_id"]}, "contains no words")
        self.doc_term_tfs = doc_term_tfs
    
    
    def calcTF_IDFs(self):
        self.calcTerm_IDFs()
        self.calcDoc_Term_TFs()

        doc_term_tf_idfs = {} #{documtent_id: {term: value}}

        no_idf_count = 0

        for document_id, term_value in self.doc_term_tfs.items():
            current_tf_idfs = {}
            for term, tf in term_value.items():
                try:
                    #take '{documtent_id: {term: value}}' from tfs and multiply every tf score with idf score for that document
                    current_tf_idfs[term] = tf*self.term_idfs[term] 
                except:
                    no_idf_count += 1
            doc_term_tf_idfs[document_id] = current_tf_idfs
        
        if self.verbose and no_idf_count:
            print("TF-IDF module: inital TF-IDF calculation: no idf for", {no_idf_count},"terms")
            
        self.doc_term_tf_idfs = doc_term_tf_idfs
        
        """c=0
        for i, a in self.tf_idfs.items():
            if c<10:
                print(i, ":", a)
                c+=1"""
    
    
    # input is a list of words
    def calcTF_IDF(self, user_input):
        
        try:
            term_tf = self.getTermFrequencies(user_input) 
        except:
            if self.verbose:
                print("TF-IDF module: user input TF calculation: input contains no words")
        
        tf_idfs = {}
        no_idf_count = 0
        for term, tf in term_tf.items():
            try:
                tf_idfs[term] = tf*self.term_idfs[term]
            except:
                no_idf_count += 1
                if self.verbose:
                    print("TF-IDF module: user input TF-IDF calculation: word", {term}, "in query is not in db")
                
        return tf_idfs
    
    
    #user_input: list of input words (lowercase)
    #possible_docids: hand over a preselection of urls, the results will be based on that
    #n_results: how many results do you want?
    #return sims: also return similarities?
    #min_sim: is an article required to have a minimum similarity to the input?
    #returns a list of urls (and if requested a list of tuples(url, sim), cosine similarity is used)
    def getResultsForInput(self, user_input, possible_docids=None, n_results=None, return_sims=False, min_sim=None):
        input_term_tfidfs = self.calcTF_IDF(user_input)

        keys_a = set(input_term_tfidfs.keys())

        sims = []

        #determines cos similarity between input and every document in the database
        for docid, doc_term_tfidfs in self.doc_term_tf_idfs.items():

            #only calculate cosine sim for candidate documents
            if (not possible_docids) or (docid in possible_docids):
                keys_b = set(doc_term_tfidfs.keys())
                intersection = keys_a & keys_b    #common words of input and respective document
                if intersection:# and len(intersection)>min_equal_words:
                    a = [] #tfidf values for respective document
                    b = [] #tfidf values for input
                    for key in intersection:
                        a.append(doc_term_tfidfs[key])
                        b.append(input_term_tfidfs[key])

                    scalar_product = np.dot(a, b)
                    d_a = np.linalg.norm(list(input_term_tfidfs.values()))
                    d_b = np.linalg.norm(list(doc_term_tfidfs.values()))

                    sim = scalar_product/(d_a*d_b)

                    #only add documents that meet the similarity requirement
                    if min_sim:
                        if sim >= min_sim:
                            sims.append((docid, sim))
                    else:
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
        
    def getSimilarArticles(self, url, n_results=2, return_sims=False, min_sim=0.2):
        words = self.dao.getPageDetails(url)["words"]
        return self.getResultsForInput(words, n_results=n_results, return_sims=return_sims, min_sim=min_sim)[1:]