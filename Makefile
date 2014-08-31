BOOK_PREFIX := prince-of-the-dark-kingdom-book-

EPUBS := $(BOOK_PREFIX)1.epub \
    $(BOOK_PREFIX)2.epub \
    $(BOOK_PREFIX)3.epub \
    $(BOOK_PREFIX)4.epub \
    $(BOOK_PREFIX)5.epub \
    $(BOOK_PREFIX)6.epub \
    $(BOOK_PREFIX)7.epub \

HTML := $(subst .md,.html,$(wildcard src/book-*/chapter-*.md))

MOBIS := $(subst .epub,.mobi,$(EPUBS))

KINDLEGEN_FLAGS := -c2
PANDOC_FLAGS := --toc --toc-depth=1 --chapters --epub-stylesheet=src/style.css \
    --epub-embed-font=src/fonts/lumos/lumos.ttf

all: $(EPUBS) $(MOBIS) ;
epub: $(EPUBS) ;
html: $(HTML) ;
mobi: $(MOBIS) ;

clean:
	rm -rf $(EPUBS) $(HTML) $(MOBIS)

.PHONY: all clean ;

$(BOOK_PREFIX)%.epub: src/book-%/title.txt src/book-%/cover.svg src/style.css
	pandoc $(PANDOC_FLAGS) -o $@ $(subst src/book-$*/cover.svg src/style.css,,$^) \
	    --epub-cover-image=src/book-$*/cover.svg

%.html: %.md src/style.css
	pandoc $(PANDOC_FLAGS) -s -t html5 -o $@ $(subst src/style.css,,$^)

%.mobi: %.epub
	kindlegen $(KINDLEGEN_FLAGS) -o $@ $^ || true

$(BOOK_PREFIX)1.epub:  $(sort $(wildcard src/book-1/chapter-*.md))
$(BOOK_PREFIX)2.epub:  $(sort $(wildcard src/book-2/chapter-*.md))
$(BOOK_PREFIX)3.epub:  $(sort $(wildcard src/book-3/chapter-*.md))
$(BOOK_PREFIX)4.epub:  $(sort $(wildcard src/book-4/chapter-*.md))
$(BOOK_PREFIX)5.epub:  $(sort $(wildcard src/book-5/chapter-*.md))
$(BOOK_PREFIX)6.epub:  $(sort $(wildcard src/book-6/chapter-*.md))
$(BOOK_PREFIX)7.epub:  $(sort $(wildcard src/book-7/chapter-*.md))
