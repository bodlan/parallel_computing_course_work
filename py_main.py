"""
The program stores all words from directories in one dictionary.
Also realised parallel computing
"""

import time
import glob
import re
import threading
from collections import defaultdict
from multiprocessing import Process


THREAD_COUNT = 4
global_dictionary = defaultdict(list)


def process_directory(files, counter, thread_part):
    """
    Function processing given directory to find words in files
    Dictionary contain words of files in it
    :param files: path to your directories
    :param counter: used for parallel computing to track lower bound
    :param thread_part: used for parallel computing to track upper bound
    """
    start = time.time()
    # list of path names that matches pathname
    print("indent:", threading.get_ident())

    for name in files[slice(int(thread_part*counter), int(thread_part*(counter+1)))]:
        with open(name, encoding="utf-8") as file:
            # setting variable count to txt number.
            # print("name:",name, "with: ",threading.get_ident())
            words = file.read().split(" ")
            for word in words:
                # clear words in text
                word = re.findall(r'\w+|$', word)[0]
                global_dictionary['{}'.format(word)].append(name.split("\\", 5)[-1])

    end = time.time()-start
    print("time in func:", end, 'with indent:', threading.get_ident())


def print_list(words):
    """
    Function prints dictionary for each key and value
    :param words: dictionary to print
    """
    word_count, size = 0, 0
    for key, value in words.items():
        word_count += 1
        size += len([item for item in value if item])
        # print(key,":",value)
    print("words:", word_count, 'size:', size)


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
    thread_part = int((len(glob.glob(folder_path)))/THREAD_COUNT)
    files = glob.glob(folder_path)
    print("len:", len(glob.glob(folder_path)))
    print("thread_part:", thread_part)
    start_time = time.time()
    thread_list = []
    for i in range(THREAD_COUNT):
        process = Process(target=process_directory, args=(files, i, thread_part))
        process.start()
        thread_list.append(process)
    for i in thread_list:
        i.join()
    end_time = time.time()
    print("time:", end_time - start_time)
    print("globalList starts:\n")
    print_list(global_dictionary)

    # word_frequencies(globalList)
    # find combination of words in single file
    # list_appearance('', globalList)


if __name__ == '__main__':
    main()
