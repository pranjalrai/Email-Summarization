import csv
from nltk.stem.wordnet import WordNetLemmatizer
import re, string, random
from nltk.tag import pos_tag
import argparse
import nltk
nltk.download('vader_lexicon')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import word_tokenize
def plot_graph(xaxis, yaxis, file_name="plot"):
  import tkinter as tk
  import matplotlib.pyplot as plt
  from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
  root= tk.Tk()
  figure, axis = plt.subplots(nrows = 1, ncols = 1, figsize=(15, 17))
  bar = FigureCanvasTkAgg(figure, root)
  bar.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
  axis.plot(xaxis, yaxis)
  axis.set_title('Email Sentiment Trend')
  for label in axis.get_xticklabels():
    label.set_rotation(90)
  figure.savefig(f'analysis/{file_name}.png')
def read_csv(path):
  csv_data = {}
  headers = []
  csv_data_lst = []
  with open(path, newline='') as f:
    reader = csv.reader(f)
    for id, row in enumerate(reader):
      if id != 0:
        row_details = {}
        for i, x in enumerate(row):
          row_details.update({headers[i]: x})
        csv_data_lst.append(row_details)
      else:
        headers = row
  return csv_data_lst
def remove_noise(sentence, stop_words = ()):
  cleaned_tokens = []
  for token, tag in pos_tag(sentence):
    token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
             '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
    token = re.sub("(@[A-Za-z0-9_]+)","", token)
    if tag.startswith("NN"):
      pos = 'n'
    elif tag.startswith('VB'):
      pos = 'v'
    else:
      pos = 'a'
    lemmatizer = WordNetLemmatizer()
    token = lemmatizer.lemmatize(token, pos)
    if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
      cleaned_tokens.append(token.lower())
  return ' '.join(cleaned_tokens)
def get_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('--file_path')
  args = parser.parse_args()
  return args
args = get_args()
summary_txt = read_csv(args.file_path)
sid = SentimentIntensityAnalyzer()
sentence_scores = {
  'Time': [],
  'Sentiment_Score': []
}
for index, sentence in enumerate(summary_txt):
  if sentence['IsCustomerMail'] == 'TRUE':
    cleaned_data = remove_noise(word_tokenize(sentence['Message']))
    scores = sid.polarity_scores(cleaned_data)
    sentence_scores['Time'].append(sentence['Time'].strip().replace("\"",""))
    sentence_scores['Sentiment_Score'].append(scores['compound'])
file_name = args.file_path.split("/")[-1]
plot_graph(sentence_scores['Time'], sentence_scores['Sentiment_Score'], file_name)