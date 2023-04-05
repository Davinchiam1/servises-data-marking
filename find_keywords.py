import re
import os
import pandas as pd
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import nltk
from nltk.util import ngrams
from pymorphy3 import MorphAnalyzer
from collections import defaultdict
from collections.abc import Iterable
from data_loading import Data_loading


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
        self.n_grams = 1
        self.text = ''
        self.patterns = "[0-9!#$%&'()*+,./:;<=>?@[\]^_`{|}~—\"\-]+"
        self.lang = language
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
        docs = re.sub(self.patterns, '', docs)
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
        if self.n_grams > 1:
            # stringA = tokens[::self.n_grams]
            # stringB = tokens[1::self.n_grams]
            # if len(stringA) > len(stringB):
            #     stringB.append(' ')
            # tokens = []
            # for i in range(len(stringA)):
            #     tokens.append(stringA[i] + ' ' + stringB[i])
            tokens = list(ngrams(tokens, self.n_grams))
        if len(tokens) > 1:
            return tokens
        return None

    def _prepare_text(self):
        if self.n_grams > 1:
            self.stopwords = ''
            self.patterns = "[!#$%&'()*+,./:;<=>?@[\]^_`{|}~—\"\-]"
        else:
            self.stopwords = stopwords.words(self.lang)
            self.stopwords.extend(['шт', 'мл', "для", "гр", 'л', '№', 'е'])
        self.temp_frame = self.temp_frame.apply(self._tokenize)

    def _count_frequency(self, otput_file):
        self.frequency = defaultdict(int)
        for tokens in self.temp_frame.iloc[:]:
            if isinstance(tokens, Iterable):
                for token in tokens:
                    if self.n_grams > 1:
                        phrase = ''
                        for word in token:
                            phrase = phrase + word + ' '
                        self.frequency[phrase] += 1
                    else:
                        self.frequency[token] += 1

        final_frame = pd.DataFrame.from_dict(self.frequency, orient='index').reset_index()
        final_frame.columns = ['keyword', 'frequency']
        final_frame.to_excel(otput_file, sheet_name='list1', index=False)

    def use(self, name_colum, need_normalization=False, read_xlsx=True, directory=None,
            set_dates=False, filepath=None, n_grams=1, otput_file='./keywords.xlsx'):
        self.need_normalization = need_normalization
        self.n_grams = n_grams
        dl = Data_loading()
        self.temp_frame = dl.get_data(read_xlsx=read_xlsx, directory=directory, set_dates=set_dates, filepath=filepath)
        self.temp_frame = self.temp_frame[name_colum]
        self._prepare_text()
        self._count_frequency(otput_file=otput_file)


test1 = Find_keywords()
# test1.use(filepath='./test.xlsx', otput_file='./test_out1.xlsx', name_colum='Title', n_grams=2)
test1.use(filepath='C:\\Users\\aos.user5\\Desktop\\Масло для лица\\wb\\периоды.xlsx', name_colum='Name',
         need_normalization=False, otput_file="C:\\Users\\aos.user5\\Desktop\\Масло для лица\\масло ключевые очист.xlsx")
