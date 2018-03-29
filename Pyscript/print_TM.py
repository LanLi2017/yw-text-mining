
# @begin print_top_words @desc print the top main words for very topic
# @param model
# @param feature_name
# @param n_top_words @as number_of_top_words
# @out message
from Pyscript.LDA_topicmodeling import lda, tf_feature_names

model=lda
feature_name=tf_feature_names
n_top_words=20
for topic_idx, topic in enumerate(model.components_):
    message="Topic #%d: " % topic_idx
    message+=" ".join([feature_name[i]
                           for i in topic.argsort()[:-n_top_words -1: -1]])
    print(message)
print()

# @end print_top_words
