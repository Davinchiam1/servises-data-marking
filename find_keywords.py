import re
import os
import pandas as pd
import string
from nltk import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
import nltk
from pymorphy2 import MorphAnalyzer
from collections import defaultdict
from collections.abc import Iterable

# nltk.download('punkt')
# nltk.download('stopwords')

class Find_keywords:
    def __init__(self):
        self.frequency = {}
        self.temp_frame = None
        self.text = ''
        self.patterns = "[0-9!#$%&'()*+,./:;<=>?@[\]^_`{|}~—\"\-]+"
        self.stopwords_ru = stopwords.words("russian")
        self.morph = MorphAnalyzer()


    def _get_text(self, filepath, name_colum, selection=None):
        if filepath.split('.')[-1].lower() == 'csv':
            self.temp_frame = pd.read_csv(filepath, delimiter=';')
        elif filepath.split('.')[-1].lower() == 'xlsx':
            self.temp_frame = pd.read_excel(filepath)
        if selection is not None:
            self.temp_frame = self.temp_frame.loc[self.temp_frame[selection[0]] == selection[1]]
        self.temp_frame = self.temp_frame[name_colum]

    def _lemmatize(self, docs):
        docs = re.sub(self.patterns, ' ', docs)
        tokens = []
        for token in docs.split():
            if token and token not in self.stopwords_ru:
                token = token.strip()
                token = self.morph.normal_forms(token)[0]
                tokens.append(token)
        if len(tokens) > 2:
            return tokens
        return None

    def _prepare_text(self, name_colum):
        # TODO привести к единому виду варианты с нормализацией и без
        self.stopwords_ru.extend(['шт', 'мл'])
        if self.need_normalization:
            self.temp_frame = self.temp_frame.apply(self._lemmatize)
        else:
            temp_list = self.temp_frame.to_list()
            self.text = ' '.join(temp_list)
            self.text = self.text.lower()
            spec_chars = string.punctuation + '\n\xa0«»\t—…'
            self.text = "".join([ch for ch in self.text if ch not in spec_chars])

    def _count_frequency(self):
        if self.need_normalization:
            self.frequency = defaultdict(int)
            for tokens in self.temp_frame.iloc[:]:
                if isinstance(tokens, Iterable):
                    for token in tokens:
                        self.frequency[token] += 1
        else:
            text_tokens = word_tokenize(self.text)
            text_tokens = [token.strip() for token in text_tokens if token not in self.stopwords_ru]
            self.text = nltk.Text(text_tokens)
            self.frequency = FreqDist(self.text)

        final_frame = pd.DataFrame.from_dict(self.frequency, orient='index').reset_index()
        final_frame.columns = ['keyword', 'frequency']
        print(final_frame.sort_values(by='frequency', ascending=False).head(20))

    def use(self, filepath, name_colum, need_normalization=False):
        self.need_normalization = need_normalization
        self._get_text(filepath=filepath, name_colum=name_colum)
        self._prepare_text(name_colum=name_colum)
        self._count_frequency()


test = Find_keywords()
test.use(filepath='./final.xlsx', name_colum='Название',need_normalization=False)
