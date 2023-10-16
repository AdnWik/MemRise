"""Main module"""
from menu import show_menu
from dictionary import Dictionary


WELCOME_MESSAGE = (
    "\nHello! \nThis program downloads audio files with the "
    "English pronunciation of the words you pass on in the "
    "file '.tsv'.\n"
)
START_MESSAGE = '\nWhat do you want to do?'
options = ['Show all words',
           'Show words without audio files',
           'Download the pronunciation for words']

dictionary = Dictionary()
dictionary.load_words_from_file()

print(WELCOME_MESSAGE)

while True:
    print(show_menu(start_message=START_MESSAGE, menu_options=options))
    choice = input('-->')

    if choice == '1':
        dictionary.show_all_words()

    elif choice == '2':
        dictionary.show_words_without_audio()

    elif choice == '3':
        print("\nProcessing........")
        dictionary.download_pronunciation_for_words()

    else:
        break


print('\nEnd')
