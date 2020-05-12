"""
The program stores all words from directories in one dictionary.
Also realised parallel computing
"""

import time
import glob
import re
import threading
import errno
import concurrent.futures
from collections import defaultdict


THREAD_COUNT = 2
globalList = defaultdict(list)


def process_directory(folder_path, counter, thread_part):
    """
    Function processing given directory to find words in files
    Dictionary contain words of files in it
    :param folder_path: path to your directories
    :param counter: used for parallel computing to track lower bound
    :param thread_part: used for parallel computing to track upper bound
    """
    lock = threading.Lock()
    tmp_dict = defaultdict(list)
    # list of path names that matches pathname
    files = glob.glob(folder_path)
    for name in files[slice(int(thread_part*counter), int(thread_part*(counter+1)))]:
        try:
            with open(name) as file:
                # print("name: ",name)
                # setting variable count to txt number.
                words = file.read().split(" ")
                for word in words:
                    # clear words in text
                    word = re.findall(r'\w+|$', word)[0]
                    if word in tmp_dict:
                        tmp_dict['{}'.format(word)].append(name.split("\\", 5)[-1])
                    else:
                        tmp_dict['{}'.format(word)].append(name.split("\\", 5)[-1])
        except IOError as exc:
            # Do not fail if a directory is found, just ignore it.
            if exc.errno != errno.EISDIR:
                # Propagate other kinds of IOError.
                raise
        # locking other threads from modifying dictionary
        # waits till thread finishes processing dictionary
        with lock:
            for key in tmp_dict.keys():
                if key in globalList.keys():
                    for i in tmp_dict.get(key):
                        if i not in globalList.get(key):
                            globalList[key].append(i)
                else:
                    for i in tmp_dict.get(key):
                        globalList[key].append(i)


def print_list(words):
    """
    Function prints dictionary for each key and value
    :param words: dictionary to print
    """
    word_count = 0
    for i in words:
        print(i, " : ", words[i], "\n")
        word_count += 1
    print("words:", word_count)


def common(lst1, lst2):
    """
    :param lst1: first list
    :param lst2: second list
    :return: common value between first and second list
    """
    return list(set(lst1) & set(lst2))


def list_appearance(string, dictionary):
    """
    Function returns appearance of string in dictionary
    :param string: string to find in dictionary
    :param dictionary: dictionary where to find
    :return: dictionary with appearance
    """
    string_to_find = string.split(" ")
    print("s:", string_to_find)
    appearance = []
    for i in string_to_find:
        if i in dictionary:
            if not appearance:
                appearance = dictionary.get(i)
            else:
                appearance = common(appearance, dictionary.get(i))
        else:
            print("No such word in dict as:", i)
    if not appearance:
        print("No such combinations of words in one file!")
    else:
        print("Combination of words appears at:", appearance)
    return appearance


def word_frequencies(dictionary):
    """
    Function prints frequencies of words in dictionary
    :param dictionary: dictionary to track frequency
    """
    for key, value in dictionary.items():
        print(key, len([item for item in value if item]))


def main():
    """
    Main function of program which is processing dictionary
    Parallel computing in program starts here
    """
    folder_path = 'C:\\Users\\bodlan\\Desktop\\aclImdb\\**\\**\\*.txt'
    thread_part = int(len(glob.glob(folder_path))/THREAD_COUNT)
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=THREAD_COUNT) as executor:
        for counter in range(THREAD_COUNT):
            executor.submit(process_directory, folder_path, counter, thread_part)
    end_time = time.time()
    print("globalList starts:\n")
    print_list(globalList)
    print("time:", end_time-start_time)
    # word_frequencies(globalList)
    # find combination of words in single file
    # list_appearance('', globalList)


if __name__ == '__main__':
    main()
