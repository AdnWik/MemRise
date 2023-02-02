import time
import os
import urllib.request
import re


class Word:

    wordList = []

    def __init__(self, *data):
        for id, english_word, polish_word, level, part_of_speach, audio_file in data:
            if english_word:
                self.id = id
                self.english_word = english_word
                self.polish_word = polish_word
                self.level = level
                self.part_of_speach = part_of_speach
                self.audio_file = audio_file
                Word.wordList.append(self)

    @ staticmethod
    def _read_data():
        """
        Read data from .tsv file
        """
        with open('input\Słówka - Slowka.tsv', 'r', encoding='UTF-8') as file:
            content = file.read().splitlines()
        words = []
        for record in content[1:]:
            words.append(record.split('\t'))

        return words

    @staticmethod
    def create_object():
        """
        Create word object from TSV file
        """
        for data in Word._read_data():
            Word(data)

    @staticmethod
    def show_all_words():
        """
        Show all created word object
        """
        for word in Word.wordList:
            print(
                f'Id: {word.id:<5} Eng: {word.english_word:<50} Pl: {word.polish_word:<30}')

    @property
    def english_word(self):
        return self._english_word

    @english_word.setter
    def english_word(self, value):
        _value = value.replace('.', '')
        _value = re.sub("[\(\[].*?[\)\]]", "", _value)
        while not _value[-1].isalpha():
            _value = _value[:-1]
        self._english_word = _value


Word.create_object()
Word.show_all_words()

"""
for word in Word.wordList:
    buffer = word.english_word
    buffer = buffer.replace('.', '')
    buffer = re.sub("[\(\[].*?[\)\]]", "", buffer)
"""

"""
print(f"a -> {'a'.isalpha()}")
print(f"- -> {'-'.isalpha()}")
print(f"_ -> {'_'.isalpha()}")
print(f"  -> {' '.isalpha()}")
"""
