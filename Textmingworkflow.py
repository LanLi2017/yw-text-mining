from nltk import word_tokenize
from nltk.corpus import stopwords
import re

from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
import gensim
import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer

"""
@begin topic_modeling @desc Workflow for topic modeling procedure
@param path @desc path of the input raw dataset
@param n_components @desc the number of topics
@param n_top_words @desc top words in topic
@out topic_log 
"""
def topic_modeling(path,n_components,n_top_words):

    """
    @begin read_file  @desc get the input raw file
    @param path
    @out doc
    """
    doc=read_file(path)
    """
    @end read_file
    """
    """
    @begin preprocessing @desc do data cleaning,tokenization ,removal of stop words
    @in stopwords 
    @in doc  @as doc
    @in regexr @desc regular expression filter
    @out clean_book
    """
    clean_book=preprocessing(doc)
    """
    @end preprocessing
    """
    """
    @begin tf_calculation @desc convert the text documents to a matrix of token counts
    @param clean_book @as clean_book @desc dataset after preprocessing
    @out tf @as TermFrequency @desc term frequency for the documents
    @out tf_vectorizer @desc a matrix of token counts
    """
    tf=tf_calculation(clean_book)[0]
    tf_vectorizer=tf_calculation(clean_book)[1]
    """
    @end tf_calculation
    """
    """
    @begin LatentDirichletAllocation @desc using the sciki-learn library to do LDA modeling
    @param n_components @as n_components
    @param tf @as tf
    @param tf_vectorizer @as tf_vectorizer
    @in max_iter @desc the maximum number of iterations
    @in learning_method @desc method used to update _component, only used in fit method
    @in learning_offset @desc a parameter that downweights early iterations in online learning
    @in random_state @desc random number generator 
    @out lda @desc output the lda model
    @out tf_feature_names 
    """
    lda=LatentDirichletAllocation(n_components=n_components, max_iter=5,
                                learning_method='online',
                                learning_offset=50.,
                                random_state=0)
    lda=lda.fit(tf)
    print("\nTopics in LDA model:")
    tf_feature_names=tf_vectorizer.get_feature_names()
    """
    @end LatentDirichletAllocation
    """
    """
    @begin print_top_words @desc print the topics with top words
    @param lda @as lda @desc LDA model
    @param tf_feature_names @as tf_feature_names
    @param n_top_words
    @out topic_log
    """
    topic_log=print_top_words(lda,tf_feature_names,n_top_words)
    return topic_log
    """
    @end print_top_words
    """
"""
@end topic_modeling
"""


"""
@begin read_file 
@param path @desc path for reading file
@return file @desc raw file before data preprocessing
"""

def read_file(path):
    doc=open(path,"r")
    file=str(doc.read())
    return file
"""
@end read_file
"""


en_stopwords=set(stopwords.words('english'))
de_stopwords=set(stopwords.words('german'))
fr_stopwords=set(stopwords.words('french'))
stopwords=en_stopwords|de_stopwords|fr_stopwords

"""
@begin preprocessing 
@in file @as file
@in stopwords 
@in regexr 
@return file_valid
"""
def preprocessing(file):
    file_tokens=word_tokenize(file.lower())
    clean_file=[word for word in file_tokens if word not in stopwords]
    regexr=re.compile('([a-z])\w+')
    file_valid=[w for w in clean_file if regexr.match(w)]
    return list(file_valid)


"""
@end preprocessing
"""

"""
@begin print_top_words
@param model 
@param feature_name
@param n_top_names
@return message
"""
def print_top_words(model,feature_name,n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        message="Topic #%d: " % topic_idx
        message+=" ".join([feature_name[i]
                           for i in topic.argsort()[:-n_top_words -1: -1]])
        print(message)
    print()

"""
@end print_top_words
"""

"""
@begin tf_calculation 
@param clean_book 
@return tf
@return tf_vectorizer
"""
def tf_calculation(clean_book):
    tf_vectorizer=CountVectorizer()
    tf=tf_vectorizer.fit_transform(clean_book)
    return tf,tf_vectorizer
"""
@end tf_calculation
"""

"""
@begin LDA 
@param clean_book
@param n_components
@param n_top_words
@return topic_log
"""
def LDA(clean_book,n_components,n_top_words):
    """
    @begin tf_calculation
    @param clean_book
    @out tf
    @out tf_vectorizer
    """
    tf=tf_calculation(clean_book)[0]
    tf_vectorizer=tf_calculation(clean_book)[1]
    """
    @end tf_calculation
    """

    """
    @begin LatentDirichletAllocation @desc using the sciki-learn library to do LDA modeling
    @param n_components @as n_components
    @param tf @as tf
    @param tf_vectorizer @as tf_vectorizer
    @in max_iter @desc the maximum number of iterations
    @in learning_method @desc method used to update _component, only used in fit method
    @in learning_offset @desc a parameter that downweights early iterations in online learning
    @in random_state @desc random number generator 
    @out lda
    @out tf_feature_names
    """
    lda=LatentDirichletAllocation(n_components=n_components, max_iter=5,
                                learning_method='online',
                                learning_offset=50.,
                                random_state=0)
    lda=lda.fit(tf)
    print("\nTopics in LDA model:")
    tf_feature_names=tf_vectorizer.get_feature_names()
    """
    @end LatentDirichletAllocation
    """

    """
    @begin print_top_words @desc print the topics with top words
    @param lda @as lda @desc LDA model
    @param tf_feature_names @as tf_feature_names
    @param n_top_names
    @return topic_log
    """
    for topic_idx, topic in enumerate(lda.components_):
        message="Topic #%d: " % topic_idx
        message+=" ".join([tf_feature_names[i]
                           for i in topic.argsort()[:-n_top_words -1: -1]])
        print(message)
    print()
    """
    @end print_top_words
    """
"""
@end LDA
"""


def main():
    topic_modeling("religious-and-philosophical-texts/book1.txt",n_components=10,n_top_words=20)


if __name__=='__main__':
    main()




