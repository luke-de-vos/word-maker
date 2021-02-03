# word-maker

**makeword.py** implements an n-gram language model to generate words that (most likely) don't exist.

Words are generated on a character by character basis. The likelihood of a character being generated is equal to the relative frequency with which that character followed the last n-1 generated characters in the training set. The first n-1 characters are generated in one chunk drawing from a separate collection of (n-1)-grams that only occur at the beginning of words. By default, n = 4.

The default training set is an English dictionary of ~450,000 terms. There are separate entries for each word's different possible prefixes and suffixes, such as run and running.


### USAGE:
  
`$python3 makeWord.py FLAG(S) ROOT`

Flags and root are optional. Flags and root will modify the functionality of makeWord.py.


### FLAGS:

- `-c`
	- print generation with green and highlights denoting particularly expected or unexpected generations respectively
	- see COLOR CODING section below for details
- `-i`
	- print the relative frequency and relative 'expectedness' for each character generated
	- see COLOR CODING section below for details
	- implements -v
- `-m`
	- wait for user to hit ENTER to generate next character
	- implements -v
- `-max NUM`	
	- set maximum length of generated word to NUM
- `-min NUM`	
	- set minimum length of generated word to NUM
- `-n NUM`
	- set n-gram length to NUM
	- longer n-grams tend to yield more convincing fake words but are more likely to generate real words
- `-t NUM`
	- wait NUM seconds to generate each character
	- implements -v
- `-v`
	- print in-progress generation every time a character is generated


### ROOT:

User can pass a string of length >=n-1 as the final command line argument to serve as the "root" of the generation. **makeWord.py** will build off of this root to generate a word.


### EXAMPLE EXECUTION

In this example, 'rad' is passed as the (optional) root.

	$python3 makeword.py -max 12 -v rad
	<Hit ENTER to generate word>

 	rad
	radi
	radic
 	radicr
 	radicro
 	radicrol
 	radicroli
 	radicrolis
 	radicrolis


### COLOR CODING:
If the -c flag is passed, characters may be highlighted green or red to denote 'expected' and 'unexpected' generations respectively. A generated character's expectedness is determined by how the probability of its generation compares to the average probability of all other possible genenerated characters given the last n-1 characters. The brightness of the highlight corresponds to the magnitude of its (un)expectedness.


For example, let n=4 and 'xyz' be the last n-1 characters of an in-progress generation. If, in the training set, 'a' follows those characters 90% of the time and 'b' follows them 10% of the time, the average relative frequency in that state is 50%. In this case, 'a' is 40% more likely than average. Thus, if 'a' were generated, it would be shaded a bright green.




