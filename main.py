from word import Word


Word.create_object()
print("\nWitaj! \nTen program pobiera pliki audio z angielską wymową słowek które przekażesz w pliku '.tsv'.\nPowodzenia!")

while True:
    print('\nCo chesz teraz zrobic?')

    print('0 - ZAKOŃCZ\n1 - Pokaż wszystkie słówka\n2 - Pokaż słówka bez plików audio\n3 - Pobierz wymowę do słówek\n ')
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

print('\nKoniec')
