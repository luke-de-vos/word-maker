# word-maker

Generates words with 4-grams and markov chains.
Gram length can be adjusted by modifying variable 'gramLen'.
Chance for initial gram to be selected is based on the relative frequency of that initial gram.
For gram length n and >=n already-generated characters, the chance for given character to be generated is equal to the relative frequency of that char following the last n-1 characters.

To generate word:
  $python3 makeWord.py
  
To generate word beginning with n or more specific characters:
  $python3 makeWord.py exampleCharacters
 
