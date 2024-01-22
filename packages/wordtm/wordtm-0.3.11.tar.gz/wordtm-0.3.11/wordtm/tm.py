# tm.py
#    Topic modeling with LDA, NMF, and BERTopic for a prescribed range of Scripture or other text
#    By Johnny Cheng
#    Created: 20 Jan. 2024
#    Updated: 22 Jan. 2024
#       ~ Remove customized Chinese word embeddings
#       ~ Add global load_bible with category


## Dependencies

import warnings
warnings.filterwarnings("ignore")

import os
import numpy as np
import pandas as pd
import string
import re

import time
from pprint import pprint
from IPython.display import IFrame
from importlib_resources import files

import jieba
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import TweetTokenizer
import nltk

from gensim import corpora, models
from gensim.models.coherencemodel import CoherenceModel

import torch
from bertopic import BERTopic
from transformers import BertTokenizer, BertModel

import pyLDAvis.gensim_models as gensimvis
import pyLDAvis

from wordtm import util


def load_bible(textfile, cat=0, group=True):
    # textfile = "web.csv"
    scfile = files('wordtm.data').joinpath(textfile)
    print("Loading Bible '%s' ..." %scfile)
    df = pd.read_csv(scfile)

    cat_list = ['tor', 'oth', 'ket', 'map', 'mip',\
                'gos', 'nth', 'pau', 'epi', 'apo']	
    cat = str(cat)
    if cat == '1' or cat == 'ot':
        df = util.extract(df, testament=1)
    elif cat == '2' or cat == 'nt':
        df = util.extract(df, testament=2)               
    elif cat in cat_list:
        df = util.extract(df, category=cat)

    if group:
        # Group verses into chapters
        df = df.groupby(['book_no', 'chapter'])\
                        .agg({'text': lambda x: ' '.join(x)})\
                .reset_index()

    df.text = df.text.str.replace('　', '')
    return list(df.text)


## LDA Class
class LDA:
    num_topics = 10

    def __init__(self, textfile, chi):
        self.textfile = textfile
        self.chi = chi
        self.docs = None
        self.pro_docs = None
        self.dictionary = None
        self.corpus = None
        self.model = None
        self.vis_data = None
        self.vis_file = None

    def load_text(self):
        df = pd.read_csv(self.textfile)
        self.docs = list(df.text)
        return self.docs

    def load_data(self, docs):
        self.docs = list(docs)
        return self.docs

    def load_bible(self):
        # self.textfile = "web.csv"
        scfile = files('wordtm.data').joinpath(self.textfile)
        print("Loading Bible '%s' ..." %scfile)
        df = pd.read_csv(scfile)

        # Group verses into chapters
        df = df.groupby(['book_no', 'chapter'])\
                        .agg({'text': lambda x: ' '.join(x)})\
                .reset_index()

        df.text = df.text.str.replace('　', '')
        self.docs = list(df.text)
        return self.docs

   
    def process_text(self, doc):
        # List of punctuation
        punc = list(set(string.punctuation))

        # List of stop words
        add_stop = []
        stop_words = ENGLISH_STOP_WORDS.union(add_stop)

        doc = TweetTokenizer().tokenize(doc)
        doc = [each.lower() for each in doc]
        doc = [re.sub('[0-9]+', '', each) for each in doc]
        doc = [SnowballStemmer('english').stem(each) for each in doc]
        doc = [w for w in doc if w not in punc]
        doc = [w for w in doc if w not in stop_words]
        return doc
    
    def preprocess(self):
        self.pro_docs = [self.process_text(doc) for doc in self.docs]

        # Create a dictionary and corpus for LDA
        self.dictionary = corpora.Dictionary(self.pro_docs)
        self.corpus = [self.dictionary.doc2bow(doc) for doc in self.pro_docs]

    def preprocess_chi(self):
        # Build stop words
        stop_file = files('wordtm.data').joinpath("tc_stopwords_2.txt")
        stopwords = [k[:-1] for k in open(stop_file, encoding='utf-8')\
                     .readlines() if k != '']

        # Tokenize"the text using Jieba
        dict_file = files('wordtm.data').joinpath("user_dict_4.txt")
        jieba.load_userdict(str(dict_file))
        docs = [jieba.cut(doc) for doc in self.docs]

        # Replace special characters
        docs = [[word.replace('\u3000', ' ') for word in doc] \
                                     for doc in docs]

        # Remove stop words
        self.pro_docs = [' '.join([word for word in doc if word not in stopwords]) \
                                        for doc in docs]

        self.pro_docs = [doc.split() for doc in self.pro_docs]

        # Create a dictionary and corpus
        self.dictionary = corpora.Dictionary(self.pro_docs)
        self.corpus = [self.dictionary.doc2bow(doc) for doc in self.pro_docs]


    # Train LDA model
    def fit(self):
        self.model = models.LdaModel(self.corpus, 
                            num_topics=self.num_topics, 
                            id2word=self.dictionary, 
                            passes=10)
    
    def viz(self):
        self.vis_data = gensimvis.prepare(self.model, self.corpus, self.dictionary)
        pyLDAvis.enable_notebook()
        pyLDAvis.display(self.vis_data)
        print("If no visualization is shown,")
        print("  you may execute the following commands")
        print("  to show the visualization:")
        print("    import pyLDAvis")
        print("    pyLDAvis.display(lda.vis_data)")

    def show_topics(self):
        print("\nTopics from LDA Model:")
        pprint(self.model.print_topics())
    
    def evaluate(self):
        # Compute coherence score
        coherence_model = CoherenceModel(model=self.model,
                                         texts=self.pro_docs,
                                         dictionary=self.dictionary,
                                         coherence='c_v')
        print(f"  Coherence: {coherence_model.get_coherence()}")
        
        # Compute perplexity
        perplexity = self.model.log_perplexity(self.corpus)
        print(f"  Perplexity: {perplexity}")
        
        # Compute topic diversity
        topic_sizes = [len(self.model[self.corpus[i]]) for i in range(len(self.corpus))]
        total_docs = sum(topic_sizes)
        topic_diversity = sum([(size/total_docs)**2 for size in topic_sizes])
        print(f"  Topic diversity: {topic_diversity}")
        
        # Compute topic size distribution
        # topic_sizes = [len(self.model[self.corpus[i]]) for i in range(len(self.corpus))]
        topic_size_distribution = max(topic_sizes) / sum(topic_sizes)
        print(f"  Topic size distribution: {topic_size_distribution}\n")

