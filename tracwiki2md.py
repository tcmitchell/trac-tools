#!/usr/bin/env python

'''Convert files from Trac Wiki format to GitHub Flavored Markdown.

Usage:
  python tracwiki2md.py [-h] FILE [FILE ...]

Example:
  python tracwiki2md.py SwPortal_ChangeEmail.txt

If the input filename ends with ".txt" the output filename will have ".txt"
replaced with ".md". For instance, converting Foo.txt will generate Foo.md.
If the input filename ends with anything other than ".txt", ".md" will be
appended to the input filename. For instance, converting Foo.wiki will
generate Foo.wiki.md.

'''

import argparse
import re
import sys


class Converter(object):

    subs = [
            # This first handles things like #!xml
            [r"\{\{\{\s*?[\n\r]{1,2}#!([a-z\/]+)(.*?)\}\}\}", r"```\1\2```"],
            # Single line block quotes
            [r"\{\{\{([^\n]*?)\}\}\}",  r"`\1`"],
            # Multi line block quotes
            [r"\{\{\{(.*?)\}\}\}",  r"```\1```"],
            # These next are for headings
            [r"====\s([^\n]+?)\s====(\s*[\n\r]+)", r'#### \1\2'],
            [r"===\s([^\n]+?)\s===(\s*[\n\r]+)", r'### \1\2'],
            [r"==\s([^\n]+?)\s==(\s*[\n\r]+)", r'## \1\2'],
            [r"=\s([^\n]+?)\s=(\s*[\n\r]+)", r'# \1\2'],
            [r"\!(([A-Z][a-z0-9]+){2,})", r'\1'],
            # These next are italics, bold
            [r"'''(.+)'''", r'*\1*'],
            [r"''(.+)''", r'_\1_'],
            # This was an attempt to avoid converting things that shouldnt, but not quite there yet
#            [r"'''([^\]\'\s\n\,\}\=].*[^\]\'\s\n\,\}\=])'''", r'*\1*'],
#            [r"''([^\]\'\s\n\,\}\=](?!\'\').*(?!\'\')[^\]\'\s\n\,\}\=])''", r'_\1_'],
            # These next 2 are various bulleted or numbered lists
            # This next should probably be beginning-of-line, not beginning-of-field
            # So need to give the MULTILINE, M flag re.M. Or change ^ to \n
            [r"^\s\*", r'*'],
            # Hmm. This next rule turns any #d list at start of field into a header. That makes no sense
            # Probably '\s\d.\s' changed to '\d.\s' is better
#            [r"^\s\d\.", r'#'],
            # This next looks like it tries to strip leading !, getting rid of wikilink escapes
            [r"!(\w)", r"\1"]
            ]

    def __init__(self):
        pass

    def convert(self, text):
        subs = [[re.compile(r, re.DOTALL), s] for r, s in self.subs]
        for p,s in subs:
            text = p.sub(s, text)
        return text

    def convert_file(self, infile, outfile):
        with open(infile, 'r') as inf:
            wiki = inf.read()
        md = self.convert(wiki)
        with open(outfile, 'w') as outf:
            outf.write(md)

def parseArgs(args):
    desc = 'Convert Trac wiki to GitHub Flavored Markdown'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('files', metavar='FILE', nargs='+',
                        help='a file to convert')
    return parser.parse_args()

def main(argv=None):
    if argv is None:
        argv = sys.argv
    args = parseArgs(argv)
    print args
    converter = Converter()
    for inf in args.files:
        if inf.endswith('.txt'):
            outf = inf[:-4] + '.md'
        else:
            outf = inf + '.md'
        converter.convert_file(inf, outf)

if __name__ == "__main__":
    sys.exit(main())

if __name__ == "XX__main__":
    f = 'SwClearinghouse_DatabaseQueries.txt'
    c = Converter()
    with open(f, 'r') as wiki:
        wikiText = wiki.read()
    mdText = c.convert(wikiText)
    print mdText

