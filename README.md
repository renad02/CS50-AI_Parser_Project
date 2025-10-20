# Parser Project (CS50 AI)

This project is part of **Harvard’s CS50 Introduction to Artificial Intelligence with Python**.  
It builds a **context-free grammar (CFG) parser** that analyzes the **syntax structure** of English sentences to determine their grammatical composition and extract **noun phrases (NPs)**.

---

## Overview

- **Goal:** Implement a simple **natural language parser** that breaks down a sentence into its syntactic components.  
- **Technique:** Uses **context-free grammar (CFG)** and the **NLTK ChartParser** to generate possible parse trees.  
- **Focus:** Extract and display **noun phrase chunks (NPs)** from the parse tree.

---

## Features

Reads sentences from text files  
Tokenizes and preprocesses words (lowercase, filters non-alphabetic tokens)  
Builds parse trees using NLTK’s **CFG** grammar  
Detects and prints all **noun phrase chunks**  
Handles parsing errors gracefully  

---

## Grammar Rules

The parser defines its own **Context-Free Grammar (CFG)** with two categories:

- **Terminals:**  
  Words that appear in the sentence (e.g., “the”, “man”, “car”, “walked”).  
- **Non-Terminals:**  
  Abstract grammatical components like `S`, `NP`, `VP`, `N`, `V`, etc.

Example rule set:
```python
S -> NP VP
NP -> D N | N | D Adj N | Adj N
VP -> V | V NP | V NP PP | V PP
PP -> P NP
D -> "the" | "a"
N -> "man" | "park" | "dog" | "telescope" | "city"
V -> "saw" | "walked"
P -> "in" | "with"
Adj -> "small" | "red"
```
---

## How It Works

- **Preprocessing**

  Converts all text to lowercase and removes non-alphabetic tokens using nltk.word_tokenize().

- **Parsing**

  Uses nltk.ChartParser to generate all valid parse trees based on the grammar.

- **Noun Phrase Extraction**

  Identifies all subtrees labeled “NP” that:

    Do not contain any other “NP” inside them (smallest chunks).

    Represent independent noun phrases like “the man” or “a telescope”.

---

## Key Learning Outcomes

- Understanding **Context-Free Grammar (CFG)**

- Building a syntactic parser using NLTK

- Working with parse trees and linguistic structures

- Extracting meaningful **noun phrase chunks**
