from keras.datasets import imdb
from keras.utils.data_utils import get_file
import pickle
import pandas as pd
import numpy as np

PATH_WHOLE_IMDB = 'imdb_master.csv'
PATH_FILTERED_IMDB  = ''

def pickle_data(path):
    (x_train, y_train), (x_test, y_test) = imdb.load_data()
    dataset = np.concatenate((x_train, x_test))
    pickle.dump(dataset, open(path, 'wb'))
    word_to_index = imdb.get_word_index()
    print(word_to_index)

def load_csv(path):
    data = pd.read_csv(path, encoding = "ISO-8859-1")
    data = data[["review", "label"]]
    k = data.head()
    print((k))
    data = np.array(data)
    print(data[1])

if __name__ == "__main__":
    # pickle_data(PATH_WHOLE_IMDB)
    load_csv(PATH_WHOLE_IMDB)
