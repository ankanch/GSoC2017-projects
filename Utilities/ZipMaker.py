import os
import zipfile

def make_zip(source_dir, output_filename):
    """
    the source dir and output dir cannot be the same one, or there is possibility that 
    it will run into a recursive problem, cost disk space. 
    """
    zipf = zipfile.ZipFile(output_filename, 'w')    
    pre_len = len(os.path.dirname(source_dir))
    for parent, dirnames, filenames in os.walk(source_dir):
        for filename in filenames:
            pathfile = os.path.join(parent, filename)
            arcname = pathfile[pre_len:].strip(os.path.sep)    
            zipf.write(pathfile, arcname)
    zipf.close()