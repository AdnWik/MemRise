from word import Word


class Dictionary:
    audioFilePath = '.\\audio\\'

    def __init__(self) -> None:
        self.wordList = []

    def load_words_from_file(self):
        with open('input\Słówka - Slowka.tsv', 'r', encoding='UTF-8') as file:
            content = file.read().splitlines()
        words = []
        for record in content[1:]:
            words.append(record.split('\t'))

        for data in words:
            if data[1]:
                print(data)
                self.wordList.append(Word(data))

    def show_all_words(self):
        for word in self.wordList:
            print(
                f'Id: {word.id:<5} Eng: {word.english_word:<50} Pl: {word.polish_word:<60} Level: {word.level:<12}')


dictionary1 = Dictionary()
dictionary1.load_words_from_file()
dictionary1.show_all_words()
