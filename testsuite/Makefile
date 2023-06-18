COMPILER = gcc
FILESYSTEM_FILES = ../hangman_fs1.c

build: $(FILESYSTEM_FILES)
	$(COMPILER) $(FILESYSTEM_FILES) -shared -Wall -o hangman_fs.so  `pkg-config fuse3 --cflags --libs` -IC -fPIC -Wl,-soname,hangman_fs
clean:
	rm hangman_fs.so
