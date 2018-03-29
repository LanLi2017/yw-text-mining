
# @begin LDA
# @in file_valid @desc file after pre_process procedure
# @param n_components
# @param n_top_words
# @in random_state
# @in max_iter
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

