"""Words module"""
import time
from urllib import request
import re
import json
from my_exception import Downloaded


class Word:
    """Word"""
    AUDIO_FILE_PATCH = '.\\audio\\'

    def __init__(self, *data):
        for id, english_word, polish_word, level, part_of_speech in data:
            self.id = id
            self.english_word = english_word
            self.polish_word = polish_word
            self.level = level
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

    def download_audio(self) -> None:
        """Download pronunciation for word from
        diki.pl or soundoftext.com

        Raises:
            Downloaded: download successfully
        """
        prepared_word = self.prepare_word()
        urls = {
            'Diki.pl(EN)': 'https://www.diki.pl/images-common/en/mp3/',
            'Diki.pl(EN-AME)': 'https://www.diki.pl/images-common/en-ame/mp3/',
            'SoundOfText.com(EN)': 'https://api.soundoftext.com/sounds'
        }

        try:
            print('='*59)
            for url_name, url in urls.items():
                print(f'\nTry download from: {url_name}')

                # Diki.pl
                if 'Diki' in url_name:
                    for word in prepared_word:
                        time.sleep(0.2)
                        try:
                            print(f'Send -> {word}')
                            request.urlretrieve(
                                url+word+'.mp3',
                                Word.AUDIO_FILE_PATCH+prepared_word[0]+'.mp3'
                                )
                        except Exception:
                            pass
                        else:
                            raise Downloaded

                # soundoftext.com
                if 'SoundOfText' in url_name:
                    data = {
                        'engine': 'Google',
                        'data': {'text': prepared_word[0], 'voice': 'en-GB'}
                        }
                    data = json.dumps(data)
                    data = data.encode('UTF-8')
                    try:
                        print(f'Send -> {prepared_word[0]}')
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
                            request.urlretrieve(
                                content['location'],
                                Word.AUDIO_FILE_PATCH+prepared_word[0]+'.mp3'
                                )

                    except Exception:
                        pass
                    else:
                        raise Downloaded

            print(f'\nERROR <= {self.english_word:<50}')
        except Downloaded:
            self.audio_file = True
            print(f'\nOK <==== {self.english_word:<50}')

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
