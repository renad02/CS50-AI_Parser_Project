import nltk                                                                     # for tokenizing and parsing the sentence
import sys                                                                      # to read from command-line arguments
import re                                                                       # for regular expressions (used in text cleaning)
from nltk import Tree                                                           # Used to represent grammatical parse trees.

nltk.download("punkt", quiet=True)                                              #  Download tokenizer data if not already available
nltk.download('punkt_tab', quiet=True)


# These are the vocabulary rules — the actual words. Words used in parsing
TERMINALS = """                                                                 
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"      
Adv -> "down" | "here" | "never"                                                
Conj -> "and" | "until"                                                         
Det -> "a" | "an" | "his" | "my" | "the"                                        
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"      
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"                                
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"           
V -> "smiled" | "tell" | "were"
"""

"""
Adj -> generates adjectives
Adv -> generates adverbs
Conj -> generates conjunctions
Det ->  generates determiners
N ->  generates nouns
P -> generates prepositions
V ->  generates verbs.
"""

# NONTERMINALS: grammar rules that describe how parts of speech combine to form valid sentences.
NONTERMINALS = """                                                              
S -> NP VP | S Conj S
NP -> N | Det N | Det AP N | P NP | NP P NP | AP N | Det NP
AP -> Adj | Adj AP
VP -> V | V NP | V NP PP | V PP | Adv VP | VP Adv
PP -> P NP                                                            
"""

"""
S -> NP VP → A sentence (S) consists of a noun phrase (NP) followed by a verb phrase (VP).
Example: “Holmes smiled.”
NP -> Det N → A noun phrase can be a determiner (like the) + noun (like door).
Example: “the door.”
VP -> V NP → A verb phrase can be a verb followed by a noun phrase.
Example: “had a smile.”
AP -> Adj | Adj AP → An adjective phrase can be one or more adjectives chained together.
Example: “dreadful little.”
"""


#This combines both rule sets and builds a chart parser — an efficient CFG parser from NLTK.
grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:                                                      # If you run the program with a filename (like python parser.py sentence.txt), it reads from that file.
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:                                                                       # Otherwise, it asks you to type a sentence directly.
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)                                                           # Before parsing, it cleans and tokenizes the input text.

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))                                           # This line tells the parser to generate all valid parse trees that fit the grammar.
    except ValueError as e:
        print(e)
        return
    if not trees:                                                               # If there are no valid parses
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:                                                          # Otherwise, for each valid tree:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    tokens = nltk.word_tokenize(sentence.lower())                               # Converts all text to lowercase and tokenizes the sentence into individual words (nltk.word_tokenize).
    words = [word for word in tokens if re.search("[a-zA-Z]", word)]            # Removes anything that doesn’t contain at least one alphabetic letter (e.g., punctuation or numbers).
    return words              


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    chunks = []

    for subtree in tree.subtrees(filter=lambda t: t.label() == "NP"):           # Iterates over all subtrees in the parse tree that are labeled "NP".
        has_inner_np = any(                                                     # Checks if this NP contains another NP inside it.
            child.label() == "NP" for child in subtree.subtrees(lambda t: t != subtree)
        )
        if not has_inner_np:                                                    # If not — it’s a noun phrase chunk (the smallest NP).
            chunks.append(subtree)                                              # Adds it to chunks.

    return chunks


if __name__ == "__main__":
    main()
