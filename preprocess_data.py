import pickle
import pandas as pd
import numpy as np
import argparse


def pickle_data(filename, data):
    pickle.dump(data, open(filename, 'wb'))


def load_csv(path):
    data = pd.read_csv(path, encoding = "ISO-8859-1")
    data = data[["review", "label"]]
    # data = data.head()
    data = np.array(data)
    return data


def cut_sentences(max_length, data):
    filtered_dataset = []
    for row in data:
        items = row[0].split('.')
        index = 0
        temp = items[index]
        while len(temp) < max_length:
            temp = temp + items[index]
            index = index + 1
        filtered_dataset.append([temp, row[1]])
    return filtered_dataset


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv_path", type=str, required=False, default= 'imdb_master.csv',
                        help="Path to imdb dataset.")
    parser.add_argument("--filename", type=str, required=False, default= 'filtered_dataset.pkl',
                        help="Name of pickle file.")
    parser.add_argument("--max_length", type=int, required=False, default=60,
                        help="Max length of sentence.")
    args = parser.parse_args()

    whole_data = load_csv(args.csv_path)
    filtered_data = cut_sentences(args.max_length, whole_data)
    pickle_data(args.filename, filtered_data)
