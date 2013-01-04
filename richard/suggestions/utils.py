from django.conf import settings
from richard.suggestions.models import Suggestion


def mark_if_spam(suggestion):
    """
    Accepts a suggestion instance and checks it's name and comment
    fields for spam words specified in `settings.SPAM_WORDS`.

    If any words are found, it marks the item's state as spam.
    """
    if not settings.SPAM_WORDS:
        return suggestion

    s = ' '.join([suggestion.name, suggestion.comment])
    unique_words = set(
        ''.join(c for c in s.lower() if c.isalnum() or c.isspace()).split())

    for word in settings.SPAM_WORDS:
        if word in unique_words:
            suggestion.state = Suggestion.STATE_SPAM
            suggestion.save()
            break
    return suggestion
