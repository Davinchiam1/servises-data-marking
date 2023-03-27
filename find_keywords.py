import re
import os
import pandas as pd
import string
from nltk import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
import nltk
# nltk.download('punkt')
# nltk.download('stopwords')

class Find_keywords:
    def __init__(self):
        self.frequency = {}
        self.temp_frame = None
        self.text = ''

    def _get_text(self, filepath, name_colum, selection=None):
        if filepath.split('.')[-1].lower() == 'csv':
            self.temp_frame = pd.read_csv(filepath, delimiter=';')
        elif filepath.split('.')[-1].lower() == 'xlsx':
            self.temp_frame = pd.read_excel(filepath)
        if selection is not None:
            self.temp_frame = self.temp_frame.loc[self.temp_frame[selection[0]] == selection[1]]
        temp_list = self.temp_frame[name_colum].to_list()
        self.text = ' '.join(temp_list)

    def _prepare_text(self):
        self.text = self.text.lower()
        spec_chars = string.punctuation + '\n\xa0«»\t—…'
        self.text = "".join([ch for ch in self.text if ch not in spec_chars])

    def _count_frequency(self):
        text_tokens = word_tokenize(self.text)
        russian_stopwords = stopwords.words("russian")
        text_tokens = [token.strip() for token in text_tokens if token not in russian_stopwords]
        self.text = nltk.Text(text_tokens)
        self.frequency = FreqDist(self.text)
        final_frame = pd.DataFrame.from_dict(self.frequency, orient='index').reset_index()
        print(final_frame.head(20))

    def use(self, filepath, name_colum):
        self._get_text(filepath=filepath, name_colum=name_colum)
        self._prepare_text()
        self._count_frequency()


test = Find_keywords()
test.use(filepath='./final1.xlsx', name_colum='Название')
