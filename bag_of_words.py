import csv
import argparse
import nltk
import re
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords


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
    #
    # def load_sentences(self, path):
    #     with open(path, 'r') as file:
    #         lines = file.readlines()
    #     for line in lines:

    def calculate_sentiment(self, sentence):
        valence = 0
        arousal = 0
        stop_words = set(stopwords.words('english'))
        word_list = []
        print(stop_words)
        for word in sentence:
            if word not in stop_words and word in self.word_dict:
                word_list.append(word)
        for word in word_list:
            print(word)
            valence += self.word_dict[word][0]
            arousal += self.word_dict[word][1]
        mean_valence = valence / len(word_list)
        mean_arousal = arousal / len(word_list)
        print(mean_valence, mean_arousal)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dictionary_path", type=str, required=True,
                        help="Path to dictionary file.")
    parser.add_argument("--filename", type=str, required=False,
                        help="Name of input file.")
    args = parser.parse_args()

    bag = BagOfWords(args.dictionary_path)
    t = bag.preprocess_text("I'm hurt and upset by what's happened. I'd like to hear your side of it so that we address the situation together.")
    bag.calculate_sentiment(t)
