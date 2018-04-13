
# @begin topic_modeling @desc Exercise YW for Analysing Text with NLTk
# @in Static_text @uri file:news2012.txt
# @out LDA_model @desc Transformation from BOW counts into a topic space @uri file:LDA_output.txt
# @out HDP_model @desc non-parametric bayesian method @uri file:HDP_output.txt
# @out LSI_model @desc Transformation from BOW or TfIDF @uri file:LSI_output.txt
# @out Evaluation_result

import os
from gensim import corpora,models
from collections import defaultdict
from nltk import word_tokenize, re, pprint, corpus
from nltk.corpus import stopwords
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer

# @begin TrainingCorpus @desc Using Gensim to construct training corpus
# @in text_data_path @as Static_text @desc Text file which contains static text data @uri file:book1.txt
# @in stopwords
# @in regexr @as regular_expression
# @out processed_corpus @as Corpus
# @out dictionary @as dictionary @desc associate each word in the corpus with a unique integer ID

text_data_path='news2012.txt'

en_stopwords=set(stopwords.words('english'))
de_stopwords=set(stopwords.words('german'))
fr_stopwords=set(stopwords.words('french'))
stopwords=en_stopwords|de_stopwords|fr_stopwords

regexr=re.compile('([a-z])\w+')

# @begin AccessText @desc To read the text data from book1.txt file
# @in text_data_path @as Static_text @desc Text file which contains static text data @uri file:news2012.txt
# @out text_file @as TextRead
text_file=[]
with open(text_data_path,"rt")as f:
    for line in f:
        line=[
            word
            for word in line.lower().split()
            if word not in stopwords and regexr.match(word)
        ]
        text_file.append(line)

# @end AccessText

# @begin PreprocessFile @desc To preprocess the text data
# @in stopwords
# @in regexr @as regular_expression
# @in TextRead
# @out dictionary @as Corpus

# calculate word frequencies
word_frequency=defaultdict(int)
for text in text_file:
    for token in text:
        word_frequency[token] +=1
# only keep words that occur more than once
processed_corpus=[[token for token in text if word_frequency[token]>1] for text in text_file]
# associate each word in the corpus with a unique integer ID
dictionary=corpora.Dictionary(processed_corpus)
corpus=[dictionary.doc2bow(text) for text in processed_corpus]
# @end PreprocessFile

# @end TrainingCorpus


# @begin Evaluation_Model @desc Using different models to do Topic and Transformation
# @in Corpus
# @in dictionary
# @out LDA_model @desc Transformation from BOW counts into a topic space @uri file:LDA_output.txt
# @out HDP_model @desc non-parametric bayesian method @uri file:HDP_output.txt
# @out LSI_model @desc Transformation from BOW or TfIDF @uri file:LSI_output.txt
# @out Evaluation_result

# @begin LDA_evaluation @desc tuning hyper-parameters to do modeling
# @in Corpus
# @in dictionary
# @param num_topics
# @out LDA_model
_num_topics=5
LDA_model=models.LdaModel(corpus,id2word=dictionary,num_topics=_num_topics)

with open('LDA_output.txt','wt')as f0:
    for topic in range(_num_topics):
        f0.write(str(LDA_model.print_topic(topic))+'\n')

# @end LDA_evaluation

# @begin HDP_evaluation
# @in Corpus
# @in dictionary
# @out HDP_model
HDP_model = models.HdpModel(corpus, id2word=dictionary)
with open('HDP_output.txt','w')as f1:
    for topic in range(_num_topics):
        f1.write(str(HDP_model.print_topic(topic))+'\n')
# @end HDP_evaluation

# @begin LSI_evaluation
# @in Corpus
# @in dictionary
# @param num_topics
# @out LSI_model @desc Generate LSI model @uri file:LSI_output.txt

# @begin TFIDF_transformation
# @in Corpus
# @out corpus_tfidf @desc using tfidf transformation to transform corpus

tfidf=models.TfidfModel(corpus)
corpus_tfidf=tfidf[corpus]

# @end TFIDF_transformation

# @begin LSI_model
# @in corpus_tfidf
# @in dictionary
# @param num_topics
# @out LSI_model
LSI_model = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=_num_topics)

with open('LSI_output.txt','w')as f2:
    for topic in range(_num_topics):
        f2.write(str(LSI_model.print_topic(topic))+'\n')
# @end LSI_model

# @end LSI_evaluation


# @end Evaluation_Model

# @end topic_modeling
