import csv
import os
import django
from django.core.exceptions import ObjectDoesNotExist
from sys import argv

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()

# your imports, e.g. Django models
from capstoneproject.models import Category, Word, Phrase, PhraseSpelling, WordSpelling

categories = Category.objects
words = Word.objects
phrases = Phrase.objects
word_spellings = WordSpelling.objects
phrase_spellings = PhraseSpelling.objects


def csv_reader(path):
    f = open(path, 'r')
    print('opened ' + path.rpartition('/')[2])
    reader = csv.DictReader(f)
    print('header fields:')
    for name in reader.fieldnames:
        print('\t' + name)
    return reader


def import_category(path):
    reader = csv_reader(path)

    for category_entry in reader:
        try:
            category = categories.get(category=category_entry['category'])
        except ObjectDoesNotExist:
            category = Category(category=category_entry['category'])

        try:
            category.weight = category_entry['weight']
        except ValueError:
            print('skipping ' + category_entry['category']
                  + ': weight ' + category_entry['weight'] + ' is not an integer')

        category.save()

    print('import of csv into category table complete\n')


def import_word(path):
    reader = csv_reader(path)

    for word_entry in reader:
        try:
            category = categories.get(category=word_entry['category'])
            words.update_or_create(word=word_entry['word'], category_id=category.id, weight=word_entry['weight'])
        except ObjectDoesNotExist:
            print('skipping ' + word_entry['word'] + ': category \'' + word_entry['category'] + '\' does not exist')
        except ValueError:
            print('skipping ' + word_entry['word'] + ': weight ' + word_entry['weight'] + ' is not an integer')

    print('import of csv into words table complete\n')


def import_phrase(path):
    reader = csv_reader(path)

    for phrase_entry in reader:
        try:
            category = categories.get(category=phrase_entry['category'])
        except ObjectDoesNotExist:
            print('skipping ' + phrase_entry['phrase'] + ': category \'' + phrase_entry['category'] + '\' does not exist')
            continue

        word_set = list()
        for word_word in [phrase_entry['word1'], phrase_entry['word2'], phrase_entry['word3']]:
            if word_word != '':
                try:
                    word_set.append(words.get(word=word_word))
                except ObjectDoesNotExist:
                    print('skipping ' + phrase_entry['phrase'] + ': word \'' + word_word + '\' does not exist')

        try:
            phrase = phrases.get(phrase=phrase_entry['phrase'])
        except ObjectDoesNotExist:
            phrase = Phrase()

        phrase.category_id = category.id
        phrase.phrase = phrase_entry['phrase']
        phrase.weight = phrase_entry['weight']
        phrase.word.clear()
        for word_obj in word_set:
            phrase.word.add(word_obj)
        phrase.save()

    print('import of csv into phrases table complete\n')


def import_phrase_spelling(path):
    reader = csv_reader(path)

    for spelling_entry in reader:
        try:
            phrase = phrases.get(phrase=spelling_entry['phrase'])
        except ObjectDoesNotExist:
            print('skipping ' + spelling_entry['spelling']
                  + ': phrase \'' + spelling_entry['phrase'] + '\' does not exist')
            continue

        phrase_spellings.update_or_create(
            phrase_id=phrase.id,
            spelling=spelling_entry['spelling'],
        )

    print('import of csv into phrases spelling table complete\n')


def import_word_spelling(path):
    reader = csv_reader(path)

    for spelling_entry in reader:
        try:
            word = words.get(word=spelling_entry['word'])
        except ObjectDoesNotExist:
            print('skipping ' + spelling_entry['spelling'] + ': word \'' + spelling_entry['word'] + '\' does not exist')
            continue

        word_spellings.update_or_create(
            word_id=word.id,
            spelling=spelling_entry['spelling'],
        )

    print('import of csv into words spelling table complete\n')


def import_tables(root_folder='', category_path='', word_path='', phrase_path='', wordspelling_path='',
                  phrasespelling_path=''):
    if category_path != '':
        import_category(root_folder + category_path)
    if word_path != '':
        import_word(root_folder + word_path)
    if phrase_path != '':
        import_phrase(root_folder + phrase_path)
    if wordspelling_path != '':
        import_word_spelling(root_folder + wordspelling_path)
    if phrasespelling_path != '':
        import_phrase_spelling(root_folder + phrasespelling_path)
    print('\nall imports complete\n')


def main():
    import_tables(
        root_folder='/Users/jwilliams/Downloads/',
        category_path='Category.csv',
        word_path='Word.csv',
        phrase_path='Phrase.csv',
        wordspelling_path='WordSpelling.csv',
        phrasespelling_path='PhraseSpelling.csv'
    )


if __name__ == '__main__':
    main()
