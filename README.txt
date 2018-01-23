usage: midiconv.py [-h] [-s SHIFT] [-a APPEND] [-f] file [file ...]

Tool to change pitch of midi files

positional arguments:
  file                  list of files to convert - wildcards allowed

optional arguments:
  -h, --help            show this help message and exit
  -s SHIFT, --shift SHIFT
                        pitch shift to apply, e.g. -1 to lower 1/2 tone
  -a APPEND, --append APPEND
                        string to append to the filenames
  -f, --force           allow in-place conversion (same filename)