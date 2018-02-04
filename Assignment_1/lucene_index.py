"""
Title: IR Assignment 1 Solution
Name: Gaurav Sahu
Roll number: 14MF10008
"""

import sys
import json
import time

import lucene
from os import path, listdir
from java.io import File
from org.apache.lucene.document import Document, Field, StringField, TextField
from org.apache.lucene.util import Version
from org.apache.lucene.store import RAMDirectory, SimpleFSDirectory

# Indexer imports:
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import IndexWriter, IndexWriterConfig
# from org.apache.lucene.store import SimpleFSDirectory

# Retriever imports:
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser

# ---------------------------- global constants ----------------------------- #

BASE_DIR = path.dirname(path.abspath(sys.argv[0]))
INPUT_DIR = BASE_DIR + "/data/alldocs/"
INDEX_DIR = BASE_DIR + "/output/lucene_index/"

# --------------------------------------------------------------------------- #
#                    ___           _                                          #
#                   |_ _|_ __   __| | _____  _____ _ __                       #
#                    | || '_ \ / _` |/ _ \ \/ / _ \ '__|                      #
#                    | || | | | (_| |  __/>  <  __/ |                         #
#                   |___|_| |_|\__,_|\___/_/\_\___|_|                         #
#                                                                             #
# --------------------------------------------------------------------------- #


def create_document(file_name):
    """
    This method returns a document which afterwards can be added to the
    IndexWriter.
    """
    path = INPUT_DIR+file_name  # assemble the file descriptor
    file = open(path)  # open in read mode
    doc = Document()  # create a new document
    # add the title field
    doc.add(StringField("title", input_file, Field.Store.YES))
    # add the whole book
    doc.add(TextField("text", file.read(), Field.Store.YES))
    file.close()  # close the file pointer
    return doc

# Initialize lucene and the JVM
lucene.initVM()
directory = SimpleFSDirectory(File(INDEX_DIR))

# Get and configure an IndexWriter
analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
config = IndexWriterConfig(Version.LUCENE_CURRENT, analyzer)
writer = IndexWriter(directory, config)

print "Number of indexed documents: %d\n" % writer.numDocs()
for input_file in listdir(INPUT_DIR):  # iterate over all input files
    print "Current file:", input_file
    doc = create_document(input_file)  # call the create_document function
    writer.addDocument(doc)  # add the document to the IndexWriter

print "\nNumber of indexed documents: %d" % writer.numDocs()
writer.close()
print "Indexing done!\n"
print "------------------------------------------------------"


# --------------------------------------------------------------------------- #
#                    ____      _        _                                     #
#                   |  _ \ ___| |_ _ __(_) _____   _____ _ __                 #
#                   | |_) / _ \ __| '__| |/ _ \ \ / / _ \ '__|                #
#                   |  _ <  __/ |_| |  | |  __/\ V /  __/ |                   #
#                   |_| \_\___|\__|_|  |_|\___| \_/ \___|_|                   #
#                                                                             #
# --------------------------------------------------------------------------- #

def lucene_index_based_retrieval(searcher, analyzer):
    """
    Asks the user for query strings and will show the corresponding result
    """
    with open('data/jsonified_data.json') as dataFile:
        input_data = json.load(dataFile)

    for qid in input_data:
        command = input_data[qid]['input_query']
        query = QueryParser(Version.LUCENE_CURRENT,
                            "text", analyzer).parse(command)

        start = time.clock()
        scoreDocs = searcher.search(query, 50).scoreDocs
        duration = time.clock() - start

        result = []
        for scoreDoc in scoreDocs:
            doc = searcher.doc(scoreDoc.doc)
            result.append(doc.get("title"))

        input_data[qid]['system_response'] = result
        input_data[qid]['time_taken'] = duration
        print("query {0} ({1} seconds) => {2}".format(qid,
                                                      duration,
                                                      result))

    with open('output/lucene_index_based_retrieval.json', 'w') as json_output:
        json.dump(input_data, json_output)
    return(True)


# Create a searcher for the above defined Directory
searcher = IndexSearcher(DirectoryReader.open(directory))

# Create a new retrieving analyzer
analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)

# ... and start searching!
lucene_index_based_retrieval(searcher, analyzer)

# ----------------------------------- EOF ----------------------------------- #
