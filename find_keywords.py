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
    def __init__(self, language="russian"):
        self.frequency = {}
        self.temp_frame = None
        self.text = ''
        self.patterns = "[0-9!#$%&'()*+,./:;<=>?@[\]^_`{|}~—\"\-]+"
        self.stopwords_ru = stopwords.words(language)
        self.morph = MorphAnalyzer()

    def _get_text(self, filepath, name_colum, selection=None):
        if filepath.split('.')[-1].lower() == 'csv':
            self.temp_frame = pd.read_csv(filepath, delimiter=';')
        elif filepath.split('.')[-1].lower() == 'xlsx':
            self.temp_frame = pd.read_excel(filepath)
        if selection is not None:
            self.temp_frame = self.temp_frame.loc[self.temp_frame[selection[0]] == selection[1]]
        self.temp_frame = self.temp_frame[name_colum]

    def _tokenize(self, docs):
        docs = re.sub(self.patterns, ' ', docs)
        tokens = []
        for token in docs.split():
            if token and token not in self.stopwords_ru:
                token = token.strip()
                if self.need_normalization:
                    token = self.morph.normal_forms(token)[0]
                else:
                    token = token.lower()
                tokens.append(token)
        if len(tokens) > 2:
            return tokens
        return None

    def _prepare_text(self, name_colum):
        self.stopwords_ru.extend(['шт', 'мл'])
        self.temp_frame = self.temp_frame.apply(self._tokenize)

    def _count_frequency(self):
        self.frequency = defaultdict(int)
        for tokens in self.temp_frame.iloc[:]:
            if isinstance(tokens, Iterable):
                for token in tokens:
                    self.frequency[token] += 1

        final_frame = pd.DataFrame.from_dict(self.frequency, orient='index').reset_index()
        final_frame.columns = ['keyword', 'frequency']
        print(final_frame.sort_values(by='frequency', ascending=False).head(30))

    def use(self, filepath, name_colum, need_normalization=False):
        self.need_normalization = need_normalization
        self._get_text(filepath=filepath, name_colum=name_colum)
        self._prepare_text(name_colum=name_colum)
        self._count_frequency()


test = Find_keywords()
test.use(filepath='./final1.xlsx', name_colum='Название', need_normalization=True)
