
# Malt

Malt is a static website generator built in Python. It transforms a directory of text files into a WordPress-style website with support for pages, posts, and custom post types.

    $ malt --help

    Usage: malt [FLAGS] [COMMAND]

      Malt is a static website generator. It transforms a directory of text
      files into a self-contained website.

    Flags:
      --help            Print the application's help text and exit.
      --version         Print the application's version number and exit.

    Commands:
      build             Build the current site.
      clear             Clear the output directory.
      init              Initialize a new site directory.
      serve             Run a web server on the site's output directory.
      watch             Monitor the site directory and rebuild on changes.

    Command Help:
      help <command>    Print the specified command's help text and exit.

  See the [documentation][docs] or [demo site][demo] for details.

  [docs]: http://www.dmulholl.com/docs/malt/
  [demo]: http://www.dmulholl.com/demos/malt
