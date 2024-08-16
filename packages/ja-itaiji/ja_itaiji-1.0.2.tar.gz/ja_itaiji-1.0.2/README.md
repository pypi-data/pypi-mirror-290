# ja-itaiji

ja-itaiji is a Python package for handling Japanese 異体字 (itaiji), which are variant forms of kanji characters. This package allows you to find equivalent characters, check if two kanji characters or words are equivalent, and generate a list of similar words by replacing kanji with their itaiji.

## Features

* Get Itaiji Family: Retrieve a list of kanji characters that are equivalent to a given kanji.
* Check Kanji Equivalence: Determine whether two kanji characters are equivalent itaiji.
* Check Word Equivalence: Check if two words are equivalent within itaiji.
* Generate Similar Words: Generate a list of words by replacing each kanji with its equivalent itaiji.

## Installation

To install the package, use pip:
```shell
pip install ja-itaiji
```

## Usage
### Importing the Package
```python
from ja_itaiji import Itaiji
```

### Get Itaiji Family
Retrieve a list of kanji characters that are equivalent to a given kanji.
```python
family = Itaiji.get_family('漢')
print(family)  # Output: ['漢', '㵄', '漢', '汉']
```

### Check Kanji Equivalence
Determine whether two kanji characters are equivalent itaiji.
```python
is_equivalent = Itaiji.is_family('漢', '㵄')
print(is_equivalent)  # Output: True
```

### Check Word Equivalence
Check if two words are equivalent within itaiji.
```python
is_similar = Itaiji.is_similar('漢字', '汉字')
print(is_similar)  # Output: True
```

### Generate Similar Words
Generate a list of words by replacing each kanji with its equivalent itaiji.
```python
similar_words = Itaiji.get_similar('漢字')
print(similar_words)  # Output: ['漢字', '㵄字', '漢字', '汉字']
```

You can also specify the number of replacing.
```python
similar_words = Itaiji.get_similar("低頭思故郷", n=1)
print(similar_words)  # Output: ['低頭思故郷', '低頭思故鄕', '低頭思故乡', '低頭楒故郷', '低頭䰄故郷', '低頭恖故郷', '低头思故郷', '氐頭思故郷', '仾頭思故郷']
```

# Data
The package uses a JSON file (ja-itaiji.json) that contains mappings of kanji to their itaiji. Ensure that this file is located in the correct directory as specified by `ITAIJI_PATH`.

# License
This project is licensed under the MIT License. See the LICENSE file for details.