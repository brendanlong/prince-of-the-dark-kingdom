## About

This project is an attempt to create ebooks out of Mizuni-sama's Harry Potter Fanfiction, [Prince of the Dark Kingdom](https://www.fanfiction.net/s/3766574/1/Prince-of-the-Dark-Kingdom).

Currently there are scripts for scraping the original story in HTML form and converting it to Markdown, and a Makefile which uses Pandoc to create an EPUB for each book, then Kindlegen to create the MOBI file.

If you want a PDF version, I recommend [the With Pins and Needles version](http://www.withpinsandneedles.com/?p=408) is much nicer than this one will ever be.

## Requirements

To build this project, you will need:

  * [git](http://git-scm.com/)
  * [Make](http://www.gnu.org/software/make/)
  * [Pandoc](http://johnmacfarlane.net/pandoc/)
  * [KindleGen](http://www.amazon.com/gp/feature.html?docId=1000765211) (optional)

You will need to download KindleGen yourself, and add it to your PATH. The rest can be installed

### Fedora 20

    sudo yum install git make pandoc
