import re
import pandas
import string


class Find_keywords:
    def __init__(self):
        self.frequency = {}

    def get_text(self, filepath):
        pass
    def count_frequency(self):
        self.frequency = {}
        document_text = open('test.txt', 'r')
        text_string = document_text.read().lower()
        match_pattern = re.findall(r'\b[az]{3, 15}\b', text_string)

        for word in match_pattern:
            count = self.frequency.get(word, 0)
            self.frequency[word] = count + 1

        frequency_list = self.frequency.keys()

        for words in frequency_list:
            print(words, self.frequency[words])
