import sqlite3
import time
import os
import urllib.request
import re


class Word:

    wordList = []

    def __init__(self, *data):
        for id, english_word, polish_word, level, part_of_speach, audio_file in data:
            if english_word:
                self._id = id
                self.english_word = english_word
                self.polish_word = polish_word
                self._level = level
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
    def download_audio():
        urls = [
            'https://www.diki.pl/images-common/en/mp3/',
            'https://www.diki.pl/images-common/en-ame/mp3/'
        ]
        for word in Word.wordList:
            time.sleep(1)
            try:
                urllib.request.urlretrieve(
                    urls[0]+word.english_word+'.mp3', '.\\audio\\'+word.english_word+'.mp3')

            except:
                word.audio_file = False
                print(f'ERROR: {word.english_word}')
            else:
                word.audio_file = True
                print(f'Download - OK: {word.english_word}')

    @staticmethod
    def show_all_words():
        """
        Show all created word object
        """
        for word in Word.wordList:
            print(
                f'Id: {word.id:<5} Eng: {word.english_word:<50} Pl: {word.polish_word:<60} Level: {word.level:<12} audio_file: {word.audio_file}')

    @property
    def id(self):
        return self._id

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

    @property
    def level(self):
        return self._level

    @property
    def audio_file(self):
        return self._audio_file

    @audio_file.setter
    def audio_file(self, value):
        if isinstance(value, bool):
            self._audio_file = value

        elif value == 1 or value == '1':
            self._audio_file = True

        else:
            self._audio_file = False


def sql():
    con = sqlite3.connect('test.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    cur.execute("DROP TABLE IF EXISTS words;")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS words (
            id INTEGER PRIMARY KEY NOT NULL,
            english_word varchar(250) NOT NULL,
            polish_word varchar(250) NOT NULL,
            level varchar(250) NOT NULL,
            part_of_speach varchar(250) NOT NULL,
            audio_file BOOLEAN NOT NULL 
        )""")

    cur.execute(
        'INSERT INTO words VALUES(?,?,?,?,?,?);',
        (1, 'this is ', 'test', 'pierwszy', 'ogolny', True)
    )
    cur.execute(
        'INSERT INTO words VALUES(?,?,?,?,?,?);',
        (2, 'this is ', 'test', 'drugi', 'ogolny', False)
    )
    con.commit()


Word.create_object()
Word.show_all_words()
# Word.download_audio()
# Word.show_all_words()
