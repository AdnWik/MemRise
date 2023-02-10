from word import Word


Word.create_object()
print("\nHello! \nThis program downloads audio files with the English pronunciation of the words you pass on in the file '.tsv'.\nGood luck!")

while True:
    print('\nWhat do you want to do?')

    print('0 - END\n1 - Show all words\n2 - Show words without audio files\n3 - Download the pronunciation for words\n ')
    choice = int(input('-->'))

    if choice == 0:
        break

    elif choice == 1:
        Word.show_all_words()

    elif choice == 2:
        Word.show_words_without_audio()

    elif choice == 3:
        print("\nProcessing........")
        Word.download_audio()

print('\nEnd')
