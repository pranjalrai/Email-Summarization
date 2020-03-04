import numpy as np
import pandas as pd
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx


def remove_stopwords(sen):
  sen_new = " ".join([i for i in sen if i not in stop_words])
  return sen_new


# df = pd.read_csv("sc-conv2.csv")
df = pd.read_csv("SC-conv - Sheet1.csv")

sentences = []
for s in df['Message']:
  sentences.append(sent_tokenize(s))

sentences = [y for x in sentences for y in x]

word_embeddings = {}
f = open('glove.6B.100d.txt', encoding='utf-8')
for line in f:
    values = line.split()
    word = values[0]
    coefs = np.asarray(values[1:], dtype='float32')
    word_embeddings[word] = coefs
f.close()

# preprocess sentences
clean_sentences = pd.Series(sentences).str.replace("[^a-zA-Z]", " ")
clean_sentences = [s.lower() for s in clean_sentences]

# remove stopwords
stop_words = stopwords.words('english')
clean_sentences = [remove_stopwords(r.split()) for r in clean_sentences]
for ind, sent in enumerate(clean_sentences):
  sent = sent.lower()
  clean_sentences[ind] = sent.replace('thanks' or 'thank you' or 'thanks a lot' or 'regards' or 'thanks & regards' or 'thanks and regards' or 'regards', '')

sentence_vectors = []
for i in clean_sentences:
  if len(i) != 0:
    v = sum([word_embeddings.get(w, np.zeros((100,))) for w in i.split()]) / (len(i.split()) + 0.001)
  else:
    v = np.zeros((100,))
  sentence_vectors.append(v)

# similarity matrix
sim_mat = np.zeros([len(sentences), len(sentences)])

for i in range(len(sentences)):
  for j in range(len(sentences)):
    if i != j:
      sim_mat[i][j] = cosine_similarity(sentence_vectors[i].reshape(1,100), sentence_vectors[j].reshape(1,100))[0,0]

nx_graph = nx.from_numpy_array(sim_mat)
scores = nx.pagerank(nx_graph)

ranked_sentences = sorted(((scores[i], s, i) for i, s in enumerate(sentences)), reverse=True)
top_sentences = []
fin_sent_cnt = len(ranked_sentences)//3
for i in range(fin_sent_cnt):
  # print(ranked_sentences[i][1])
  top_sentences.append((ranked_sentences[i][2], ranked_sentences[i][1]))

top_sentences = sorted(top_sentences)
for i in range(len(top_sentences)):
  final_sent = top_sentences[i][1].lower().replace(
    'thanks' or 'thank you' or 'thanks a lot' or 'regards' or 'thanks & regards' or 'thanks and regards' or 'regards', '')
  print(final_sent)

