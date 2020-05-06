import sys
import glob
import re
import errno
from collections import defaultdict


def main():
    globalList = defaultdict(list)
    path = 'C:\\Users\\bodlan\\Desktop\\aclImdb\\test\\pos\\*.txt'
    files = glob.glob(path) # list of path names that matches pathname

    for name in files: # 'file' is a builtin type, 'name' is a less-ambiguous variable name.
        try:
            with open(name) as f:
                #print("name: ",name)
                #setting variable count to txt number.
                count=int(re.findall(r'\d+|$',name)[0])
                # sys.stdout.write(f.read())
                words =f.read().split(" ")
                for word in words:
                    #clear words in text
                    word=re.findall(r'\w+|$',word)[0]
                    if word in globalList:
                        globalList['{}'.format(word)].append(count)
                    else:
                        globalList['{}'.format(word)].append(count)
                count+=1
        except IOError as exc:
            if exc.errno != errno.EISDIR: # Do not fail if a directory is found, just ignore it.
                raise # Propagate other kinds of IOError.
    print("globalList starts:\n")
    w=0
    for i in globalList:
        print(i," : ",globalList[i],"\n")
        w+=1
    print("w: ",w)
    #count frequency of word
    for key,value in globalList.items():
        print(key,len([item for item in value if item]))



if __name__ == '__main__':
    main()