## End of LDA Class

## LDA Process
def lda_process(doc_file, cat=0, chi=False, eval=False):
    lda = LDA(doc_file, chi)
    # lda.load_bible()
    lda.docs = load_bible(lda.textfile, cat=cat)
    print("Bible loaded!")

    if chi:
        lda.preprocess_chi()
    else:
        lda.preprocess()
    print("Text preprocessed!")

    lda.fit()
    print("Text trained!")
    lda.viz()
    print("Visualization prepared!")
    lda.show_topics()

    if eval:
        print("\nModel Evaluation Scores:")
        lda.evaluate()

    return lda


## NMF Class
class NMF:
    num_topics = 10

    # List of punctuation
    punc = list(set(string.punctuation))

    # List of stop words
    add_stop = []
    stop_words = ENGLISH_STOP_WORDS.union(add_stop)

    def __init__(self, textfile, chi=False):
        self.textfile = textfile
        self.chi = chi
        self.docs = None
        self.pro_docs = None
        self.dictionary = None
        self.corpus = None
        self.model = None
        self.vis_data = None
        self.vis_file = None

    def load_text(self):
        df = pd.read_csv(self.textfile)
        self.docs = list(df.text)
        return self.docs

    def load_data(self, docs):
        self.docs = list(docs)
        return self.docs
 
    def load_bible(self):
        # self.textfile = "web.csv"
        scfile = files('wordtm.data').joinpath(self.textfile)
        print("Loading Bible '%s' ..." %scfile)
        df = pd.read_csv(scfile)

        # Group verses into chapters
        df = df.groupby(['book_no', 'chapter'])\
                        .agg({'text': lambda x: ' '.join(x)})\
                .reset_index()

        df.text = df.text.str.replace('　', '')
        self.docs = list(df.text)
        return self.docs
   
    def process_text(self, doc):
        doc = TweetTokenizer().tokenize(doc)
        doc = [each.lower() for each in doc]
        doc = [re.sub('[0-9]+', '', each) for each in doc]
        doc = [SnowballStemmer('english').stem(each) for each in doc]
        doc = [w for w in doc if w not in self.punc]
        doc = [w for w in doc if w not in self.stop_words]
        return doc
    
    def preprocess(self):
        self.pro_docs = [self.process_text(doc) for doc in self.docs]

        # Create a dictionary and corpus for NMF
        self.dictionary = corpora.Dictionary(self.pro_docs)
        self.corpus = [self.dictionary.doc2bow(doc) for doc in self.pro_docs]

    def preprocess_chi(self):
        # Build stop words
        stop_file = files('wordtm.data').joinpath("tc_stopwords_2.txt")
        stopwords = [k[:-1] for k in open(stop_file, encoding='utf-8')\
                     .readlines() if k != '']

        # Tokenize"the text using Jieba
        dict_file = files('wordtm.data').joinpath("user_dict_4.txt")
        jieba.load_userdict(str(dict_file))
        docs = [jieba.cut(doc) for doc in self.docs]

        # Replace special characters
        docs = [[word.replace('\u3000', ' ') for word in doc] \
                                     for doc in docs]

        # Remove stop words
        self.pro_docs = [' '.join([word for word in doc if word not in stopwords]) \
                                        for doc in docs]

        self.pro_docs = [doc.split() for doc in self.pro_docs]

        # Create a dictionary and corpus
        self.dictionary = corpora.Dictionary(self.pro_docs)
        self.corpus = [self.dictionary.doc2bow(doc) for doc in self.pro_docs]


    # Train NMF model
    def fit(self):
        self.model = models.Nmf(self.corpus,
                                num_topics=self.num_topics)

    def show_topics_words(self):
        print("\nTopics-Words from NMF Model:")
        for topic_id in range(self.model.num_topics):
            topic_words = self.model.show_topic(topic_id, topn=10)
            print(f"Topic {topic_id+1}:")
            for word_id, prob in topic_words:
                # word = self.dictionary.id2token[int(word_id)]
                word = self.dictionary[int(word_id)]
                print("%s (%.6f)" %(word, prob))
            print()

    def evaluate(self):
        # Compute coherence score
        coherence_model = CoherenceModel(model=self.model,
                                         texts=self.pro_docs,
                                         dictionary=self.dictionary,
                                         coherence='c_v')
        print(f"  Coherence: {coherence_model.get_coherence()}")
        
        # Compute topic diversity
        topic_sizes = [len(self.model[self.corpus[i]]) for i in range(len(self.corpus))]
        total_docs = sum(topic_sizes)
        topic_diversity = sum([(size/total_docs)**2 for size in topic_sizes])
        print(f"  Topic diversity: {topic_diversity}")
        
        # Compute topic size distribution
        # topic_sizes = [len(self.model[self.corpus[i]]) for i in range(len(self.corpus))]
        topic_size_distribution = max(topic_sizes) / sum(topic_sizes)
        print(f"  Topic size distribution: {topic_size_distribution}\n")

