from django.urls.converters import StringConverter


class UnicodeSlugConverter(StringConverter):
    """Custom converter that allows Unicode characters in slugs"""

    regex = r"[-\w\u0080-\uffff]+"
