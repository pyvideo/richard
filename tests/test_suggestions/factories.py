import factory

from richard.suggestions import models


class SuggestionFactory(factory.DjangoModelFactory):
    name = factory.Sequence(lambda x: '{:08d}'.format(x))
    url = factory.Sequence(lambda x: 'http://www.site{}.com'.format(x))

    class Meta:
        model = models.Suggestion
