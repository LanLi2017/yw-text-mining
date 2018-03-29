# @begin tf_calculation @desc using CountVectorizer from sklearn library to calculate the term frequency
# @in file_valid @desc file after pre_process
# @out tf @as term_frequency
# @out tf_vectorizer @as term_frequency_vectorizer
from sklearn.feature_extraction.text import CountVectorizer


from Pyscript.preprocess_data import file_valid

tf_vectorizer=CountVectorizer()
tf=tf_vectorizer.fit_transform(file_valid)

# @end tf_calculation