## End of NMF Class

## NMF Process
def nmf_process(doc_file, cat=0, chi=False, eval=False):
    nmf = NMF(doc_file, chi)
    # nmf.load_bible()
    nmf.docs = load_bible(nmf.textfile, cat=cat)
    print("Bible loaded!")

    if chi:
        nmf.preprocess_chi()
    else:
        nmf.preprocess()
    print("Text preprocessed!")

    nmf.fit()
    print("Text trained!")
    nmf.show_topics_words()

    if eval:
        print("\nModel Evaluation Scores:")
        nmf.evaluate()

    return nmf


## BTM Class
class BTM:
    num_topics = 10

    def __init__(self, textfile, chi=False, embed=True):
        self.textfile = textfile
        self.chi = chi
        self.docs = None
        self.pro_docs = None
        self.dictionary = None
        self.corpus = None
        self.model = None
        self.vis_data = None
        self.vis_file = None

        self.embed = embed
        self.btokenizer = None # Tokenizer from pretrained model
        self.bmodel = None # BERT pretrained model
        self.bt_topics = None
        self.bt_vectorizer = None
        self.bt_analyzer = None
        self.cleaned_docs = None

    def load_text(self):
        df = pd.read_csv(self.textfile)
        self.docs = list(df.text)
        return self.docs

    def load_data(self, docs):
        self.docs = list(docs)
        return self.docs
 
    def load_bible(self):
        # self.textfile = "web.csv"
        scfile = files('wordtm.data').joinpath(self.textfile)
        print("Loading Bible '%s' ..." %scfile)
        df = pd.read_csv(scfile)

        # Group verses into chapters
        df = df.groupby(['book_no', 'chapter'])\
                        .agg({'text': lambda x: ' '.join(x)})\
                .reset_index()

        df.text = df.text.str.replace('　', '')
        self.docs = list(df.text)
        return self.docs
   
    def process_text(self, doc):
        # List of punctuation
        punc = list(set(string.punctuation))

        # List of stop words
        add_stop = []
        stop_words = ENGLISH_STOP_WORDS.union(add_stop)

        doc = TweetTokenizer().tokenize(doc)
        doc = [each.lower() for each in doc]
        doc = [re.sub('[0-9]+', '', each) for each in doc]
        doc = [SnowballStemmer('english').stem(each) for each in doc]
        doc = [w for w in doc if w not in punc]
        doc = [w for w in doc if w not in stop_words]
        return doc
    
    def preprocess(self):
        self.pro_docs = [self.process_text(doc) for doc in self.docs]

        # Create a dictionary and corpus
        self.dictionary = corpora.Dictionary(self.pro_docs)
        self.corpus = [self.dictionary.doc2bow(doc) for doc in self.pro_docs]

    def preprocess_chi(self):
        # Build stop words
        stop_file = files('wordtm.data').joinpath("tc_stopwords_2.txt")
        stopwords = [k[:-1] for k in open(stop_file, encoding='utf-8')\
                     .readlines() if k != '']

        # Tokenize"the text using Jieba
        dict_file = files('wordtm.data').joinpath("user_dict_4.txt")
        jieba.load_userdict(str(dict_file))
        docs = [jieba.cut(doc) for doc in self.docs]

        # Replace special characters
        docs = [[word.replace('\u3000', ' ') for word in doc] \
                                     for doc in docs]

        # Remove stop words
        self.pro_docs = [' '.join([word for word in doc if word not in stopwords]) \
                                        for doc in docs]

        self.pro_docs = [doc.split() for doc in self.pro_docs]

        # Create a dictionary and corpus
        self.dictionary = corpora.Dictionary(self.pro_docs)
        self.corpus = [self.dictionary.doc2bow(doc) for doc in self.pro_docs]


    # Train BERTopic model - English
    def fit(self):
        j_pro_docs = [" ".join(doc) for doc in self.pro_docs]

        if self.embed:
            self.bmodel = BertModel.from_pretrained('bert-base-uncased')
            self.model = BERTopic(language='english', 
                                  calculate_probabilities=True,
                                  embedding_model=self.bmodel)
        else:
            self.model = BERTopic(language='english', 
                                  calculate_probabilities=True)

        self.bt_topics, _ = self.model.fit_transform(j_pro_docs)


    # Train BERTopic model - Chinese
    def fit_chi(self):
        j_pro_docs = [" ".join(doc) for doc in self.pro_docs]

        if self.embed:
            self.bmodel = BertModel.from_pretrained('bert-base-chinese')
            self.model = BERTopic(language='chinese (traditional)', 
                                  calculate_probabilities=True,
                                  embedding_model=self.bmodel)
        else:
            self.model = BERTopic(language='chinese (traditional)', 
                                  calculate_probabilities=True)

        self.bt_topics, _ = self.model.fit_transform(j_pro_docs)


    def show_topics(self):
        print("\nTopics from BERTopic Model:")

        for topic in self.model.get_topic_freq().Topic:
            if topic == -1: continue
            twords = [word for (word, _) in self.model.get_topic(topic)]
            print(f"Topic {topic}: {' | '.join(twords)}")


    def pre_evaluate(self):
        doc_df = pd.DataFrame({"Document": self.docs,
                       "ID": range(len(self.docs)),
                       "Topic": self.bt_topics})
        documents_per_topic = doc_df.groupby(['Topic'], \
                             as_index=False).agg({'Document': ' '.join})
        self.cleaned_docs = self.model._preprocess_text(\
                              documents_per_topic.Document.values)

        # Extract vectorizer and analyzer from BERTopic
        self.bt_vectorizer = self.model.vectorizer_model
        self.bt_analyzer = self.bt_vectorizer.build_analyzer()

    def evaluate(self):
        self.pre_evaluate()
        
        # Extract features for Topic Coherence evaluation
        # words = self.bt_vectorizer.get_feature_names_out()
        tokens = [self.bt_analyzer(doc) for doc in self.cleaned_docs]

        self.dictionary = corpora.Dictionary(tokens)
        self.corpus = [self.dictionary.doc2bow(doc) for doc in tokens]

        topic_words = [[words for words, _ in self.model.get_topic(topic)] 
                       for topic in range(len(set(self.bt_topics))-1)]

        coherence = CoherenceModel(topics=topic_words, texts=tokens, corpus=self.corpus, 
                                      dictionary=self.dictionary, coherence='c_v')\
                        .get_coherence()

        print(f"  Coherence: {coherence}")


    def viz(self):
        print("\nBERTopic Model Visualization:")

        # Intertopic Distance Map
        self.model.visualize_topics().show()

        # Visualize Terms (Topic Word Scores)
        self.model.visualize_barchart().show()

        # Visualize Topic Similarity
        self.model.visualize_heatmap().show()
        
        print("  If no visualization is shown,")
        print("    you may execute the following commands one-by-one:")
        print("      btm.model.visualize_topics()")
        print("      btm.model.visualize_barchart()")
        print("      btm.model.visualize_heatmap()")
        print()

## End of BTM Class

## BTM Process
def btm_process(doc_file, cat=0, chi=False, eval=False):
    btm = BTM(doc_file, chi)
    # btm.load_bible()
    btm.docs = load_bible(btm.textfile, cat=cat)
    print("Bible loaded!")

    if chi:
        btm.preprocess_chi()
        print("Chinese text preprocessed!")
        btm.fit_chi()
    else:
        btm.preprocess()
        print("Text preprocessed!")
        btm.fit()
    
    print("Text trained!")

    btm.show_topics()

    if eval:
        print("\nModel Evaluation Scores:")
        btm.evaluate()
    
    btm.viz()

    return btm

### End of TM Module