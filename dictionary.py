import os
from word import Word


class Dictionary:
    audioFilePath = '.\\audio\\'

    def __init__(self) -> None:
        self.wordList = []
        self.wordWithoutAudio = []

    def load_words_from_file(self):
        with open('input\Słówka - Slowka.tsv', 'r', encoding='UTF-8') as file:
            content = file.read().splitlines()
        words = []
        for record in content[1:]:
            words.append(record.split('\t'))

        for data in words:
            if data[1]:
                self.wordList.append(Word(data))

    def check_audio_files(self):
        # print(Word.audioFilePath)
        # print(Word.audioFilePath[:-1])
        if not os.path.exists(Dictionary.audioFilePath[:-1]):
            os.mkdir(Dictionary.audioFilePath[:-1])

        audioFiles = [file[:-4]
                          for file in os.listdir(Dictionary.audioFilePath[:-1])]
        for word in self.wordList:
            if word.english_word in audioFiles:
                word.audio_file = True

    def show_all_words(self):
        self.check_audio_files()
        for word in self.wordList:
            print(
                f'Id: {word.id:<5} Eng: {word.english_word:<50} Pl: {word.polish_word:<60} Level: {word.level:<12} Audio file: {word.audio_file}')

    def show_words_without_audio(self):
        self.check_audio_files()
        for word in self.wordList:
            if not word.audio_file:
                self.wordWithoutAudio.append(word)

        wordsWithoutAudio = len(self.wordWithoutAudio)
        if wordsWithoutAudio == 0:
            print('All words have audio')
        else:
            print(f'You have {wordsWithoutAudio} files without audio:\n')

        for word in self.wordWithoutAudio:
            print(
                f'Id: {word.id:<5} Eng: {word.english_word:<50} Pl: {word.polish_word:<60} Level: {word.level:<12} Audio file: {word.audio_file}')

if __name__ == "__main__":
    dictionary1 = Dictionary()
    dictionary1.load_words_from_file()
    dictionary1.check_audio_files()
    dictionary1.show_all_words()
