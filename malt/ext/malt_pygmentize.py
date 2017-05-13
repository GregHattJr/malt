# --------------------------------------------------------------------------
# This extension registers a syntax-highlighting shortcode. The shortcode
# accepts an optional argument specifying the language:
#
#   [% code lang %] ... [% endcode %]
#
# Syntax highlighting is applied using the Pygments package. If no language
# is specified, Pygments will attempt to guess the correct lexer to use.
#
# If the Pygments package is not available or if an appropriate lexer cannot
# be found the shortcode will return the wrapped content with HTML special
# characters escaped.
# --------------------------------------------------------------------------

import html

try:
    import shortcodes
except ImportError:
    shortcodes = None

try:
    import pygments
    import pygments.lexers
    import pygments.formatters
except ImportError:
    pygments = None


# The shortcodes package is an optional dependency.
if shortcodes:

    @shortcodes.register('code', 'endcode')
    def handler(record, content, pargs, kwargs):
        lang = pargs[0] if pargs else ''

        if pygments:
            code = pygmentize(content, lang)
        else:
            code = html.escape(content)

        if lang:
            fmt = '<pre class="lang-%s" data-lang="%s">\n%s\n</pre>'
            return fmt % (lang, lang, code.strip('\n'))
        else:
            return '<pre>\n%s\n</pre>' % code.strip('\n')


def pygmentize(code, lang):
    if lang:
        try:
            lexer = pygments.lexers.get_lexer_by_name(lang)
        except pygments.util.ClassNotFound:
            lexer = None
    else:
        try:
            lexer = pygments.lexers.guess_lexer(code)
        except pygments.util.ClassNotFound:
            lexer = None

    if lexer:
        formatter = pygments.formatters.HtmlFormatter(nowrap=True)
        return pygments.highlight(code, lexer, formatter)
    else:
        return html.escape(code)
