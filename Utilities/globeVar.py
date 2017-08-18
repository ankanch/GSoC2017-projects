# this file defines some globe variables used for web interface

# file paths, below is some import files' path

VAR_PATH_PROTEIN_ID_DATABASE = "./DoMoPred/Protein/Db/map_sgd.txt"  # this file is all the ids for the system will work
VAR_PATH_PWMS = "./data/pwm_dir/"
VAR_PATH_UPLOAD_FOLDER = "./Cache"
VAR_PATH_RESULT_FOLDER = "./Cache"  
VAR_PATH_IREFWEB_ALL = "./data/irefweb_all.pos"

# this dict defines the map of features name and feature code
# features' name are in index.html , their codes are in run_protein.py
# dict below includes features in PWMs and PPI-Pred
VAR_FEATURES = {
    "cellular_location":"A",    # features belongs to PPI-Pred
    "biological_process":"B",
    "molecular_function":"C",
    "gene_expression":"D",
    "sequence_signature":"E",
    "protein_expression":"F",
    "disorder":"L",             # features from here are belongs to PWMs
    "surface":"M",
    "peptide":"N",
    "structure":"O"
}

# result types describes how to dispaly the result to user 
VAR_RESULTTYPE_TABULAR = "tabular"
VAR_RESULTTYPE_TEXT = "text"
VAR_RESULTTYPE_COLOR = "color"

