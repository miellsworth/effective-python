# Chapter 1 - Pythonic Thinking
"""
An introduction to the adjective "Pythonic" and how it is used to described code
that follows a coding style that prefers to be explicit, simple over complex and
readable.
"""

## Item 1: Know which version of python you're using
# At the command line
"""
python --version
or check for installed versions using
py --list-paths
or pick the specific version you would like to use using
py -X.Y
"""

# At runtime
import sys
print(sys.version_info)
print(sys.version)

## Item 2: Follow the PEP 8 style guide
"""
Whitespace: 
- Perhaps the biggest surprise here is spaces instead of tabs
but it looks like vscode already converts tabs to 4 spaces
- No other surprises: pylint should handle a lot of these rules

Naming:
- Functions, variables and attributes: lowercase_underscore
- Protected instance attributes: _leading_underscore
- Private instance attributes: __double_leading_underscore
- Classes: CapitalizeWord
- Module-level constants: ALL_CAPS
- Instance methods: use self
- Class methods: use cls

Expressions and statements:
- Use inline negation (if a is not b) instead of negation of positive
expressions (if not a is b)
- Don't check for empty containers comparing to length zero (if len(somelist) == 0).
Use if not somelist and assume empty values will implicitly evaluate to False
- Similar rule for non-empty containers (if somelist)
- Avoid single line if statements, for and while loops and except compound statements
- If an expression doesn't fit on one line, surround it with parentheses and add
line breaks and indentation (instead of using \ line continuation)

Imports:
- Always include at the top of the file
- Imports should be in sections
  - standard library modules
  - third-party library modules
  - your own modules
"""

## Item 3: Know the Differences Between bytes and str
"""
Likely not the most relevant part of the chapter for me but it's interesting nonetheless!

Sequences of character data can be represented via two different types: bytes and str
- bytes: unsigned 8-bit values (binary data)
- str: Unicode code points (a unique number) that represent textual characters from human languages

Ensure you know which type you're working with as the types do not work together.
- Use helper functions to ensure you're using the type you're expecting

Reading and writing binary data requires binary mode
- 'rb' or 'wb' specified in open()

Be mindful of the text encoding you're using when reading and writing Unicode data
"""

## Item 4: Prefer Interpolated F-Strings Over C-style Format Strings and str.format
"""
Not a section of huge importance other than to remember to use F-strings

C-style format strings use the % operator and introduces a variety of problems
- code readibility
- verbosity

str.format and format solve a few of the issues but are not perfect and repeat the same mistakes

Interpolated format strings solve these issues
- Allows reference to all names in the current Python scope as part of a formatting expression
- More succinct
- Allow for directly embedded Python expressions within the format specifiers
"""
key = 'my_var'
value = 1.234

formatted = f'{key} = {value}'
print(formatted)
"""
The following represents all the different ways to format strings, showing the benefit of f strings
"""

f_string = f'{key:<10} = {value:.2f}'
c_tuple  = '%-10s = %.2f' % (key, value)
str_args = '{:<10} = {:.2f}'.format(key, value)
str_kw   = '{key:<10} = {value:.2f}'.format(key=key,
                                            value=value)
c_dict   = '%(key)-10s = %(value).2f' % {'key': key,
                                         'value': value}

assert c_tuple == c_dict == f_string
assert str_args == str_kw == f_string

## Item 5: Write Helper Functions Instead of Complex Expressions
"""
Key message of this section is to avoid the temptation of reducing code using single-line, complex expressions
and instead, use helper functions, especially if the same logic needs repeating.
-if/else expression provides a more readable alternative than 'or' and 'and'
"""
from urllib.parse import parse_qs
my_values = parse_qs('red=5&blue=0&green=',
                     keep_blank_values=True)
print(repr(my_values))

# Complex single-line
red = int(my_values.get('red', [''])[0] or 0)

# More readable helper function
def get_first_int(values, key, default=0):
    found = values.get(key, [''])
    if found[0]:
        return int(found[0])
    return default

red = get_first_int(my_values, 'red')

## Item 6: Prefer Multiple Assignment Unpacking Over Indexing
"""
In order to reduce visual noise and increase code clarity, use unpacking to avoid
explicitly indexing into sequences
"""

# Indexing
item = ('Peanut butter', 'Jelly')
first = item[0]
second = item[1]
print(first, 'and', second)

# Unpacking
item = ('Peanut butter', 'Jelly')
first, second = item
print(first, 'and', second)

# Indexing
snacks = [('bacon', 350), ('donut', 240), ('muffin', 190)]
for i in range(len(snacks)):
    item = snacks[i]
    name = item[0]
    calories = item[1]
    print(f'#{i+1}: {name} has {calories} calories')

# Unpacking
for rank, (name, calories) in enumerate(snacks, 1):
    print(f'#{rank}: {name} has {calories} calories')

## Item 7: Prefer enumerate Over range
"""
enumerate wraps any iterator with a lazy generator and yields pairs of the 
loop index and the next value.
- provides concise syntax for looping over an iterator and getting
the index of each item of the iterator as you go
"""
flavor_list = ['vanilla', 'chocolate', 'pecan', 'strawberry']
it = enumerate(flavor_list)
print(next(it))
print(next(it))

for i, flavor in enumerate(flavor_list):
    print(f'{i + 1}: {flavor}')

# Make shorter - specify the number from which enumerate should begin counting
for i, flavor in enumerate(flavor_list, 1):
    print(f'{i}: {flavor}')

## Item 8: Use zip to Process Iterators in Parallel
"""
The zip built-in function can iterate over multiple iterators in parallel
- creates a lazy generator that produces tuples
- truncates its output silently to the shortest iterator
- zip_longest is preferred for iterators of unequal lenths
"""
names = ['Cecilia', 'Lise', 'Marie']
counts = [len(n) for n in names]
print(counts)

#Set-up example
longest_name = None
max_count = 0

# Not-preferred method of iterating over multiple iterators
for i in range(len(names)):
    count = counts[i]
    if count > max_count:
        longest_name = names[i]
        max_count = count

# Slightly preferred but still not great
for i, name in enumerate(names):
    count = counts[i]
    if count > max_count:
        longest_name = name
        max_count = count

# Preferred - use zip
for name, count in zip(names, counts):
    if count > max_count:
        longest_name = name
        max_count = count

# Use zip_longest for iterators of unequal lengths
names.append('Rosalind')

# zip will ignore 'Rosalind'
for name, count in zip(names, counts):
    print(name)

# zip_longest will include 'Rosalind' and fill value with default None
import itertools
for name, count in itertools.zip_longest(names, counts):
    print(f'{name}: {count}')
