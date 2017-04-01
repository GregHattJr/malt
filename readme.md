
# Ark

Ark is a static website generator built in Python. It transforms a
directory of text files into a self-contained website.

* Ark is extensible. It has builtin support for source files written
  in [Markdown][] and [Syntex][], but can be extended via plugins to support
  any similar text-to-html format.

* Ark is flexible. By default it produces sites with page-relative links
  that can be viewed locally via the filesystem without any need for a web
  server (ideal for distributing project documentation in html format), but it
  can easily produce sites with resource or directory-style urls.

See Ark's [documentation][docs] or the Ark [demo site][demo] for further details.

[Markdown]: http://daringfireball.net/projects/markdown/
[Syntex]: https://github.com/dmulholland/syntex
[docs]: http://mulholland.xyz/docs/ark/
[demo]: http://ark.mulholland.xyz/phoenix/



## Interface

Run`ark --help` to view the application's command-line help text:

    Usage: ark [FLAGS] [COMMAND]

      Ark is a static website generator. It transforms a directory of text
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

Run `ark help <command>` to view the help text for a specific command.



## Installation

Install directly from the Python Package Index using `pip`:

    $ pip install ark

Ark requires Python 3.5 or later.



## License

This work has been placed in the public domain.
