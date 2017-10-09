import os
import textract
import cPickle as pickle
from sklearn.feature_extraction.text import TfidfVectorizer as tfidf
import Stemmer
from sklearn.neighbors import NearestNeighbors
import argparse

types = [".csv", ".doc", ".docx", ".eml", ".epub", ".gif", ".jpg", ".jpeg", ".json", ".html", ".mp3", ".msg", ".odt", ".ogg",
".pdf", ".png", ".pptx", ".rtf", ".tiff", ".txt", ".wav", ".xlsx", ".xls"]

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument("-d", "--document", help="use document as search query, insert path", type=str)
group.add_argument("-q","--query", help="search query", type=str, nargs='+')
parser.add_argument("-n", "--number", help="number of search result to show", type=int, default=10)
parser.add_argument("-i", "--init", help="initiate data gethering and processing", action="store_true")
parser.add_argument("-dirs", "--directories", help="direcotires to search for documents", nargs='+', type=str)
parser.add_argument("-dt", "--doctypes", help="document types that can be processed", nargs='+', type=str, choices=types, metavar='')
args = parser.parse_args()

#create datadir in root/data and return path to it
def create_datadir():
    cwd = os.getcwd()
    datadir = cwd+"/data"
    if not os.path.exists(datadir):
        os.makedirs(datadir)
    return datadir

#check for saved data
def check_saved_data():
    if 'docSearcherData.p' in os.listdir(os.getcwd()):
        return True
    else:
        return False

#checking dirs for documents specified in doctypes list (eg. .pdf, .doc, .jpg), return list of founded docs (paths)
def get_docs(dirs, doctypes):
    docs = []
    for d in dirs:
        for filename in os.listdir(d):
            for doctype in doctypes:
                if filename.endswith(doctype):
                    doc = d+"/"+filename
                    docs.append(doc)
    return docs

#convert file path to filname ,input a doc from docs list, return a string name
def filename(doc):
    d = d = doc.split("/")
    name = d[-1].partition(".")[0]
    return name

#write doc (from docs list) and text from textract to .txt file in datadir, return txt name with full path
def txt_write(doc, text, datadir):
    name = filename(doc)
    txt = datadir+"/"+name+".txt"
    f = open(txt, "w")
    f.write(text)
    return txt


#idea from stackoverflow, progres bar
from sys import stdout

def progress(count, total, suffix=''):
    bar_len = 100
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
    stdout.flush()
    
#convert doc to txt, input doc - path to document, output - txt, raw text 
def convert(doc):
    text = textract.process(doc)
    return text

#convert document from docs[] to txt and store them in ./data, return 2 list, txts[] with path to created txt files
#and fails[] with path to documents that failed to convert
def convert_docs(docs, datadir):
    txts = []
    fails = []   
    for doc in docs:
        progress(docs.index(doc), len(docs)) 
        try:
            text = convert(doc)
            txt = txt_write(doc, text, datadir)
            txts.append(txt)
        except (UnicodeDecodeError, TypeError):
            fails.append(doc)
            pass
    return (txts, fails)

#saving program data
def save_state(dirs, doctypes, docs, txts, datadir, vectorizer, vec):
    data  = (dirs, doctypes, docs, txts, datadir, vectorizer, vec)
    pickle.dump(data, open("docSearcherData.p", "wb"))

#loading program data
def load_state():
    loaded = pickle.load(open("docSearcherData.p", "rb"))
    return loaded

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
    vectorizer = StemmedTfidfVectorizer(decode_error="ignore", strip_accents="unicode", analyzer='word', 
                                     ngram_range=ngram_range, stop_words="english", lowercase=True)
    vec = vectorizer.fit_transform(corpus)
    return vectorizer, vec

#transform query, as in sklearn .transform(), return sparse matrix 
def transform_query(text, vectorizer):
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

def list_results_docs(docs, results):
    res = []
    for n in results:
        res.append(docs[n])
    return res

#initialize stemmer
stemmer = Stemmer.Stemmer('en')

#initial data gathering and processing
def init():
    datadir = create_datadir()
    print("collecting documents")
    docs = get_docs(dirs, doctypes)
    print("converting founded documents")
    txts, fails = convert_docs(docs, datadir)
    print("creating corpus")
    corpus = create_corpus(txts)
    print("vectorizing corpus")
    vectorizer, vec = create_vectorizer(corpus)
    print("saving data")
    save_state(dirs, doctypes, docs, txts, datadir, vectorizer, vec)

if args.init and args.directories and args.doctypes is None:
	parser.error("--init requires --directories and --doctypes")
elif args.init:
    dirs = args.directories
    doctypes = args.doctypes
    init()

if args.document or args.query:
    if check_saved_data():
	    print("saved data found, now loading..")
	    dirs, doctypes, docs, txts, datadir, vectorizer, vec =load_state()
    else:
	    print("saved data not found, please use --init option")

    nn = nbrs(vec)
    stemmer = Stemmer.Stemmer('en')

    if args.document:
	    query = convert(args.document)
    else:
	    query = args.query
    query = transform_query(query, vectorizer)
    if args.number:
	    n = args.number
	    r = search(query, nn, n)
    else:
        r = search(query, nn)
    results = list_results_docs(docs, r)
    print(" ")
    print("Founded documents: ")
    for result in results:
	     print result
