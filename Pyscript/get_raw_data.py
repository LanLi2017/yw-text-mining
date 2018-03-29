# @begin get_raw_data
# @param path @uri file:https://www.kaggle.com/tentotheminus9/religious-and-philosophical-texts/downloads/religious-and-philosophical-texts.zip
# @out raw_data @desc raw file before data pre-process
import urllib.request

# @begin download_file @uri file:https://docs.python.org/3.0/library/urllib.request.html#urllib.request.urlretrieve
# @param path @uri file: https://www.kaggle.com/tentotheminus9/religious-and-philosophical-texts/downloads/religious-and-philosophical-texts.zip
# @out local_file @desc store the file at the local path
path="https://www.kaggle.com/tentotheminus9/religious-and-philosophical-texts/downloads/religious-and-philosophical-texts.zip"
local_file=urllib.request.urlretrieve(path,'/Users/BarbaraLee/Downloads/text_tempo/dataset.zip')
# @end download_file

# @begin read_file
# @in local_file @uri file:/local/Downloads/file_name.txt
# @out raw_data
doc=open('/Users/BarbaraLee/Downloads/religious-and-philosophical-texts/book1.txt')
raw_data=str(doc.read())

# @end read_file

# @end get_raw_data

