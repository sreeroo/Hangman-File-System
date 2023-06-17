/*
  hangman_fs: Hangman Filesystem in Userspace
  This program can be distributed under the terms of the GNU GPLv2
*/
#define FUSE_USE_VERSION 31
#include <errno.h>
#include <fuse3/fuse.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

// Data about the files in our file system
char player[256] = "[default]";          // information on the current player
char guard1[] = "123";                   // some defined memory content
ulong player_size = 9;                   // size of the "player" file
char solution[128] = "WEINBERGSCHNECKE"; // the word being looked for
char guard2[] = "123";                   // some defined memory content
char status[128] = "WEINBERGSCHNECKE"; // the currently guessed part of the word
char guard3[] = "123";                 // some defined memory content
ulong solution_size = 16; // size of the "solution" (and "status") file
char guesses[32];         // the letters guessed so far
char guard4[] = "123";    // some defined memory content
ulong guesses_size = 0;   // size of the "guesses" file

int fs_getattr(const char *path, struct stat *stbuf, struct fuse_file_info *fi) {
  // Set defaults
  memset(stbuf, 0, sizeof(struct stat));
  stbuf->st_uid = getuid(); // the owner of the file/directory is the user who mounted the filesystem
  stbuf->st_gid = getgid(); // the group of the file/directory is the same as the group of the user who mounted the filesystem
  stbuf->st_atime =
      time(NULL); // the last access to the file/directory is right now
  stbuf->st_mtime =
      time(NULL); // the last modification to the file/directory is right now
  stbuf->st_mode = S_IFREG | 0664;
  stbuf->st_nlink = 1;
  // Set data for our files
  if (strcmp(path, "/") == 0) {
    stbuf->st_mode = S_IFDIR | 0755;
    stbuf->st_nlink = 2;
  } else if (strcmp(path + 1, "player") == 0) {

    // - your task -
    stbuf -> st_mode = S_IFREG | 0664;
    stbuf -> st_size = player_size;
    stbuf -> st_nlink = 1;
  }
  else if (strcmp( path + 1, "solution") == 0){
      stbuf -> st_mode = S_IFREG | 0664;
      stbuf -> st_size = solution_size;
      stbuf -> st_nlink = 1;
  }
  else if (strcmp( path + 1, "guesses") == 0){
      stbuf -> st_mode = S_IFREG | 0664;
      stbuf -> st_size = guesses_size;
      stbuf -> st_nlink = 1;
  }
  else if (strcmp( path + 1, "status") == 0){
      stbuf -> st_mode = S_IFREG | 0444;
      stbuf -> st_size = solution_size;
      stbuf -> st_nlink = 1;
  } else
    return -ENOENT;
  return 0;
}

int fs_readdir(const char *path, void *buf, fuse_fill_dir_t filler, off_t offset, struct fuse_file_info *fi, enum fuse_readdir_flags flags) {
  // Only root directory of our file system has any content
  if (strcmp(path, "/") != 0)
    return -ENOENT;
  // List of files in our root directoy
  filler(buf, ".", NULL, 0, 0);
  filler(buf, "..", NULL, 0, 0);
  filler(buf, "player", NULL, 0, 0);

  // - your task -
  filler(buf, "solution", NULL, 0, 0);
  filler(buf, "status", NULL, 0, 0);
  filler(buf, "guesses", NULL, 0, 0);

  return 0;
}


int fs_open(const char *path, struct fuse_file_info *fi) {
  printf("Trying to open [%s] with flags [%d]\n", path, fi->flags);
  // Check whether opening in the requested mode is allowed
  if (strcmp(path + 1, "status") == 0)
    if ((fi->flags & O_ACCMODE) != O_RDONLY)
      return -EACCES;
  // Truncate (writable) file if flag is set to do so
  if ((fi->flags & O_TRUNC) == O_TRUNC) {

    // - your task -

  }
  // Allow open for known files
  if ((strcmp(path + 1, "player") == 0)
     || (strcmp(path + 1, "solution") == 0)
     || (strcmp(path + 1, "status") == 0)
     || (strcmp(path + 1, "guesses") == 0)) {
    return 0;
  }
  return -ENOENT;
}


int fs_read(const char *path, char *buf, size_t size, off_t offset, struct fuse_file_info *fi) {
  printf("Trying to read [%s], offset %lu, size %lu\n", path, offset, size);

  // - your task -
  return 0;

}


int fs_write(const char *path, const char *buf, size_t size, off_t offset, struct fuse_file_info *info) {
  printf("Trying to write [%s], offset %lu, size %lu\n", path, offset, size);
  size_t maxlen;
  char *file_data;
  ulong *file_size;
  // Get size of file depending on requested filename
  if (strcmp(path + 1, "player") == 0) {
    maxlen = sizeof(player);
    file_data = player;
    file_size = &player_size;
  } else if (strcmp(path + 1, "solution") == 0) {
    maxlen = sizeof(solution);
    file_data = solution;
    file_size = &solution_size;
  } else if (strcmp(path + 1, "guesses") == 0) {
    maxlen = sizeof(guesses);
    file_data = guesses;
    file_size = &guesses_size;
  } else
    return -ENOTSUP;
  // Write requested data within limits of allocated memory
  if (offset < maxlen) {
    if (offset + size > maxlen)
      size = maxlen - offset;
    memcpy(file_data + offset, buf, size);
    if (offset + size > *file_size)
      *file_size = offset + size;
  } else
    size = 0;
  return size;
}


int fs_truncate(const char *path, off_t size, struct fuse_file_info *fi)
{
  printf("Trying to truncate [%s] to size %lu\n", path, size);

  // - your task -
  // Note: when increasing the file size, the file gets extended with null bytes

  return -ENOTSUP;
}


const struct fuse_operations fs_operations = {
  .getattr = fs_getattr, .readdir = fs_readdir,
  //    .open           = fs_open,
  //    .read           = fs_read,
  //    .write          = fs_write,
  //    .truncate       = fs_truncate,
};

int main(int argc, char *argv[]) {
  int ret;
  struct fuse_args args = FUSE_ARGS_INIT(argc, argv);
  ret = fuse_main(args.argc, args.argv, &fs_operations, NULL);
  return ret;
}
