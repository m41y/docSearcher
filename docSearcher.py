import argparse
import data_utils as du
import file_utils as fu
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

#initial data gathering and processing
def init():
    datadir = fu.create_datadir()
    print("collecting files")
    docs = fu.get_docs(dirs, doctypes)
    print("converting founded documents")
    txts, fails = fu.convert_docs(docs, datadir)
    if fails:
        print("Failed to convert these documents: ")
        for fail in fails:
            print fail
    print("creating corpus")
    corpus = du.create_corpus(txts)
    print("vectorizing corpus")
    vectorizer, vec = du.create_vectorizer(corpus)
    print("saving data")
    fu.save_state(dirs, doctypes, docs, txts, datadir, vectorizer, vec)

if args.init and args.directories and args.doctypes is None:
	parser.error("--init requires --directories and --doctypes")
elif args.init:
    dirs = args.directories
    doctypes = args.doctypes
    init()

if args.document or args.query:
    if fu.check_saved_data():
	    print("now loading..")
	    dirs, doctypes, docs, txts, datadir, vectorizer, vec = fu.load_state()
    else:
	    print("saved data not found, check folder or use --init option")
    nn = du.nbrs(vec)
    if args.document:
	    query = fu.convert(args.document).split()
    else:
	    query = args.query
    query = du.transform_query(query, vectorizer)
    if args.number:
	    n = args.number
	    r = du.search(query, nn, n)
    else:
        r = du.search(query, nn)
    results = fu.list_results_docs(docs, r)
    print(" ")
    print("Founded documents: ")
    for result in results:
	     print result
