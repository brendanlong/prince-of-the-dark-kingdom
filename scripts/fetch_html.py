#!/usr/bin/env python3
import argparse
from bs4 import BeautifulSoup
import os
import urllib.request
import sys

def get_chapter(i, out_dir):
    print("Downloading Chapter {}".format(i))
    url = "https://www.fanfiction.net/s/3766574/{}/".format(i)
    page_content = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(page_content)

    story_text = soup.find(id="storytext")
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    with open(os.path.join(out_dir, "chapter-{:03d}.html".format(i)), "w") as f:
        f.write(str(story_text))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--page", "-p", type=int)
    parser.add_argument("--output-dir", "-o", required=True)
    args = parser.parse_args()
    if args.page is not None:
        get_chapter(args.page, args.output_dir)
    else:
       for i in range(1, 148):
            get_chapter(i, args.output_dir)
