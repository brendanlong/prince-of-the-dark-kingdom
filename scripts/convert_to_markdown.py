#!/usr/bin/env python3
import argparse
import itertools
import os
import re
import subprocess
import sys

CHAPTER_ENDS = [
    0,
    20,
    41,
    62,
    82,
    110,
    139
]

NUMERALS = [
    "I",
    "II",
    "III",
    "IV",
    "V",
    "VI",
    "VII",
    "VIII",
    "IX",
    "X"
]

AUTHORS_NOTE_REGEX = re.compile("^(\\\~ )?Author'?s notes?(:|\\\~).*", flags=re.IGNORECASE)
CHAPTER_REGEX = re.compile("^(Epilogue)|^(\*\*)?Chapter [0-9]+[:-]? *([^*]*)(\*\*)?$")
FOOTNOTE_REGEX = re.compile("^([0-9]+)[.)] (.+)")
PAGE_BREAK_REGEX = re.compile("^(\* )+\*$|^o+$|^\\\~ *Page Break(er)?s? *\\\~$", flags=re.IGNORECASE)

class Chapter(object):
    def __init__(self, number):
        self.title = None
        self.part = None
        self.lines = []
        self.number = number

    def get_title(self):
        if self.part:
            return "{} {}".format(self.title, NUMERALS[self.part - 1])
        else:
            return self.title

def write_book(output_dir, book_number, chapters):
    book_dir = os.path.join(args.output_dir, "book-{}".format(book_number))
    if not os.path.isdir(book_dir):
        os.makedirs(book_dir)

    title_file = os.path.join(book_dir, "title.txt")
    if not os.path.isfile(title_file):
        with open(title_file, "w") as f:
            f.write("% Prince of the Dark Kingdom: Book {}\n"
                "% Mizuni-sama".format(book_number))

    for chapter in chapters:
        with open(os.path.join(book_dir, "chapter-{:02d}.md".format(chapter.number)), "w") as f:
            f.write("# {}\n\n".format(chapter.get_title()))
            f.write("\n".join(chapter.lines))
            f.write("\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", "-i", required=True)
    parser.add_argument("--output-dir", "-o", required=True)
    args = parser.parse_args()

    book_number = 1
    chapter_number = 1
    chapters = []
    for i in itertools.count(1):
        filename = os.path.join(args.input_dir, "chapter-{:03d}.html".format(i))
        if not os.path.isfile(filename):
            write_book(args.output_dir, book_number, chapters)
            break

        print("Importing Book {} Chapter {} ({})".format(book_number, chapter_number, i))

        story_text = subprocess.check_output(["pandoc", "-t", "markdown", filename]).decode("UTF-8")

        next_note = 1
        chapter = Chapter(chapter_number)
        lines = story_text.splitlines()
        in_authors_note = False
        in_footnote = False
        skip_paragraphs = 0
        for line_number, line in enumerate(lines):
            line = line.strip().strip(chr(8203))
            if not chapter.title:
                match = CHAPTER_REGEX.search(line)
                if match is not None:
                    if match.group(1) or match.group(3):
                        chapter.title = match.group(1) or match.group(3)
                        words = chapter.title.split()
                        if words[-1] in NUMERALS:
                            chapter.part = NUMERALS.index(words[-1]) + 1
                            words.pop()
                            if words[-1].lower() == "part":
                                words.pop()
                            chapter.title = " ".join(words)
                    else:
                        if not chapters[-1].part:
                            chapters[-1].part = 1
                        chapter.title = chapters[-1].title
                        chapter.part = chapters[-1].part + 1
            elif PAGE_BREAK_REGEX.match(line):
                # Remove superfluous horizontal rules at the end of files
                if line_number == len(lines) - 1:
                    continue
                # Remove duplicate horizontal rules
                if len(chapter.lines) > 1 and chapter.lines[-2] == "---":
                    continue
                chapter.lines.append("---")
            elif AUTHORS_NOTE_REGEX.match(line):
                # Book 6 chapter 5 has an authors note at the beginning..
                if book_number == 6 and chapter_number == 5:
                    skip_paragraphs = 2
                else:
                    in_authors_note = True
            elif not line:
                if skip_paragraphs:
                    skip_paragraphs -= 1
                if in_footnote or not (in_authors_note or skip_paragraphs):
                    # Don't print duplicate empty lines
                    if len(chapter.lines) and chapter.lines[-1]:
                        chapter.lines.append(line)
                if in_footnote:
                    in_footnote = False
            else:
                match = FOOTNOTE_REGEX.search(line)
                if match is not None:
                    chapter.lines.append("[^{}-{}]: {}".format(i, match.group(1), match.group(2)))
                    in_footnote = True
                    in_authors_note = True
                elif not (in_authors_note or skip_paragraphs) or in_footnote:
                    while "\\*" in line:
                        line = line.replace("\\*", "[^{}-{}]".format(i, next_note))
                        next_note += 1
                    while "({})".format(next_note) in line:
                        line = line.replace("({})".format(next_note),
                            "[^{}-{}]".format(i, next_note))
                        next_note += 1
                    chapter.lines.append(line)
        chapters.append(chapter)

        if not chapter.title:
            print("ERROR: Didn't see a chapter title!")
            sys.exit(1)

        if book_number >= len(CHAPTER_ENDS) or i < CHAPTER_ENDS[book_number]:
            chapter_number += 1
        else:
            write_book(args.output_dir, book_number, chapters)

            book_number += 1
            chapter_number = 1
            chapters = []
