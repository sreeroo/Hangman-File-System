COMPILER = gcc
FILESYSTEM_FILES = hangman_fs1.c

build: $(FILESYSTEM_FILES)
	$(COMPILER) $(FILESYSTEM_FILES) -Wall -o hangman_fs `pkg-config fuse3 --cflags --libs`
	echo "Mount with ./hangman_fs -f <mountdir>"
clean:
	rm hangman_fs
