import nltk
# nltk.download('wordnet')
from nltk.corpus import wordnet
import random
import os
import pandas as pd

# method to swap a word with another that means the same thing
def swap_words(sentence, word1, word2):
    # split the sentence into a list of words
    words = sentence.split()
    # loop through the list of words
    for i in range(len(words)):
        # if the word matches word1, replace it with word2
        if words[i] == word1:
            words[i] = word2
    # join the list of words back into a sentence
    return ' '.join(words)

# method to find synonyms of a word
def find_synonyms(word):
    # create a list of synonyms
    synonyms = []
    # loop through the list of words
    for syn in wordnet.synsets(word):
        # loop through the list of lemmas
        for l in syn.lemmas():
            # add the synonym to the list
            synonyms.append(l.name())
    # return the list of synonyms
    return synonyms

# Method to switch out random words with synonyms
def synonym_swap(sentence):
    
    # function to test if something is a noun/verb
    is_noun = lambda pos: pos[:2] == 'NN'
    is_verb = lambda pos: pos[:2] == 'VB'
    tokenized = nltk.word_tokenize(sentence)
    nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)] 
    verbs = [word for (word, pos) in nltk.pos_tag(tokenized) if is_verb(pos)]
    synonyms = []
    if len(nouns) > 0:
        noun = nouns[random.randint(0, len(nouns) - 1)]
        noun_synonyms = find_synonyms(noun)
        if len(noun_synonyms) > 0:
            synonyms.append((noun, noun_synonyms[random.randint(0, len(noun_synonyms) - 1)]))
    if len(verbs) > 0:
        verb = verbs[random.randint(0, len(verbs) - 1)]
        verb_synonyms = find_synonyms(verb)  
        if len(verb_synonyms) > 0:
            synonyms.append((verb, verb_synonyms[random.randint(0, len(verb_synonyms) - 1)]))      
    if len(synonyms) == 0:
        return sentence

    # loop through the list of synonyms and replace the existing word in sentance
    for synonym in synonyms:
        sentence = swap_words(sentence, synonym[0], synonym[1])

    return sentence

# Create n augmented sentences
def add_synonym_swap(sentence, n):
    augmented_sentences = []
    for _ in range(n):
        augmented_sentences.append(synonym_swap(sentence))
    return augmented_sentences

# method to add row to dataframe
def add_row(df, row):
    df.loc[len(df)] = row
    return df

# Method to open and edit every sentence in a file
def augment_file(file_name, new_file_name, question, answer,n):
    df = pd.read_csv(file_name)
    df = df[[question, answer]]
    df = add_row(df, [question, answer])
    # print(df.tail(5))
    for ind, row in enumerate(df.iterrows()):
        q = row[1][question]
        if q.strip() == 'Question':
            continue
        a = row[1][answer]
        for augmented_question in add_synonym_swap(q, n):
            add_row(df, [augmented_question, a])
    df.to_csv(f'{new_file_name}.csv', index=False)

# Method to find all txt files in a directory
def find_csv_files(directory):
    # create a list of txt files
    csv_files = []
    # loop through the list of files in the directory
    for file in os.listdir(directory):
        # if the file is a txt file, add it to the list
        if file.endswith('.csv'):
            csv_files.append(file)
    # return the list of txt files
    return csv_files

if __name__ == '__main__':

    for f in find_csv_files('.'):
        augment_file(f, 'augmented_' + f,' Question',' Answer', 5)

