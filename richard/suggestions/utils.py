from django.conf import settings
from richard.suggestions.models import Suggestion


def mark_if_spam(suggestion):
    """
    Accepts a suggestion instance and checks it's name
    and comment fields for spam words.

    If any words are found, it marks the item's state as spam.
    """
    # parse suggestion text into a list of containing only unique alphnum words
    s = ' '.join([suggestion.name, suggestion.comment])
    unique_words = set(''.join(c for c in s if c.isalnum() or c.isspace()).split())

    for word in settings.SPAM_WORDS:
        if word in unique_words:
            suggestion.state = Suggestion.STATE_SPAM
            suggestion.save()
            break
    return suggestion
