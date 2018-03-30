# @begin topic_modeling @desc Exercise YW for Analysing Text with NLTk
# @in Static_text @uri file:book1.txt
# @out Topicmodeling_Result @desc log file which contains the topics @uri file:output.txt


from nltk import word_tokenize, re
from nltk.corpus import stopwords
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer

# @begin AccessText @desc To read the text data from book1.txt file
# @in text_data_path @as Static_text @desc Text file which contains static text data @uri file:book1.txt
# @out text_file @as TextRead
text_data_path='book1.txt'
text_file=str(open(text_data_path,"r"))
# @end AccessText

# @begin PreprocessFile @desc To preprocess the text data
# @in stopwords
# @in regexr @as regular_expression
# @in TextRead
# @out Valid_file @as FileProcess @desc valid file after data preprocessing
en_stopwords=set(stopwords.words('english'))
de_stopwords=set(stopwords.words('german'))
fr_stopwords=set(stopwords.words('french'))
stopwords=en_stopwords|de_stopwords|fr_stopwords
Tokenize_file=word_tokenize(text_file.lower())
clean_file=[word for word in Tokenize_file if word not in stopwords]
regexr=re.compile('([a-z])\w+')
Valid_file=[w for w in clean_file if regexr.match(w)]

# @end PreprocessFile

# @begin LDA
# @in FileProcess @desc file after pre_process procedure
# @param n_components
# @param n_top_words
# @in random_state
# @in max_iter
# @in learning_method
# @in learning_offset
# @out Topicmodeling_Result @desc log file which contains the topics @uri file:output.txt


# @begin tf_calculation @desc using CountVectorizer from sklearn library to calculate the term frequency
# @in file_valid @desc file after pre_process
# @out tf @as term_frequency
# @out tf_vectorizer @as term_frequency_vectorizer

tf_vectorizer=CountVectorizer()
tf=tf_vectorizer.fit_transform(Valid_file)
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
# @out Topicmodeling_Result @uri file:output.txt

n_components=10
lda=LatentDirichletAllocation(n_components=n_components, max_iter=500,
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
# @out Topicmodeling_Result @uri file:output.txt
n_top_words=20
with open("output.txt","w")as file:
    for topic_idx, topic in enumerate(lda.components_):
        topic_log="Topic #%d: " % topic_idx
        topic_log+=" ".join([tf_feature_names[i]
                           for i in topic.argsort()[:-n_top_words -1: -1]])+"\n"
        file.write(topic_log)

# @end print_top_words

# @end LDA

# @end topic_modeling
