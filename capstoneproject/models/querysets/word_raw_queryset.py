from django.db.models import RawQuerySet


class WordRawQuerySet(RawQuerySet):
    def user(self, user_id):
        return self.raw('''
SELECT
    w.id
    w.name

FROM capstoneproject_userstorage_words AS uw
INNER JOIN capstoneproject_word AS w ON uw.word_id = w.id

WHERE uw.userstorage_id = %s
''', [user_id])

    def category(self, category_id):
        return self.raw('''
SELECT
    w.id
    w.name

FROM capstoneproject_word AS w
INNER JOIN capstoneproject_userstorage_word_features AS uf
    ON u.id = uf.userstorage_id
INNER JOIN capstoneproject_wordfeature AS f
    ON uf.wordfeature_id = f.id

WHERE f.category_id = %s
''', [category_id])

    def user_category(self, user_id, category_id):
        return self.raw('''
SELECT
    w.id
    w.name

FROM capstoneproject_userstorage AS u
INNER JOIN capstoneproject_userstorage_words AS uw
    ON u.id = uw.userstorage_id
INNER JOIN capstoneproject_word AS w
    ON uw.word_id = w.id
INNER JOIN capstoneproject_userstorage_word_features AS uf
    ON u.id = uf.userstorage_id
INNER JOIN capstoneproject_wordfeature AS f
    ON uf.wordfeature_id = f.id

WHERE uw.userstorage_id = %s
''', [user_id])
