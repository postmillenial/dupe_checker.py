# dupe_checker.py

```
python3 dupe_checker.py .
```

The above command will check the current directory for duplicates based on filename, file size, and adler32 checksum (in that order). It stores it all in a dictionary which can probably be used for other fun stuff. Right now I just have the program piping out the duplicates in this format:

```
original:relative/path/to/first/file/found:duplicate:relative/path/to/current/dupe
```

It also pumps out some progress messages to stderr.

Uses python os dirents for speed. CRCs computer last and not used for lookups in case you're dealing with the particular situation that I am, in which your mom's hard drive is slowing down to 10 seconds per inode lookup in the worst case (and this worst case is affecting the majority of over a million files)
