# Import libraries
####
import nltk
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx

####
# Download stopwords and specify the language
####
nltk.download("stopwords")
stop_words = stopwords.words("english")


def text_summarization(text_input: str) -> list:
    """Summarizing the text using the similarity matrix method.

    Params:
        text_input (str): input text

    Returns:
        list: 3 sentences from the text with higher score
    """

    ####
    # Read text input and split it
    ####
    sentences = []
    text = text_input.split('. ')
    for sentence in text:
        sentences.append(sentence.split(' '))
    for s in sentences:
        if '.' not in s[-1]:
            s.append('.')

    ####
    # Creating a similarity matrix between sentences
    ####
    def sentence_similarity(sent1, sent2, stopwords=None):

        if stopwords is None:
            stopwords = []

        sent1 = [w.lower() for w in sent1]
        sent2 = [w.lower() for w in sent2]

        all_words = list(set(sent1 + sent2))

        vector1 = [0] * len(all_words)
        vector2 = [0] * len(all_words)

        # Build the vector for the first sentence
        for w in sent1:
            if w in stopwords:
                continue
            vector1[all_words.index(w)] += 1
        # Build the vector for the second sentence
        for w in sent2:
            if w in stopwords:
                continue
            vector2[all_words.index(w)] += 1

        return 1 - cosine_distance(vector1, vector2)

    similitary_matrix = np.zeros((len(sentences), len(sentences)))

    for i in range(len(sentences)):
        for j in range(len(sentences)):
            similitary_matrix[i][j] = sentence_similarity(
                sentences[i], sentences[j], stop_words)

    sentence_similarity_graph = nx.from_numpy_array(similitary_matrix)

    scores = nx.pagerank(sentence_similarity_graph)

    ranked_sentence = sorted(
        ((scores[i], s) for i, s in enumerate(sentences)), reverse=True)

    summarize_text = []
    for i in range(len(ranked_sentence)):
        summarize_text.append(" ".join(ranked_sentence[i][1]))
    return summarize_text[:3]

