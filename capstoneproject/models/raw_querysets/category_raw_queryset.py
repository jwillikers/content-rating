from django.db.models import Category


class CategoryRawQuerySet(RawQuerySet):
    def user(self, user_id):
        return Category.categories.raw('''
SELECT
    c.id
    c.name
    c.weight

FROM capstoneproject_userstorage_categories AS uc
INNER JOIN capstoneproject_category AS c
    ON uc.category_id = c.id

WHERE uc.userstorage_id = %s
''', [user_id])