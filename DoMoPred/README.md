# Web Interface for DoMo-Pred 

## About

This folder stores `the original DoMo-Pred source code` but with some changes for web interface. All changed files you can find in `Changes` section. And due to the size limitS of Github repo, there are some database files are not included here. You can download it from `Additional Source` section (We also use Github LFS to manage it, you can also get it via LFS).

The original README of DoMo-Pred has been renamed as `oldREADME` in the root of this folder

## Changes

Modified these files  for web interface support:

* `run_pipeline.py`
* `run_protein.py`
* `run_peptide.py`

Moved these files/folders to data folder in upper directory:

* `pwm_dir`
* `domain.txt`

Deleted files below for redundant:

* `out_dir`



## Additional Source

Files below are the database files needed for DoMO-Pred, to make this web interface run without exceptions, you have to download files below, and put them into proper directories.

__Example:__`filename`:`target directory`

* __`contingency.npy`__:`DoMoPred/Protein/Db/contingency.npy`
* __`profile_binary.npz`__:`DoMoPred/Protein/Db/profile_binary.npz`
* __`signatcount.npy`__:`DoMoPred/Protein/Db/signatcount.npy`

You can get those thress files from here: [Google Drive](https://drive.google.com/drive/folders/0B1wYCRysoEhza1J0WmVHM3VNWmM?usp=sharing)

