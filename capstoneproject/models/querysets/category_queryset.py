from django.db.models import QuerySet


class CategoryQuerySet(QuerySet):
    """Category model QuerySet for simplifying queries."""

    def default(self):
        """
        Filter the QueryString to only include default values.
        :return: A CategoryQuerySet containing only default Categories.
        """
        return self.filter(default=True)

    def of_user(self, user_id):
        """
        Filter the QueryString to only include this User's Categories.
        :param user_id: Id of the User model instance.
        :return: A Raw CategoryQuerySet containing only the User's Categories.
        """
        from capstoneproject.models.models.category import Category
        return self.raw('''
SELECT
    c.id,
    c.name,
    c.weight

FROM capstoneproject_userstorage_categories AS uc
INNER JOIN capstoneproject_category AS c
    ON uc.category_id = c.id

WHERE uc.userstorage_id = %s
''', [user_id])
