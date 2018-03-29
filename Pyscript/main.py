# @begin topic_modeling
# @param path
# @in stopwords
# @in regular_expression
# @in max_iter @as max_iteration
# @in random_state
# @in learning_method
# @in learning_offset
# @out topic_log
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

# @begin LDA
# @in file_valid @desc file after pre_process procedure
# @param n_components
# @param n_top_words
# @in random_state
# @in max_iter @as max_iteration
# @in learning_method
# @in learning_offset
# @out topic_log


# @begin tf_calculation @desc using CountVectorizer from sklearn library to calculate the term frequency
# @in file_valid @desc file after pre_process
# @out tf @as term_frequency
# @out tf_vectorizer @as term_frequency_vectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer


from Pyscript.preprocess_data import file_valid

tf_vectorizer=CountVectorizer()
tf=tf_vectorizer.fit_transform(file_valid)
# @end tf_calculation

# @begin LatentDirichletAllocation @desc using the sciki-learn library to do LDA modeling
# @param n_components
# @param tf @as term_frequency
# @param tf_vectorizer @as term_frequency_vectorizer
# @in max_iter @desc the maximum number of iterations
# @in learning_method @desc method used to update _component, only used in fit method
# @in learning_offset @desc a parameter that down weights early iterations in online learning
# @in random_state @desc random number generator
# @out lda @as LDA_model
# @out tf_feature_names @as TermFrequency_feature_names
n_components=10
lda=LatentDirichletAllocation(n_components=n_components, max_iter=5,
                                learning_method='online',
                                learning_offset=50.,
                                random_state=0)
lda=lda.fit(tf)
print("\nTopics in LDA model:")
tf_feature_names=tf_vectorizer.get_feature_names()

# @end LatentDirichletAllocation

# @begin print_top_words @desc print the topics with top words
# @in lda @as LDA_model @desc LDA model
# @in tf_feature_names @as TermFrequency_feature_names
# @param n_top_words
# @out topic_log
n_top_words=20
for topic_idx, topic in enumerate(lda.components_):
    topic_log="Topic #%d: " % topic_idx
    topic_log+=" ".join([tf_feature_names[i]
                       for i in topic.argsort()[:-n_top_words -1: -1]])
    print(topic_log)
print()
# @end print_top_words

# @end LDA

# @end topic_modeling
