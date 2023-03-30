import re
import os
import pandas as pd
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import nltk
from pymorphy3 import MorphAnalyzer
from collections import defaultdict
from collections.abc import Iterable


# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('averaged_perceptron_tagger')

def _get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)


class Find_keywords:
    def __init__(self, language="russian"):
        self.frequency = {}
        self.temp_frame = None
        self.text = ''
        self.patterns = "[0-9!#$%&'()*+,./:;<=>?@[\]^_`{|}~—\"\-]+"
        self.stopwords = stopwords.words(language)
        self.lang=language
        if language == "russian":
            self.morph = MorphAnalyzer()
        else:
            self.morph = WordNetLemmatizer()

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
            if token and token not in self.stopwords:
                token = token.strip()
                if self.need_normalization:
                    if self.lang != 'russian':
                        token = self.morph.lemmatize(token, _get_wordnet_pos(token)).lower()
                    else:
                        token = self.morph.normal_forms(token)[0]
                else:
                    token = token.lower()
                tokens.append(token)
        if len(tokens) > 1:
            return tokens
        return None

    def _prepare_text(self, name_colum):
        self.stopwords.extend(['шт', 'мл'])
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


test = Find_keywords(language="english")
test.use(filepath='./123.xlsx', name_colum='Title', need_normalization=True)
