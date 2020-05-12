import sys
import glob
import re
import threading
import errno
from collections import defaultdict
import concurrent.futures


Thread_count=10

def processDirectory(path,counter,thread_part):
    List=defaultdict(list)
    files = glob.glob(path)# list of path names that matches pathname
    sliced=slice(int(thread_part*counter),int(thread_part*(counter+1)))
    for name in files[sliced]:  # 'file' is a builtin type, 'name' is a less-ambiguous variable name.
        try:
            with open(name) as f:
                # print("name: ",name)
                # setting variable count to txt number.
                count = int(re.findall(r'\d+|$', name)[0])
                # sys.stdout.write(f.read())
                words = f.read().split(" ")
                for word in words:
                    # clear words in text
                    word = re.findall(r'\w+|$', word)[0]
                    if word in List:
                        List['{}'.format(word)].append(count)
                    else:
                        List['{}'.format(word)].append(count)
                count += 1
        except IOError as exc:
            if exc.errno != errno.EISDIR:  # Do not fail if a directory is found, just ignore it.
                raise  # Propagate other kinds of IOError.
    return List

def printList(list):
    w=0
    for i in list:
        print(i," : ",list[i],"\n")
        w+=1
    print("w:",w)
def common(lst1,lst2):
    return list(set(lst1)&set(lst2))
def listAppearance(string,list):
    s = string.split(" ")
    print("s:", s)
    appearance = []
    for i in s:
        if i in list:
            if not appearance:
                appearance = list.get(i)
            else:
                appearance = common(appearance, list.get(i))
        else:
            print("No such word in dict as:", i)
    if not appearance:
        print("No such combinations of words in one file!")
    else:
        print("Combination of words appears at:", appearance)
    return appearance
def wordFrequency(list):
    for key, value in list.items():
        print(key, len([item for item in value if item]))
def main():
    lock=threading.Lock()
    globalList=defaultdict(list)
    tmp_dict=defaultdict(list)
    pathList=['C:\\Users\\bodlan\\Desktop\\aclImdb\\test\\pos\\*.txt',
              'C:\\Users\\bodlan\\Desktop\\aclImdb\\test\\neg\\*.txt',
              'C:\\Users\\bodlan\\Desktop\\aclImdb\\train\\pos\\*.txt',
              'C:\\Users\\bodlan\\Desktop\\aclImdb\\train\\neg\\*.txt',
              'C:\\Users\\bodlan\\Desktop\\aclImdb\\train\\unsup\\*.txt']
    thread_part=int(len(glob.glob(pathList[0]))/Thread_count)
    with concurrent.futures.ThreadPoolExecutor(max_workers=Thread_count) as executor:
        tmp={executor.submit(processDirectory,pathList[0],counter,thread_part): counter for counter in range(Thread_count)}
        for f in concurrent.futures.as_completed(tmp):
            with lock:
                print("locked!")
            tmp_dict=f.result()
            for key, values in tmp_dict.items():
                if key in globalList.keys():
                    for i in tmp_dict.get(key):
                        if i not in globalList.get(key):
                            globalList[key].append(i)
                else:
                    for i in tmp_dict.get(key):
                        globalList[key].append(i)
            print("unlocked")


    print("globalList starts:\n")
    printList(globalList)
    #wordFrequency(globalList)
    #find combination of words in single file
    # listAppearance('',globalList)

if __name__ == '__main__':
    main()