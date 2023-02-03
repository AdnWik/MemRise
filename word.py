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
    def prepare_word(word):
        preparedWord = []
        preparedWord.append(word.lower())
        if ' ' in word:
            preparedWord.append(word.replace(' ', '_').lower())

        if '-' in word:
            preparedWord.append(word.replace('-', ' ').lower())

        if '-' in word:
            preparedWord.append(word.replace('-', '_').lower())

        if "'" in word:
            preparedWord.append(word.replace("'", '').lower())

        if "'" in word:
            preparedWord.append(word.replace(
                "'", '').replace(' ', '_').lower())

        return preparedWord

    @staticmethod
    def check_audio_files():
        audioFilesList = []
        for file in os.listdir('.\\audio'):
            audioFilesList.append(file[:-4])
        for _ in Word.wordList:
            if _.english_word in audioFilesList:
                _.audio_file = True
            else:
                _.audio_file = False

    @staticmethod
    def download_audio():
        urls = [
            'https://www.diki.pl/images-common/en/mp3/',
            'https://www.diki.pl/images-common/en-ame/mp3/'
        ]
        audio_file_path = '.\\audio\\'
        Word.check_audio_files()
        for word in Word.wordList:
            if word.audio_file == False:
                try:
                    errorN = 0
                    test = Word.prepare_word(word.english_word)
                    print('='*59)
                    for i in test:
                        time.sleep(0.2)
                        try:
                            print(f'Send -> {i}')
                            urllib.request.urlretrieve(
                                urls[0]+i+'.mp3', audio_file_path+word.english_word+'.mp3')
                        except:
                            errorN += 1
                            if errorN == len(test):
                                raise ValueError('ABC')
                            else:
                                pass

                        else:
                            break

                except:
                    print(f'\nERROR <= {word.english_word:<50}')
                else:
                    word.audio_file = True
                    print(f'\nOK <==== {word.english_word:<50}')

    @staticmethod
    def show_words_without_audio():
        Word.check_audio_files()
        wordsWhithoutAudio = []
        for word in Word.wordList:
            if word.audio_file == False:
                wordsWhithoutAudio.append(word.english_word)

        print(f'\nYou have {len(wordsWhithoutAudio)} words without audio')
        print('Do you want to see them ?\n(y/N)')
        show = input('\n-->')
        if show == 'y':
            print('='*100)
            for i in wordsWhithoutAudio:
                print(i)
            print('='*100)

    @staticmethod
    def show_all_words():
        """
        Show all created word object
        """
        Word.check_audio_files()
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
