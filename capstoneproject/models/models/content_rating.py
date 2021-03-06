from django.contrib.auth.models import User
from django.db.models import Model, ForeignKey, ManyToManyField, \
    DateTimeField, Manager, CASCADE


class ContentRating(Model):
    """
    This Model contains data related to one rated content,
    its overall rating, category ratings, word counts,
    and created and updated dates.
    """
    from capstoneproject.models.models.category_rating import CategoryRating
    from capstoneproject.models.models.content import Content
    from capstoneproject.models.models.word_count import WordCount
    from capstoneproject.models.fields.rating_field import RatingField
    content = ForeignKey(
        'Content',
        related_name='content_ratings',
        on_delete=CASCADE)
    rating = RatingField(default=0)
    category_ratings = ManyToManyField(
        CategoryRating,
        related_name='content_ratings')
    word_counts = ManyToManyField(WordCount, related_name='content_ratings')
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)
    content_ratings = Manager()

    def __str__(self):
        string = 'Rating\n'
        string += '  Content: {}\n'.format(self.content)
        string += '  Overall Rating: {}\n'.format(self.rating)
        string += '  Category Ratings: {}\n'.format(self.category_ratings)
        string += '  Word Counts: {}\n'.format(self.word_counts)
        string += '  Created: {}    Updated: {}\n'. format(
            self.created, self.updated)
        return string

    def isRelated(self):
        """
        Determines if any relatives rely on this model instance.
        :return: True if relatives rely on this model instance.
        """
        return len(self.user_storage.all()) > 0

    def isOrphaned(self):
        """
        Determines if no relatives rely on this model instance.
        :return: True if no relatives rely on this model instance.
        """
        return len(self.user_storage.all()) == 0

    def delete_relatives(self):
        """
        Deletes relatives to this model.
        :return:
        """
        category_ratings = list(self.category_ratings.all())
        self.category_ratings.clear()
        for category_rating in category_ratings:
            if category_rating.isOrphaned():
                category_rating.delete()

        word_counts = list(self.word_counts.all())
        self.word_counts.clear()
        for word_count in word_counts:
            if word_count.isOrphaned():
                word_count.delete()

    def delete(self, *args, **kwargs):
        """
        Deletes this model after deleting its relatives.
        :return:
        """
        self.delete_relatives()
        old_content = self.content
        super().delete(*args, **kwargs)
        if old_content.isOrphaned():
            old_content.delete()

    def get_category_ratings(self):
        """
        Retrieves the CategoryRatings for this Category.
        :return: a dict of CategoryRatings.
        """
        category_ratings = dict()
        for cat_rating in self.category_ratings.all():
            category_ratings[cat_rating.category.name] = cat_rating.rating
        return category_ratings

    def _create_word_count_dict(self):
        """
        Compile a dictionary of the WordCounts for this ContentRating.
        :return: a dictionary of Words and their Counts.
        """
        word_counts = dict()
        for wc in self.word_counts.all():
            word_counts[wc.word.name] = wc.count
        return word_counts

    def get_word_count_category(self):
        """
        Compile a dictionary of the WordCounts for this ContentRating's \
        Categories.
        :return: a dictionary of Categories, Words, and their Counts.
        """
        word_count_category_dict = dict()
        from capstoneproject.models.models.category import Category
        for cat in Category.categories.all():
            word_count_category_dict[cat.name] = dict()

        word_count_dict = self._create_word_count_dict()
        for word, count in word_count_dict.items():
            from capstoneproject.models.models.word import Word
            word_model = Word.words.get_word(word=word)
            for word_cat in word_model.get_categories():
                word_count_category_dict[word_cat][word] = count

        return word_count_category_dict

    class Meta:
        """Settings for the ContentRating model."""
        default_manager_name = 'content_ratings'
