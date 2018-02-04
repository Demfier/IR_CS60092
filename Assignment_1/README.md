# IR_CS60092

Please go through the following points to know the code structure for assignment 1 solution:
1. `Results.pdf` contains performance comparision for the 3 systems
2. `main.py` contains code for grep-based and index-based retrieval. `jsonify.py` and `build_inverted_index.py` are helper modules for them.
3. `evaluate.py` is the evaluation script for the three systems.
4. `lucene_index.py` contains code for index-based retrieval using lucene.

With an assumption that the user has an access to the `data` folder (having `alldocs/`, `query.txt` and `output.txt`), the systems can be generated via the following sequence of commands:

1. `mkdir output`
2. `python3 jsonify.py` : Generates `data/jsonified_data.json` where queries and ground truth are compiled in a single json.
3. `python3 build_inverted_index.py` : Generates `output/inverted_index.json` which is the inverted-index.
4. `python3 main.py` : Builds the Grep-based and Index-based IR models (`bool_retrieval_json_output.json`, `index_based_bool_retrieval.json`) and saves them in the `output` folder. Note: This takes sometime to finish as Grep-based model is quite slow.
5. `python lucene_index.py` : Builds the Index-based IR model using lucene and saves it in the `output` folder as `lucene_index_based_retrieval.json`.
6. `python3 evaluate.py` : Evaluates the IR models and show their performance (Precision, Recall, Total Search Time)
