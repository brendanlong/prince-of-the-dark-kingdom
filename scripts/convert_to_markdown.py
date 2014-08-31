#!/usr/bin/env python3
import argparse
import html2text
import itertools
import os
import re
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

CHAPTER_REGEX = re.compile("^(Epilogue)|^(\*\*)?Chapter [0-9]+[:-]? *([^*]*)(\*\*)?$")
FOOTNOTE_REGEX = re.compile("^([0-9]+)\\\. (.+)$")
PAGE_BREAK_REGEX = re.compile("^o+$|^~ *Page Break(er)?s? *~$", flags=re.IGNORECASE)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", "-i", required=True)
    parser.add_argument("--output-dir", "-o", required=True)
    args = parser.parse_args()

    book = 1
    chapter = 1
    for i in itertools.count(1):
        filename = os.path.join(args.input_dir, "chapter-{:03d}.html".format(i))
        if not os.path.isfile(filename):
            break

        print("Importing Book {} Chapter {} ({})".format(book, chapter, i))

        book_dir = os.path.join(args.output_dir, "book-{}".format(book))
        if not os.path.isdir(book_dir):
            os.makedirs(book_dir)

        title_file = os.path.join(book_dir, "title.txt")
        if not os.path.isfile(title_file):
            with open(title_file, "w") as f:
                f.write("% Prince of the Dark Kingdom: Book {}\n"
                    "% Mizuni-sama".format(book))

        with open(filename, "r") as f:
            story_text = f.read()

        story_text = story_text.replace("*", "\\*")
        story_text = html2text.html2text(story_text)

        saw_title = False
        results = []
        note = 1
        for line in story_text.splitlines():
            if not saw_title:
                match = CHAPTER_REGEX.search(line)
                if match is not None:
                    saw_title = True
                    if match.group(1) or match.group(3):
                        results.append("# {}".format(match.group(1) or match.group(3)))
                    else:
                        results.append("# Chapter {}".format(i))
            elif PAGE_BREAK_REGEX.match(line):
                results.append("---")
            else:
                match = FOOTNOTE_REGEX.search(line)
                if match is not None:
                    results.append("[^{}-{}]: {}".format(i, match.group(1), match.group(2)))
                else:
                    while "\\*" in line:
                        line = line.replace("\\*", "[^{}-{}]".format(i, note))
                        note += 1
                    results.append(line)
        if not saw_title:
            print("ERROR: Didn't see a chapter title!")
            break

        with open(os.path.join(book_dir, "chapter-{:02d}.md".format(chapter)), "w") as f:
            f.write("\n".join(results))

        if book < len(CHAPTER_ENDS) and i == CHAPTER_ENDS[book]:
            book += 1
            chapter = 1
        else:
            chapter += 1
