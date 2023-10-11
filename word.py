import time
import urllib.request
import re

AUDIO_FILE_PATCH = '.\\audio\\'


class Word:

    def __init__(self, *data):
        for id, english_word, polish_word, level, part_of_speech in data:
            self._id = id
            self.english_word = english_word
            self.polish_word = polish_word
            self._level = level
            self.part_of_speech = part_of_speech
            self.audio_file = False

    def prepare_word(self) -> list:
        """Prepare english word to download

        Returns:
            list: modified english word
        """

        preparedWord = []
        preparedWord.append(self.english_word.lower())

        if 'é' in self.english_word:
            preparedWord.append(self.english_word.replace('é', 'e').lower())

        if ' ' in self.english_word:
            preparedWord.append(self.english_word.replace(
                ' ', '_').replace('é', 'e').lower())

        if '-' in self.english_word:
            preparedWord.append(self.english_word.replace(
                '-', ' ').replace('é', 'e').lower())

        if '-' in self.english_word:
            preparedWord.append(self.english_word.replace(
                '-', '_').replace('é', 'e').lower())

        if "'" in self.english_word:
            preparedWord.append(self.english_word.replace(
                "'", '').replace('é', 'e').lower())

        if "'" in self.english_word:
            preparedWord.append(self.english_word.replace(
                "'", '').replace(' ', '_').replace('é', 'e').lower())

        if "'" in self.english_word:
            preparedWord.append(self.english_word.replace(
                "'", ' ').replace(' ', '_').replace('é', 'e').lower())

        return preparedWord

    def download_audio(self):
        urls = [
            'https://www.diki.pl/images-common/en/mp3/',
            'https://www.diki.pl/images-common/en-ame/mp3/'
        ]

        try:
            errors = 0
            preparedWord = self.prepare_word()
            print('='*59)
            for word in preparedWord:
                time.sleep(0.2)
                try:
                    print(f'Send -> {word}')
                    urllib.request.urlretrieve(urls[0]+word+'.mp3', AUDIO_FILE_PATCH+self.english_word+'.mp3')
                except:
                    errors += 1
                    if errors == len(preparedWord):
                        raise ValueError('error')
                    else:
                        pass

                else:
                    break

        except:
            print(f'\nERROR <= {self.english_word:<50}')
        else:
            self.audio_file = True
            print(f'\nOK <==== {self.english_word:<50}')

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
