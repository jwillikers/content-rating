import csv
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()

# your imports, e.g. Django models
import capstoneproject.models


def import_category(path):
    f = open(path, 'r')
    reader = csv.reader(f)

    for row in reader:
        row0 = row[0]
        if row0 != 'category':
            _, created = capstoneproject.models.Category.objects.get_or_create(
                category=row0,
                weight=row[1],
            )


def import_word(path):
    f = open(path);
    reader = csv.reader(f)

    for row in reader:
        row0 = row[0]
        if row0 != 'category':
            _, created = capstoneproject.models.Word.objects.get_or_create(
                category=capstoneproject.models.Category.objects.get(pk=row[0]),
                word=row[1],
                weight=row[2],
            )


def import_phrase(path):
    f = open(path)
    reader = csv.reader(f)

    for row in reader:
        row0 = row[0]
        if row0 != 'category':
            _, created = capstoneproject.models.Phrase.objects.get_or_create(
                category=capstoneproject.models.Category.objects.get(pk=row[0]),
                phrase=row[1],
                weight=row[2],
                word=capstoneproject.models.Word.objects.get(pk=row[3]),
            )


def import_spelling(path):
    f = open(path)
    reader = csv.reader(f)

    for row in reader:
        row0 = row[0]
        if row0 != 'word':
            _, created = capstoneproject.models.Spelling.objects.get_or_create(
                word_or_phrase=row0,
                spelling=row[1],
            )


def main():
    import_phrase("/Users/jwilliams/Downloads/Phrase.csv")


if __name__ == '__main__':
    main()
