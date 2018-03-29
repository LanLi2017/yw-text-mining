from nltk import word_tokenize
from nltk.corpus import stopwords
import re
from Pyscript.get_raw_data import raw_data

# @begin pre_process @desc pre-process the data, do data cleaning,tokenization,filter
# @in raw_data
# @in stopwords
# @in regexr @as regular_expression
# @out file_valid

# @begin tokenization @desc using NLTK word_tokenize to do tokenization
# @in raw_data
# @out file_tokens @desc the file after tokenization
file=raw_data
file_tokens=word_tokenize(file.lower())
# @end tokenization

# @begin stopwords_removal @desc remove the stopwords from the file
# @in stopwords @uri file:http://www.nltk.org/book/ch02.html
# @in file_tokens
# @out clean_file
en_stopwords=set(stopwords.words('english'))
de_stopwords=set(stopwords.words('german'))
fr_stopwords=set(stopwords.words('french'))
stopwords=en_stopwords|de_stopwords|fr_stopwords

clean_file=[word for word in file_tokens if word not in stopwords]
# @end stopwords_removal

# @begin filter_rules @desc using regular expression to filter the other data format
# @in regexr @as regular_expression
# @in clean_file
# @out file_valid @desc output the valid file
regexr=re.compile('([a-z])\w+')
file_valid=[w for w in clean_file if regexr.match(w)]
# @end filter_rules

# @end pre_process
