BOOK_PREFIX := prince-of-the-dark-kingdom-book-

EPUBS := $(BOOK_PREFIX)1.epub \
    $(BOOK_PREFIX)2.epub \
    $(BOOK_PREFIX)3.epub \
    $(BOOK_PREFIX)4.epub \
    $(BOOK_PREFIX)5.epub \
    $(BOOK_PREFIX)6.epub \
    $(BOOK_PREFIX)7.epub \

PANDOC_FLAGS := --toc --toc-depth=1 --chapters

all: $(EPUBS);
epub: $(EPUBS) ;

clean:
	rm -rf $(EPUBS)

.PHONY: all clean ;

$(BOOK_PREFIX)%.epub: src/book-%/title.txt src/book-%/cover.svg
	pandoc $(PANDOC_FLAGS) -o $@ $(subst src/book-$*/cover.svg,,$^) \
	    --epub-cover-image=src/book-$*/cover.svg

$(BOOK_PREFIX)1.epub:  $(sort $(wildcard src/book-1/chapter-*.md))
$(BOOK_PREFIX)2.epub:  $(sort $(wildcard src/book-2/chapter-*.md))
$(BOOK_PREFIX)3.epub:  $(sort $(wildcard src/book-3/chapter-*.md))
$(BOOK_PREFIX)4.epub:  $(sort $(wildcard src/book-4/chapter-*.md))
$(BOOK_PREFIX)5.epub:  $(sort $(wildcard src/book-5/chapter-*.md))
$(BOOK_PREFIX)6.epub:  $(sort $(wildcard src/book-6/chapter-*.md))
$(BOOK_PREFIX)7.epub:  $(sort $(wildcard src/book-7/chapter-*.md))
