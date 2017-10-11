from sklearn.feature_extraction.text import TfidfVectorizer as tfidf
import Stemmer
from sklearn.neighbors import NearestNeighbors

#create corpus, input - list of .txts in ./data, output - list of string,
def create_corpus(txts):
    corpus=[]
    for i in range(len(txts)):
        txt = open(txts[i])
        corpus.append(txt.read())
    return corpus
    #new class to stemm and tfidf a corpus
class StemmedTfidfVectorizer(tfidf):
    def build_analyzer(self):
        analyzer = super(tfidf, self).build_analyzer()
        return lambda doc: (stemmer.stemWord(w) for w in analyzer(doc))
#create base on StemmedTfidfVectorizer, atribiutes: ngram_range, default (1,2), fit and transform on data in corpus,
#return fitted vectorizer and sparse matrix with tf-idf document weights as in sklearn fit_transform() method
def create_vectorizer(corpus, ngram_range=(1,2)):
    initialize_stemmer()
    vectorizer = StemmedTfidfVectorizer(decode_error="ignore", strip_accents="unicode", analyzer='word',
                                     ngram_range=ngram_range, stop_words="english", lowercase=True)
    vec = vectorizer.fit_transform(corpus)
    return vectorizer, vec

#initialize stemmer
def initialize_stemmer():
    global stemmer
    stemmer = Stemmer.Stemmer('en')

#transform query, as in sklearn .transform(), return sparse matrix
def transform_query(text, vectorizer):
    initialize_stemmer()
    query = vectorizer.transform(text)
    return query

#create and fit unsupervised learner for neighbor searches, input sparse matrix from tiidf
def nbrs(vec):
    nbrs = NearestNeighbors(algorithm='auto')
    nbrs.fit(vec)
    return nbrs

#search for nearest neighbour for query, n - number of neighbors to return
def search(query, nbrs, n=10):
    results = nbrs.kneighbors(query, n)[1][0]
    return results
