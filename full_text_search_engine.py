"""Full Text Search Engine"""
import os
import re
import argparse
import string
import nltk
from IPython.display import clear_output
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer


class Document():
    """Holds key information about each text document."""

    def __init__(self, file_name, file_path, doc_id):
        self.file_path = file_path
        self.file_name = file_name
        self.doc_id = doc_id
        self.cleaned_text = ""

        with open(file_path) as f:
            self.text = f.read()

    def __str__(self):
        """String representation of the file name."""

        return str(self.file_name)

    def clean_text(self):
        """Cleans and normalises text."""

        self.cleaned_text = clean(self.text)


class Database():
    """In memory database used to hold text document objects."""

    def __init__(self):
        self.db = []
        self.total = len(self.db)

    def __iter__(self):
        """Converts object to an iterable"""
        return iter(self.db)

    def __str__(self):
        """String representation of the Database object."""

        file_names = []

        for i in self.db:
            file_names.append(str((i.doc_id, str(i))))
        return "\n".join(file_names)

    def add(self, document):
        """Adds a text document object to the database."""

        self.db.append(document)
        self.total += 1

    def remove(self, doc_id):
        """Removes a text document object from the database."""

        current_total = self.total

        for index, document in enumerate(self.db):
            if doc_id == document.doc_id:
                self.db.pop(index)
                self.total -= 1

        if current_total == self.total:
            print(f"Document id {doc_id} not found in document database!")


class Inverted_Index():
    """In memory database containing a unique word list and inverted index dictionary for text documents"""

    def __init__(self):
        self.unique_words = []
        self.dictionary = {}

    def __str__(self):
        """String representation of the inverted index dictionary"""
        dic = []
        for item in self.dictionary.items():
            dic.append(str(item))

        return "\n".join(dic)

    def unique_word_list(self, database):
        """Creates a unique word list for text documents"""

        for doc in database:
            separated_words = doc.cleaned_text.split(" ")

            for word in separated_words:
                if word not in self.unique_words:
                    self.unique_words.append(word)

    def inverted_index_db(self, database):
        """Creates an inverted index dictionary for text documents"""

        for doc in database:
            for u_word in self.unique_words:
                count = 0
                for word in doc.cleaned_text.split(" "):
                    if u_word == word:
                        count += 1

                if u_word in self.dictionary.keys():
                    self.dictionary[u_word].append((doc.doc_id, count))
                else:
                    self.dictionary[u_word] = [(doc.doc_id, count)]

    def index_search(self, term_list, database):
        """Search for inverted index values"""

        not_found = []
        clean_terms = [clean(c.strip()) for c in term_list]

        for index, word in enumerate(clean_terms):
            if word in self.dictionary.keys():
                print(f"\n{term_list[index].strip()} was found in:")

                for doc_id, freq in self.dictionary[word]:
                    if freq > 0:
                        for doc in database:
                            if doc_id == doc.doc_id:
                                print(f"{doc.file_name} with a frequency of {freq}")
            else:
                not_found.append(term_list[index].strip())

        if len(not_found) > 0:
            print("\nThe following words were not found:")
            for word in not_found:
                if word.strip() != "":
                    print(word)


def welcome():
    """Prints a welcome message."""

    print("Welcome to this full text search engine!")
    print("\nTo use this service, ensure files to analyse are contained in a single directory so we can grab them for you.\n")


def specify_directory():
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
            print("Invalid file path, please try again!")

        else:
            print(f"\nWe are currently looking in {os.getcwd()}...")
            break


def build_db(database, d_id=0):
    """Creates a text document database, default document id starting at 0."""

    for folders, subfolders, files in os.walk(os.getcwd()):
        for f in files:
            if f.split(".")[-1] == "txt":
                path = folders + "\\" + f
                document = Document(f, path, d_id)
                d_id += 1
                document.clean_text()
                database.add(document)
                print(f"{document.file_name} added")


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

    final_text = " ".join(lemmatize)

    return final_text


def replay():
    """Asks user if they would like to conduct another search in the same or different directory."""

    global search
    global directory_choice
    global indexing
    ask = True

    while ask:
        answer = input("\nWould you like to search again? (y/n/q) ")

        try:
            if answer.lower()[0] not in ("y", "n", "q"):
                print("Please enter in y/n/q!")

            elif answer.lower()[0] == "y":
                search_location = input("Would you like to change directory? (y/n)")

                if search_location.lower()[0] not in ("y", "n"):
                    print("Please enter in y/n!")

                elif search_location.lower()[0] == "y":
                    directory_choice = True
                    indexing = False
                    ask = False
                    return True

                else:
                    ask = False
                    return True

            else:
                ask = False
                search = False
                return False

        except:
            print("Please enter in y/n/q!")

search = True
indexing = False
current_directory = ""

parser = argparse.ArgumentParser()
parser.add_argument("-d", help="If user would like to specify a directory", action="store_true")
parser.add_argument("-v", help="Prints out the document database and inverted index contents", action="store_true")
parser.parse_args()
args = parser.parse_args()

if args.d:
    print("Choose your directory!\n")
    directory_choice = True
    database_creation = False
else:
    print("Working in the current directory!\n")
    database = Database()
    inverted_index = Inverted_Index()
    directory_choice = False
    database_creation = True

if args.v:
    print("Verbose mode!\n")


welcome()
while search:
    while directory_choice:
        specify_directory()

        if directory == "q":
            directory_choice = False
            search = False

        else:
            directory_choice = False
            database_creation = True

    while database_creation:
        if current_directory == os.getcwd():
            print("Database already created!\nSkipping to search!")
            database_creation = False
            indexing = True
            break

        else:
            database = Database()
            inverted_index = Inverted_Index()
            print("\nAttempting to create text document database...")
            build_db(database)

            if database.total == 0:
                clear_output()
                print("No text files were found, please check your directory!")
                directory_choice = True
                database_creation = False

            else:
                database_creation = False
                indexing = True
                inverted_index.unique_word_list(database)
                print("\nCreating inverted index dicitonary...")
                inverted_index.inverted_index_db(database)
                current_directory = os.getcwd()
                print("Now we're ready for your search!")

    while indexing:
        if args.v:
            print(f"The database of text documents currently holds:\n{database}\n")
            print(f"The underlying inverted index dictionary:\n{inverted_index}")

        print("\nEnter 'q' to quit the search any time.")
        term = input("Provide terms you would like to serch, separated by a comma: ")

        if term == "q":
            print("\nQuitting search...")
            indexing = False
            directory_choice = True

        elif len(term.strip()) == 0:
            clear_output()
            print("\nPlease specify at least one term!")

        else:
            clear_output()
            inverted_index.index_search(term.split(","), database)

            if replay():
                break

            else:
                print("\nThank you for using this full text search engine!")
                indexing = False
                break
                
