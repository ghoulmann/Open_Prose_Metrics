# -*- coding: utf-8 -*-

from docutils import core


def html_parts(input_string):
    """
    Given an input string, returns a dictionary of HTML document parts.

    Dictionary keys are the names of parts, and values are Unicode strings;
    encoding is up to the client.

    Parameters:

    - `input_string`: A multi-line text string; required.
    - `source_path`: Path to the source file or object.  Optional, but useful
      for diagnostic output (system messages).
    - `destination_path`: Path to the file or object which will receive the
      output; optional.  Used for determining relative paths (stylesheets,
      source links, etc.).
    - `input_encoding`: The encoding of `input_string`.  If it is an encoded
      8-bit string, provide the correct encoding.  If it is a Unicode string,
      use "unicode", the default.
    - `doctitle`: Disable the promotion of a lone top-level section title to
      document title (and subsequent section title to document subtitle
      promotion); enabled by default.
    - `initial_header_level`: The initial level for header elements (e.g. 1
      for "<h1>").
    """
    #overrides = {'input_encoding': 'unicode',
    #             'doctitle_xform': doctitle,
    #             'initial_header_level': initial_header_level}
    parts = core.publish_parts(input_string, writer_name='html', settings_overrides={'input_encoding':'unicode', 'report_level':5})
    return parts

def html_body(input_string, output_encoding='utf-8', doctitle=False):
    parts = html_parts(input_string)
    fragment = parts['html_body']
    if output_encoding != 'unicode':
        fragment = fragment.encode(output_encoding)
    return fragment
