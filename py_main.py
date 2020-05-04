import sys
import glob
import errno

globalList=[]
def main():
    path = 'C:\\Users\\bodlan\\Desktop\\aclImdb\\test\\pos\\*.txt'
    files = glob.glob(path) # list of path names that matches pathname
    count=0
    for name in files: # 'file' is a builtin type, 'name' is a less-ambiguous variable name.
        try:
            with open(name) as f: # No need to specify 'r': this is the default.
                # sys.stdout.write(f.read())
                string =f.read().split(" ")
                print(string)
                count+=1
        except IOError as exc:
            if exc.errno != errno.EISDIR: # Do not fail if a directory is found, just ignore it.
                raise # Propagate other kinds of IOError.
    print("count:",count)


if __name__ == '__main__':
    main()