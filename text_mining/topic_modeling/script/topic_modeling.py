
# @begin topic_modeling @desc Exercise YW for Analysing Text with NLTk
# @in Static_text @uri file:../../nipstxt
# @param num_topics
# @param num_iteration
# @out LDA_model @desc Transformation from BOW counts into a topic space @uri file:LDA_output.txt
# @out HDP_model @desc non-parametric bayesian method @uri file:HDP_output.txt
# @out LSI_model @desc Transformation from BOW or TfIDF @uri file:LSI_output.txt
# @out log @as run_log @desc record the iterations and log_perplexity and time stamp
import os
import time
import datetime
from gensim import corpora,models
from collections import defaultdict
from nltk import word_tokenize, re, pprint, corpus
from nltk.corpus import stopwords
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer

# @begin ConstructCorpus @desc Using Gensim to construct training corpus and testing corpus
# @in text_data_path @as Static_text @desc Text file which contains static text data @uri file:book1.txt
# @in stopwords
# @in regexr @as regular_expression
# @out dictionary @as dictionary @desc a mapping between words and their integer ids
# @out train_corpus @desc split 0.8 corpus to train the model
# @out test_corpus @desc split 0.2 corpus to predict
data_dir = '../../nipstxt/'

yr = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
dir = ['nips' + year for year in yr]

# @begin AccessText @desc To read the text data from book1.txt file
# @in text_data_path @as Static_text @desc Text file which contains static text data @uri file:../../nipstxt
# @out text_file @as TextRead

# Read all texts into a list.
text_file = []
for yr_dir in dir:
    files = os.listdir(data_dir + yr_dir)
    for filen in files:
        # Note: ignoring characters that cause encoding errors.
        with open(data_dir + yr_dir + '/' + filen, errors='ignore') as fid:
            txt = fid.read()
        text_file.append(txt)

# @end AccessText

# @begin PreprocessFile @desc To preprocess the text data
# @in stopwords
# @in regexr @as regular_expression
# @in TextRead
# @out dictionary
# @out train_corpus
# @out test_corpus
en_stopwords=set(stopwords.words('english'))
de_stopwords=set(stopwords.words('german'))
fr_stopwords=set(stopwords.words('french'))
stopwords=en_stopwords|de_stopwords|fr_stopwords

regexr=re.compile('([a-z])\w+')

file_tokens=(word.lower() for word in text_file)
clean_file=[word for word in file_tokens if word not in stopwords]
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

train_corpus = corpus[:int((len(corpus)+1)*.80)] # Remaining 80% to training set
test_corpus = corpus[int(len(corpus)*.80+1):]

# @end PreprocessFile

# @end ConstructCorpus


# @begin Train_Predict_Model @desc Using gensim.LDA to training model and predicting, get the converge number
# @in train_corpus
# @in dictionary
# @in test_corpus
# @param num_iteration @desc number of maximum iterations
# @param num_topics @desc number of topics
# @out LDA_model @desc Transformation from BOW counts into a topic space @uri file:LDA_output.txt
# @out log @as run_log


# @begin get_iteration_number @desc training model to get the converge iteration number
# @in train_corpus
# @in test_corpus
# @in dictionary
# @param num_iteration
# @param num_topics
# @out log @as run_log
# @out iter @as converge_iteration @desc number of iterations when converge
_num_topics=5
num_iteration=500

with open('log.txt','w')as log:
    st=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    likelihood=[]
    iter=1
    LDA_model0=models.LdaModel(corpus=train_corpus,id2word=dictionary,num_topics=_num_topics,iterations=1)
    log_likelihood0=LDA_model0.log_perplexity(test_corpus)
    likelihood.append(log_likelihood0)
    while iter<=num_iteration:
        LDA_model=models.LdaModel(corpus=train_corpus,id2word=dictionary,num_topics=_num_topics,iterations=1)
        log_likelihood=LDA_model.log_perplexity(test_corpus)
        likelihood.append(log_likelihood)
        if abs(likelihood[iter-1] -likelihood[iter])> 0.0000001:
            print(st+' '+str(log_likelihood))
            log.write(st+'  '+str(log_likelihood)+'\n')
            iter+=1
        else:
            print(' Found convergence after '+str(iter)+' iterations!')
            log.write(' Found convergence after '+str(iter)+' iterations!')
            break
# @end get_iteration_number

# @begin LDA_model
# @in dictionary
# @in num_topics
# @in iter @as converge_iteration
# @out LDA_model
with open('LDA_output.txt','wt')as f0:
    LDA_model=models.LdaModel(corpus=train_corpus,id2word=dictionary,num_topics=_num_topics,iterations=iter)
    for topic in range(_num_topics):
        f0.write(str(LDA_model.print_topic(topic))+'\n')

# @end LDA_model

# @end Train_Predict_Model

# @end topic_modeling
