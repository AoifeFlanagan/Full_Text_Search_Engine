import unittest
import os
import classes_funcs 

os.chdir(r"test_documents")

class Full_Text_Search_Test(unittest.TestCase):
    
    def test_clean_text(self):
        """Checks if text is cleaned and normalised correctly"""
        
        print("Verification of text normalisation...")
        text = "  Clean * 123:this  text! Stars /earth/ water should would she he I plurals words^ @test    "
        result = classes_funcs.clean(text)
        self.assertEqual(result, "clean text star earth water would plural word test")
        
        print("\n[+] Text cleaned successfully!\n")
    
    def test_document_database(self):
        """Checks text document attributes and subsequent addition to the database"""
        
        print("Verifying document attributes are added correctly to the database...")
        directory = os.getcwd()
        path = directory + "\\" + "testme.txt"    
        test_doc = classes_funcs.Document("testme.txt", path, 1)
        
        database = classes_funcs.Database()
        classes_funcs.build_db(database, 1)
        result = (database.db[0].file_name, database.db[0].file_path, database.db[0].doc_id, database.db[0].text)
        
        self.assertEqual(result, (test_doc.file_name, test_doc.file_path, test_doc.doc_id, test_doc.text))
        print("\n[+] Document attributes are correct!\n")
        
    def test_unique_word_list(self):
        """Checks if unique word list is generated correctly"""
        
        print("Verifying database generation...")
        unique_test = ['wrong', 'point', 'avoid', 'fruit', 'learn'] 
        unique_test.extend(['life', 'passage', 'however', 'besides', 'invited', 'comfort', 'elderly'])
        print(type(unique_test))
        directory = os.getcwd() 
        database = classes_funcs.Database()
        classes_funcs.build_db(database)
        inverted_index = classes_funcs.Inverted_Index()
        print("Testing unique word list generation...")
        inverted_index.unique_word_list(database)
        print(f"Unique word list contents:\n{inverted_index.unique_words}")
        print(f"Length of unique word list: {len(inverted_index.unique_words)}\n")
        
        result = (inverted_index.unique_words, len(inverted_index.unique_words))
        self.assertEqual(result, (unique_test, len(unique_test)))
        print("[+] Unique word list created successfully!\n")
        
    def test_dictionary(self):
        """Checks if inverted index dictionary is generated correctly"""
        
        test_dictionary = {'wrong': [(0, 1)], 'point': [(0, 1)], 'avoid': [(0, 2)], 'fruit': [(0, 2)], 'learn': [(0, 2)]}
        test_dictionary.update({'life': [(0, 1)], 'passage': [(0, 1)], 'however': [(0, 1)], 'besides': [(0, 1)], 'invited': [(0, 1)]})
        test_dictionary.update({'comfort': [(0, 1)], 'elderly': [(0, 1)]})
        database = classes_funcs.Database()
        inverted_index = classes_funcs.Inverted_Index()
        print("Adding the following text files for testing the inverted index dictionary...")
        classes_funcs.build_db(database)
        inverted_index.unique_word_list(database)
        inverted_index.inverted_index_db(database)
        print(f"The inverted index dictionary is: {inverted_index.dictionary}")
        print(f"The length of the dictionary is: {len(inverted_index.dictionary)}")
        
        result = (inverted_index.dictionary, len(inverted_index.dictionary))
        self.assertEqual(result, (test_dictionary, len(test_dictionary)))
        
        print("\n[+] Inverted index dictionary created successfully!\n")
    
if __name__ == "__main__":
    unittest.main()