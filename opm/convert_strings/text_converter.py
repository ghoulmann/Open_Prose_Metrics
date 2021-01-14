"""
place for string conversion functions
"""
from docutils import core
def text_to_html(unicode_text):
    """
    Convert unicode text string to properly encoded HTML entities and tags
    :param unicode_text: is the input string
    :returns: html tagged string without warnings
    """
    # dict of setting_overrides for docutils.core
    overrides = {
        'input_encoding':'unicode',
        'writer_name':'html',
        'report_level':5
    }
    parts = core.publish_parts(unicode_text, settings_overrides=overrides)
    return mark_safe(force_unicode(parts['html_body']))
