import os
import textract
import cPickle as pickle
from sys import stdout

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

#get current working directory
def get_cwd():
    cwd = os.getcwd()
    return cwd

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
#convert doc to txt, input doc - path to document, output - txt, raw text
def convert(doc):
    text = textract.process(doc)
    return text

#idea from stackoverflow, progres bar
def progress(count, total, suffix=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
    stdout.flush()


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

#changing results to list
def list_results_docs(docs, results):
    res = []
    for n in results:
        res.append(docs[n])
    return res

#saving program data
def save_state(dirs, doctypes, docs, txts, datadir, vectorizer, vec):
    data  = (dirs, doctypes, docs, txts, datadir, vectorizer, vec)
    pickle.dump(data, open("docSearcherData.p", "wb"))

#loading program data
def load_state():
    loaded = pickle.load(open("docSearcherData.p", "rb"))
    return loaded
