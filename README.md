# Full Text Search Engine

Inverted index search for text documents.

## Table of Contents
* [Introduction](https://github.com/AoifeFlanagan/Full-Text-Search-Engine#Introduction)
* [Program](https://github.com/AoifeFlanagan/Full-Text-Search-Engine#Program)
* [Features](https://github.com/AoifeFlanagan/Full-Text-Search-Engine#Features)
* [Known Issues](https://github.com/AoifeFlanagan/Full-Text-Search-Engine#Known-Issues)
* [Modules](https://github.com/AoifeFlanagan/Full-Text-Search-Engine#Modules)
* [Recommended Interactive Development Environment (IDE)](https://github.com/AoifeFlanagan/Full-Text-Search-Engine#recommended-interactive-development-environment-ide)

## Introduction

A full text search engine allows for a user to search for a term, or set of terms. It is characterised by utilising an inverted index database to perform searches. 

An inverted index database is a mapping from content to document. This allows for an extremely fast search to be conducted as there is no need to iterate through each document for each individual search. 

## Program

This program will first ask the user to specify a directory containing the text files they would like to search. The format is as follows:

`C:\Users\Name\Desktop\Text Files`

If there are any subdirectories contained within the directory specified, they will also be searched. 

Upon a directory being chosen, the inverted index database is created by first scanning each and every text document and producing a list of unique words. The unique words are created by first cleaning the text inside each document via normalising whitespace, lower case sorting, removing punctuation, tokenisation, stop word removal and lemmatisation.

These words will be the basis for the mapping in the inverted index database. The unique words are mapped to a document identifier and the frequency they occur in said document. 

The user can then perform a search, using a comma to split up terms if searching multiple terms. The terms entered are then cleaned and looked within the database. If the cleaned terms are found within the database, results are then presented to the user.

## Features

- Search returns the term along with the name of the text document and the frequency of the term
- Inverted index stored as a dictionary allowing fast queries
- Status updates presented to the user
- Can research either within current directory or a new, user specified directory
- If no text files found, user will be asked to specify a different directory
- Error handling on choosing a directory
  - If a directory does not exist or has been entered incorrectly, the user will be notified
- Ignores terms that are just spaces or punctuation
- The user can enter q to quit when selecting a directory, searching a term or when asked to perform another search

## Known Issues
- Speed of queries could be improved via multithreading 
- Will only search text documents ending in `.txt`
- No way for user to view underlying database
  - Debug code available for interest

## Modules
- `os`
- `re`
- `string`
- `nltk`
- `IPython.display`
- `nltk.corpus`
- `nltk.tokenize`
- `nltk.stem`


## Recommended Interactive Development Environment (IDE)
### **Jupyter notebook**
This program was created and tested using a Jupyter notebook, I recommend running the code in this environment for optimal performance.

### **Version**
The notebook server was run on Python version 3.7.6
