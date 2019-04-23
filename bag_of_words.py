import csv
import argparse
import nltk
import pickle
import re
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
import numpy as np


class BagOfWords:
    def __init__(self, dictionary_path):
        self.word_dict = {}
        self.create_dictionary(dictionary_path)


    def create_dictionary(self, path):
        with open(path, newline='') as csvfile:
            word_reader = csv.DictReader(csvfile)
            for row in word_reader:
                self.word_dict = {row['Word']: [float(row['Valence']), float(row['Arousal'])] for row in word_reader}


    def preprocess_text(self, text):
        lemmatizer = WordNetLemmatizer()
        text = re.sub(r'[^\w\s]','',text)
        text = text.lower()
        text = text.split()
        text_preprocessed = []
        for word in text:
           text_preprocessed.append(lemmatizer.lemmatize(word, 'v'))
        return text_preprocessed


    def scale_value(self, value, power):
        print("przed ", value)
        value = value - 5
        if value > 0:
            value = 4**power - (4 - value)**power
            value = (value)/4**power
        else:
            value = -(4**power) + (np.abs(4 + value))**power
            value = (value)/4**power
        print("po", value)
        return value


    def calculate_sentiment(self, sentence):
        valence = 0
        arousal = 0
        stop_words = set(stopwords.words('english'))
        word_list = []
        for word in sentence:
            if word not in stop_words and word in self.word_dict:
                word_list.append(word)
        for word in word_list:
            print(self.word_dict[word][0])
            valence += self.scale_value(self.word_dict[word][0], 4)
            arousal += self.scale_value(self.word_dict[word][1], 4)
            # # valence += ((self.word_dict[word][0] - 1) / 8) * 2 -1
            # # arousal += ((self.word_dict[word][1] -1) / 8)* 2 -1
        mean_valence = valence / len(word_list)
        mean_arousal = arousal / len(word_list)
        return mean_valence, mean_arousal

    def plot_points(self, points, p):
        r = 1
        t = np.arange(0, 2 * np.pi, 0.01)
        x = r* np.sin(t)
        y = r* np.cos(t)
        plt.plot(x, y)
        plt.axis([-1.5, 1.5, -1.5, 1.5])

        plt.plot(points, p, '^')

        plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dictionary_path", type=str, required=True,
                        help="Path to dictionary file.")
    parser.add_argument("--filename", type=str, required=False, default= 'filtered_dataset.pkl',
                        help="Name of input file.")
    args = parser.parse_args()

    bag = BagOfWords(args.dictionary_path)

    with open(args.filename, 'rb') as f:
        data = pickle.load(f)

    full_scores = []
    scores_a = []
    scores_b = []
    for row in data:
        temp = bag.preprocess_text(row[0])
        score = bag.calculate_sentiment(temp)
        full_scores.append([row[0], temp, [score]])
        scores_a.append(score[0])
        scores_b.append(score[1])
    print(scores_a, scores_b)

    pickle.dump(score, open('scores.pkl', 'wb'))
    pickle.dump(scores_a, open('scores_valence.pkl', 'wb'))
    pickle.dump(scores_b, open('scores_arousal.pkl', 'wb'))
    # bag.plot_points(scores_a, scores_b)