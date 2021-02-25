"""Full Text Search Engine"""
import os
import re
import string
import nltk
from IPython.display import clear_output
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer

def welcome():
    """Prints a welcome message."""

    print("Welcome to this full text search engine!")
    print("\nTo use this service, ensure files to analyse are contained in a single directory so we can grab them for you.\n")

def specified_directory():
    """Gets user directory."""

    global directory

    while True:
        directory = input(r"Please enter in your directory containing the files: ")

        if directory == "q":
            print("Quitting...")
            break

        try:
            os.chdir(directory)
        except:
            clear_output()
            print("Invalid file path!")
        else:
            print(f"\nWe are currently looking in {os.getcwd()}")
            break

def clean(text):
    """Cleans and normalises text."""

    reduce_whitespace = re.sub("\s+", " ", text)

    lower_text = reduce_whitespace.lower()

    remove_punctuation = re.sub("[^-9A-Za-z ]", " ", lower_text)

    tokenize = nltk.word_tokenize(remove_punctuation)

    stopwords = nltk.corpus.stopwords.words('english')
    remove_stopwords = [i for i in tokenize if i not in stopwords]

    lemmatizer = WordNetLemmatizer()
    lemmatize = [lemmatizer.lemmatize(i) for i in remove_stopwords]

    cleaned_text = " ".join(lemmatize)

    return cleaned_text

def unique_word_list():
    """Creates a unique word list from all documents within the current directory."""

    global file_list
    global unique_words
    global doc_word_list

    file_list = []
    unique_words = []
    doc_word_list = []

    for folders, subfolders, files in os.walk(os.getcwd()):
        for f in files:
            if f.split(".")[-1] == "txt":
                file_list.append(f)

                with open(f, "r") as file:
                    text = file.read()
                    cleaned_text = clean(text)

                    separated_words = cleaned_text.split(" ")
                    doc_word_list.append(separated_words)

                    for word in separated_words:
                        if word not in unique_words:
                            unique_words.append(word)

    if len(file_list) == 0:
        print("We couldn't find any text files, please check the directory!")
    else:
        return True

def inverted_index():
    """Creates an inverted index database."""

    global word_dictionary

    word_dictionary = {}

    for doc_id in range(len(file_list)):
        # For each unique word, count to see frequency in a document
        for u_word in unique_words:
            count = 0
            for word in doc_word_list[doc_id]:
                if u_word == word:
                    count += 1

            if doc_id == 0:
                word_dictionary[u_word] = [(doc_id + 1, count)]
            else:
                word_dictionary[u_word].append((doc_id + 1, count))

def index_search(terms):
    """User enters terms to search and is presented with results."""

    not_found = []
    term_list = terms.split(",")
    clean_terms = [clean(c.strip()) for c in term_list]

    for index, word in enumerate(clean_terms):
        if word in word_dictionary.keys():
            print(f"\n{term_list[index].strip()} was found in:")

            for doc_id, freq in word_dictionary[word]:
                if freq > 0:
                    print(f"{file_list[doc_id - 1]} with a frequency of {freq}")
        else:
            not_found.append(term_list[index].strip())

    if len(not_found) > 0:
        print("\nThe following words were not found:")
        for word in not_found:
            if word.strip() != "":
                print(word)

def replay():
    """Asks user if they would like to conduct another search."""

    global ask
    global change_directory

    while True:
        ask = input("\nWould you like to search again? (y/n/q) ")

        try:
            if ask.lower()[0] not in ("y", "n", "q"):
                print("Please enter in y/n/q!")

            elif ask.lower()[0] == "y":
                ask = True
                search_location = input("Would you like to change directory? (y/n)")

                if search_location.lower()[0] not in ("y", "n"):
                    print("Please enter in y/n!")

                elif search_location.lower()[0] == "y":
                    change_directory = True
                    break
                else:
                    change_directory = False
                    break
            else:
                ask = False
                break

        except:
            print("Please enter in y/n/q!")


searching = True

welcome()
while searching:
    while True:
        print("\nEnter 'q' to quit at any time.")
        directory = input("Please enter in your directory containing the files: ")

        if directory == "q":
            print("Quitting...")
            searching = False
            break

        try:
            os.chdir(directory)
        except:
            clear_output()
            print("Cannot find the file path specified!\nPlease try again!")
        else:
            clear_output()
            print(f"We are currently looking in {os.getcwd()}\n")
            print("Creating unique word list from your documents...")

            if unique_word_list():
                break

    if directory != "q":
        print("Creating inverted index database...")
        inverted_index()
#         Uncomment below to view inverted index database
#         print(word_dictionary)
        print("Now we're ready for your search!\n\n")

        while True:
            print("Enter 'q' to quit the search any time.")
            term = input("Provide terms you would like to serch, separated by a comma: ")

            if term == "q":
                print("\nQuitting search...")
                searching = False
                break
            elif len(term.strip()) == 0:
                clear_output()
                print("\nPlease specify at least one term!")
            else:
                clear_output()
                index_search(term)
                replay()

                if ask == True:
                    if change_directory:
                        break
                    else:
                        continue
                else:
                    print("\nThank you for using this full text search engine!")
                    searching = False
                    break
