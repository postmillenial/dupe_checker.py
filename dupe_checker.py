import zlib, os, sys


class Mock(object):
    def __init__(self):
        self.cache = {}

    def write(self, data):
        for k,v in data.items():
            self.cache[k] = v
dup=0

def is_dupe(input_file):
    global dup
    if input_file.name not in file_records:
        file_records[input_file.name] = { "checksums":{
          (input_file.stat().st_size, compute_checksum(input_file)): 
              {"instances": [input_file.path]}
          }
        }
        return

    else: 
        for checksum in file_records[input_file.name]["checksums"]:
            size = checksum[0]
            hash = checksum[1]

            if size == input_file.stat().st_size and hash == compute_checksum(input_file):
                dup += 1
                file_records[input_file.name]["checksums"][checksum]["instances"].append(compute_checksum(input_file)) 
                print("original:{}:duplicate:{}".format(
                      file_records[input_file.name]["checksums"][checksum]['instances'][0],input_file.path))
                return
        # if we didn't find it, add a new size-checksum tuple:
        crc = compute_checksum(input_file)
        file_records[input_file.name]["checksums"][(input_file.stat().st_size, crc)] = {"instances": [input_file.path]}
      
count = 0
checksums = {}
CHECKSUM_STRATEGY=zlib.adler32
STORAGE_STRATEGY=is_dupe
file_records = {}

""" e.g.
file_records= 
{
  "b.jpg": {
    "checksums":{
      (4.20kB,"777GG"): {
          "instances":["/x/k/c/b.jpg]
      }
    }
  },
  "c.jpg": {
    "checksums":{
      (3kB, "0AB12"): {
        "instances":[
          "/a/b/c.jpg",
          "/a/b/c/ext/c.jpg"
        ],
      },
      (3kB, "JKL0L"): {
        "instances": ["/a/other/c.jpg"]
      }
    }
  }
}

"""


def usage():
    print("usage:", sys.argv[0], sys.argv[1], sys.argv[2:] )

def compute_checksum(file, check_using_strategy=CHECKSUM_STRATEGY):
    if file.path in checksums:
        return checksums[file.path]
    else:
        with open(file.path, 'rb') as fdesc:
            return check_using_strategy(fdesc.read())

def store_data(dirent, store):
    # it's awfully convenient that store is both a noun and a verb
    if callable(store):
        store(dirent)
        return
    else:
        entry = {}
        entry[dirent.path] = (dirent.stat().st_size, compute_checksum(hash))
        store.write(entry)

def sumtree(path):
    global count
    global dup
    for entry in os.scandir(path):
        count += 1
        print("{:02d} files scanned; {:02d} dupes found".format(count, dup), file=sys.stderr, end="\r")
        if entry.is_file():
            store_data(entry, STORAGE_STRATEGY)
        elif entry.is_dir():
            sumtree(entry.path)
            pass
        else:
            print("what filetype is this??? fkn yikes")
            print(entry)


def main():
    if len(sys.argv) < 2:
        usage()
        sys.exit()

    # The arg better be a directory
    root = sys.argv[1]
    sumtree(root)

    # print(file_records)


if __name__=="__main__":
    main() 

