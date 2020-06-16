# word-maker

makeWord.py generates words with character n-grams and markov chains. By default, n is 4. N-grams are drawn from an English dictionary of ~450,000 terms. A lemma may appear many times with different prefixes and suffixes.

The chance for a given character to be generated is equal to the relative frequency of that char following the last n-1 characters. The first n-1 characters are generated in one chunk drawing from a separate collection of n-1grams that only occur at the beginning of words.

### USAGE:
  
`$python3 makeWord.py FLAG(S) ROOT`

Flags and root are optional. Flags and root will modify the functionality of makeWord.py.


### FLAGS:

- `-c`
	- print generation with red and green highlights denoting particularly unusual or common generations respectively.
	- see COLOR CODING section below for details
- `-i`
	- print the relative frequency and rel freq - average for the last character generated
	- use with `-v`
- `-max NUM`	
	- set maximum length of generated word to NUM
- `-min NUM`	
	- set minimum length of generated word to NUM
- `-n NUM`
	- set n-gram length to NUM
- `-s`
	- wait for user to hit ENTER to generate next character. 
	- use with `-v`
- `-v`
	- print in-progress generation every time a character is generated


### ROOT:

User can pass a word of length >=n-1 as the "root" of the generation. makeWord.py will build off of this root to generate a word.


### EXAMPLE EXECUTION

In this example, 'rad' is passed as a root.

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
Color coding for a given generated character is determined by how the probability of its generation compares to the average probability of all other possible genenerated characters in that state. If the generated character was more likely to appear than average, it is highlighted green. If it was less likely to appear than average, it is highlighted red. The brightness of the highlight corresponds to just how much more or less likely the character's generation was.


For example, let 'xyz' be an in-progress generation. If 'a' follows those characters 90% of the time and 'b' follows them 10% of the time, the average relative frequency in that state is 50%. 'a' is 40% more likely than average. Thus, if 'a' were generated, it would be shaded a bright green.




