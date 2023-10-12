import time
from urllib import request
import re
import json
from my_exception import Downloaded

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
        preparedWord = self.prepare_word()
        urls = {
            'Diki.pl (EN)': 'https://www.diki.pl/images-common/en/mp3/',
            'Diki.pl (EN-AME)': 'https://www.diki.pl/images-common/en-ame/mp3/',
            'SoudOfText.com (EN)': 'https://api.soundoftext.com/sounds'
        }

        try:
            print('='*59)
            for url_name, url in urls.items():
                print(f'\nTry download from: {url_name}')

                # Diki.pl
                if 'Diki' in url_name:
                    for word in preparedWord:
                        time.sleep(0.2)
                        try:
                            print(f'Send -> {word}')
                            request.urlretrieve(url+word+'.mp3', AUDIO_FILE_PATCH+preparedWord[0]+'.mp3')
                        except Exception:
                            pass
                        else:
                            raise Downloaded

                # soundoftext.com
                if 'SoudOfText' in url_name:
                    data = {
                        'engine': 'Google',
                        'data': {'text': preparedWord[0], 'voice': 'en-GB'}
                        }
                    data = json.dumps(data)
                    data = data.encode('UTF-8')
                    try:
                        print(f'Send -> {preparedWord[0]}')
                        req = request.Request(url, method='POST')
                        req.add_header('Content-Type', 'application/json')
                        r = request.urlopen(req, data=data)
                        content = json.loads(r.read())

                        if content['success']:
                            sound_url = url+"/"+str(content['id'])
                            req = request.Request(sound_url, method='GET')
                            r = request.urlopen(req, data=data)
                            content = json.loads(r.read())

                        if content['status'] == 'Done':
                            request.urlretrieve(content['location'], AUDIO_FILE_PATCH+preparedWord[0]+'.mp3')

                    except Exception:
                        pass
                    else:
                        raise Downloaded

            print(f'\nERROR <= {self.english_word:<50}')
        except Downloaded:
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
