# docSearcher
Helps you search for the most similar documents in your collection. As an input docSearcher takes simple string query or whole document. Similarity is based on term frequency–inverse document frequency uni- and bigrams, measured by nearest neighbor search. It's great tool if you have large collection of articles and want to search them for bibliography or just found something interesting on web and want to check your resources on that topic.

<h2>Usage</h2>
initial use should look like this:

python docSearcher.py [-i] [-dirs DIRECTORIES [DIRECTORIES ...]] [-dt  [...]]

setting -i agrument take script to init mode where it search the [-dirs] directories for documents of [-dt] doctypes.
docSearcher is using textract (http://textract.readthedocs.io/en/stable/) to convert documents, so every file that textract can handle could be an input to docSearcher.

search use: 

python docSearcher.py [-d DOCUMENT | -q QUERY [QUERY ...]] [-n NUMBER]

docSearcher can either search using -q followed by string query or using document -d argument followed with path-to-file, the -n argument is used to set the number of results shown, default is 10.

<h2>Requirements</h2>
docSearcher is using python 2.7, textract to convert documents for raw text, PyStemmer to stemm words and sklearn Tfidf vectorizer and nearest neighbor to search fo similarity. Install them by running:

pip install -r requirements.txt


