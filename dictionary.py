"""Dictionary module"""
import os
from word import Word


class Dictionary:
    """Dictionary"""

    def __init__(self) -> None:
        self.words_list = []
        self.words_without_audio = []

    def load_words_from_file(self):
        """Load words from .tsv file
        """
        with open('input\\Słówka - Slowka.tsv', 'r', encoding='UTF-8') as file:
            content = file.read().splitlines()
        words = []
        for record in content[1:]:
            words.append(record.split('\t'))

        for data in words:
            if data[1]:
                self.words_list.append(Word(data))

    def check_audio_files(self):
        """Check audio files with pronunciation for words
        """
        self.words_without_audio = []
        if not os.path.exists(Word.AUDIO_FILE_PATCH[:-1]):
            os.mkdir(Word.AUDIO_FILE_PATCH[:-1])

        audio_files = [file[:-4]
                       for file in os.listdir(Word.AUDIO_FILE_PATCH[:-1])]
        for word in self.words_list:
            if word.english_word.lower() in audio_files:
                word.audio_file = True

        for word in self.words_list:
            if not word.audio_file:
                self.words_without_audio.append(word)

    def show_all_words(self):
        """Show all words in dictionary
        """
        self.check_audio_files()
        for word in self.words_list:
            print(
                f'Id: {word.id:<5} Eng: {word.english_word:<50} '
                f'Pl: {word.polish_word:<60} Level: {word.level:<12} '
                f'Audio file: {word.audio_file}')

    def show_words_without_audio(self):
        """Show all words without pronunciation
        """
        self.check_audio_files()

        words_without_audio = len(self.words_without_audio)
        if words_without_audio == 0:
            print('All words have audio')
        else:
            print(f'You have {words_without_audio} files without audio:\n')

        for word in self.words_without_audio:
            print(
                f'Id: {word.id:<5} Eng: {word.english_word:<50} '
                f'Pl: {word.polish_word:<60} Level: {word.level:<12} '
                f'Audio file: {word.audio_file}')

    def download_pronunciation_for_words(self):
        """Download audio file for words without pronunciation
        """
        self.check_audio_files()
        for word in self.words_without_audio:
            word.download_audio()
