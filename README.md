<h1> docSearcher </h1>
Handy script that lets you search through your own collections of documents, such as articles, books, scans and so on, to find most similar ones to your search query. As a query you can use simple string, group of strings, sentence, paragraph or whole document. It's great tool when you need to get bibliography when writing a paper, making a presentation or you just found some interesting article on the web and remember you have something on that topic but couldn't remember where you put it or how the file was named. Moreover docSearcher looks into documents, so it solves the problem of files named like "nfjsfdsheio.pdf" or "00432523scan.jpg".

docSearcher currently works best with documents in english, due to stemmer setting.
<h2>Usage</h2>
Using docSearcher for the first time use the -i option so script can scan and analyze your documents


*python docSearcher.py [-i] [-dirs DIRECTORIES [DIRECTORIES ...]] [-dt  [...]]*

setting -i agrument take script to init mode where it search the [-dirs] directories for documents of [-dt] doctypes. Next the script will convert these documents to .txt format and store them in newly created */data* folder. Txt's will then be *stemmed* and fitted to *term frequency-invert document frequency*. In result all processed data will be saved in *"docSearcherdata.p"* file, and loaded when search commence. This operation, -i, should be done every time you add or remove document files and want the docSearcher to recognize changes.

example:

*python docSearcher.py -i -dirs /home/user/Documents/folder1  /home/user/Documents/folder2  /home/user/Documents/folder3 -dt .pdf .jpg*

Searching for documents can be done by:

*python docSearcher.py [-d DOCUMENT | -q QUERY [QUERY ...]] [-n NUMBER]*

docSearcher can either search using -q followed by string query or by using document -d argument followed with path-to-file; the -n argument is used to set the number of results shown, default is 10.

Example using -q:

*python docSearcher.py -q foo foo2 bar barbar baar*

will result in searching for documents with most occurrence of words "foo" "foo2" "bar" "barbar" "baar".

Example using -d:

*python docSearcher.py -d /home/user/Documents/searchMe.pdf*

will results in searching for documents most similar to one provided as search query.

<h2>Requirements</h2>
docSearcher relay on [textract](https://github.com/deanmalmgren/textract) for handling document conversion, [sklearn](http://scikit-learn.org/stable/) for tf-idf vectorization and [PyStemmer](https://github.com/snowballstem/pystemmer) for word stemming

install required libraries by typing:

pip install -r requirements.txt
