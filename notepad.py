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

## Item 9: Avoid else Blocks After for and while Loops
"""
Python allows for else blocks to immediately follow for and while loop interior
blocks.

- The behaviour of this else block is unintuitive and the simple lesson is to avoid
using them whenever possible
- Not much more to it!
"""

## Item 10: Prevent Repetition with Assignment Expressions
"""
The assignment expression is also known as the walrus operator! Because it looks
like a walrus!! :=

- Used to assign and evaluate variable names in a single expression
    - Assign and evaluate, assign and evaluate, assign and evaluate!
- When an assignment expression is a subexpression of a larger expression, it must be
surrounded by parentheses
- Helpful to assign variables in places such as if statements or while loops
"""
# Set-up example
fresh_fruit = {
    'apple': 10,
    'banana': 8,
    'lemon': 5,
}

def make_lemonade(count):
    ...
def out_of_stock():
    ...

# Old syntax
count = fresh_fruit.get('lemon', 0)
if count:
    make_lemonade(count)
else:
    out_of_stock()

# New syntax with assignment operator
if count := fresh_fruit.get('lemon', 0):
    make_lemonade(count)
else:
    out_of_stock()

# Subexpression example
def make_cider(count):
    ...

if (count := fresh_fruit.get('apple', 0)) >= 4:  # Include those parentheses!
    make_cider(count)
else:
    out_of_stock()

# While loop example
def pick_fruit():
    ...
def make_juice(fruit, count):
    ...

bottles = []
while fresh_fruit := pick_fruit():  # Re-assigns fresh fruit and conditionally evaluated
    for fruit, count in fresh_fruit.items():
        batch = make_juice(fruit, count)
        bottles.extend(batch)

# Chapter 2 - Lists and Dictionaries
## Item 11: Know How to Slice Sequences
"""
Slicing: access a subset of a sequence's items with minimal effort
- somelist[start:end]  (start is inclusive, end is exclusive)
"""
a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

# Slice Do
a[:5]  # leave out zero index to reduce visual noise
a[5:]  # leave out the final index

# Slice Don't
a[0:5]
a[5:len(a)]

"""
The result of a slicing a list is a whole new list. References to the objects
from the original list are maintained. Modifying the result of slicing won't affect
the original list.
"""
b = a[3:]
print('Before:   ', b)
b[1] = 99
print('After:    ', b)
print('No change:', a)

"""
Values before and after an assigned slice will be preserved if lengths of the 
slice assignment aren't the same.
"""
print('Before ', a)
# [2:7] is a slice of length 5, while the assigned list is of length 3
a[2:7] = [99, 22, 14]
print('After  ', a)

print('Before ', a)
# [2:3] is a slice of length 1, while the assigned list is of length 2
a[2:3] = [47, 11]

# list a will grow now
print('After  ', a)

"""
You can create a copy of a list by leaving the start and end indexes blank
"""
b = a[:]
assert b == a and b is not a

## Item 12: Avoid Striding and Slicing in a Single Expression
"""
Striding: lets you take every nth item when slicing a sequence
- somelist[start:end:stride]

Using this syntax can make your slice look very confusing
- It is preferred to use positive stride values w/o start or end indexes
- It is prefered to split up stride and start/end indexes into two assignments
if all three are needed
"""
# Use a positive stride value and split up the assignment
x = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
y = x[::2]   # ['a', 'c', 'e', 'g']
z = y[1:-1]  # ['c', 'e']

## Item 13: Prefer Catch-All Unpacking Over Slicing
"""
Starred expression will catch-all remaining values that didn't match any other
part of the unpacking pattern and put them in a list
- Can be used in any position
- Can't be used on their own
- Can't be used multiple times
- Will create an empty list if there are no remaining values
"""
car_ages = [0, 9, 4, 8, 7, 20, 19, 1, 6, 15]
car_ages_descending = sorted(car_ages, reverse=True)

# Messy syntax using slicing, error prone
oldest = car_ages_descending[0]
second_oldest = car_ages_descending[1]
others = car_ages_descending[2:]
print(oldest, second_oldest, others)

# Cleaner syntax using unpacking and starred expression
oldest, second_oldest, *others = car_ages_descending
print(oldest, second_oldest, others)

# Starred expressions can be used in any position
oldest, *others, youngest = car_ages_descending
print(oldest, youngest, others)

*others, second_youngest, youngest = car_ages_descending
print(youngest, second_youngest, others)

# Starred expressions can't be used on their own
*others = car_ages_descending

# Starred expressions can't be used multiple times
first, *middle, *second_middle, last = [1, 2, 3, 4]

# Starred expressions can be used multiple times in an unpacking assignment statement
## NOT RECOMMENDED - JUST AN ILLUSTRATION
car_inventory = {
    'Downtown': ('Silver Shadow', 'Pinto', 'DMC'),
    'Airport': ('Skyline', 'Viper', 'Gremlin', 'Nova'),
}
((loc1, (best1, *rest1)),
 (loc2, (best2, *rest2))) = car_inventory.items()
print(f'Best at {loc1} is {best1}, {len(rest1)} others')
print(f'Best at {loc2} is {best2}, {len(rest2)} others')

## Item 14: Sort by Complex Criteria Using the key Parameter
"""
For sorting objects (outside of built-in types, strings, floats, etc.),
the built-in sort method does not work (unless using special methods which is uncommon).

Use the key parameter of the sort method to supply a helper function
- A lambda keyword is required to specify which part of the object to sort

A lambda keyword is also helpful for built-in types to do transformations on the values
before sorting.

Sorting by multiple criteria is possible using tuples but the order must be the same
for each criteria (i.e., both ascending, both descending)
"""
# Set-up example, sort object
class Tool:
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight
    def __repr__(self):
        return f'Tool({self.name!r}, {self.weight})'

tools = [
    Tool('level', 3.5),
    Tool('hammer', 1.25),
    Tool('screwdriver', 0.5),
    Tool('chisel', 0.25),
]

# Does not work
tools.sort()

# Sorting using lambda keyword
print('Unsorted:', repr(tools))
tools.sort(key=lambda x: x.name)
print('\nSorted:  ', tools)
tools.sort(key=lambda x: x.weight)
print('\nBy weight:', tools)

# Transform and sort
places = ['home', 'work', 'New York', 'Paris']
places.sort()
print('Case sensitive:  ', places)
places.sort(key=lambda x: x.lower())
print('Case insensitive:', places)

# Sorting by multiple criteria using tuples
power_tools = [
    Tool('drill', 4),
    Tool('circular saw', 5),
    Tool('jackhammer', 40),
    Tool('sander', 4),
]

## Sort by weight then name
power_tools.sort(key=lambda x: (x.weight, x.name))
print(power_tools)

## Sort by weight (descending) then name (ascending)
power_tools.sort(key=lambda x: (-x.weight, x.name))
print(power_tools)

## Sort by name (ascending) then weight (descending)
power_tools.sort(key=lambda x: x.name)   # Name ascending
power_tools.sort(key=lambda x: x.weight, # Weight descending
                 reverse=True)
print(power_tools)

## Item 15: Be Cautious When Relying on dict Insertion Ordering
"""
Dictionary ordering was not built-in prior to Python 3.6. Since Python 3.7, you can
rely on the fact that iterating a dict instance's contents will occur in the same
order in which the keys were initially added.

If you define objects that act like dictionaries but aren't dict instances, you can't
assume that insertion ordering will be preserved.
- To avoid this problem:
    - Write code that doesn't rely on insertion ordering
    - Explicitly check for the dict type at runtime
        if not isintance(object, dict):
            raise TypeError('must provide a dict instance')
    - Require dict values using type annotations and static analysis
        def function (dict1: Dict[str, int], dict2: Dict[str, int])
"""

## Item 16: Prefer get Over in and KeyError to Handle Missing Dictionary Keys
"""
There are four ways to handle missing keys
- in expressions
- KeyError exceptions
- the get method (PREFERRED)
- the setdefault method
"""
# Set-up example
counters = {
    'pumpernickel': 2,
    'sourdough': 1,
}

# Increment counter with a new vote, using in expression
key = 'wheat'
if key in counters:
    count = counters[key]
else:
    count = 0
counters[key] = count + 1

# Increment counter with a new vote, using KeyError exception
try:
    count = counters[key]
except KeyError:
    count = 0
counters[key] = count + 1

# PREFERRED - Increment counter with a new vote, using get method
count = counters.get(key, 0)  # Assigns key with 0 if it doesn't exist
counters[key] = count + 1

# A more complex example
votes = {
    'baguette': ['Bob', 'Alice'],
    'ciabatta': ['Coco', 'Deb'],
}
key = 'brioche'
who = 'Elmer'

names = votes.get(key)
if names is None:
    votes[key] = names = []
names.append(who)

## Further simplified using assignment expression
if (names := votes.get(key)) is None:
    votes[key] = names = []
names.append(who)

## Further simplified using the setdefault method, might be too difficult to understand
## and introduces potential bugs
names = votes.setdefault(key, [])
names.append(who)

## Item 17: Prefer defaultdict Over setdefault to Handle Missing Items in Internal State
"""
This section has some details that probably aren't overly important for me.

Some key things to remember:
    - If you're creating a dictionary to manage an arbitrary set of potential keys,
    then you should prefer using defaultdict instance from the collections built-in
    module
    - If a dictionary of arbitrary keys is passed to you, and you don't control
    its creation, then you should prefer the get method to access its items
"""
from collections import defaultdict
class Visits:
    def __init__(self):
        self.data = defaultdict(set)
    def add(self, country, city):
        self.data[country].add(city)
visits = Visits()
visits.add('England', 'Bath')
visits.add('England', 'London')
print(visits.data)

## Item 18: Know How to Construct Key-Dependent Default Values with __missing__
"""
There are instances where setdefault and defaultdict is NOT the right fit
    - __missing__ helps handle those cases
"""
path = 'profile_1234.png'

def open_picture(profile_path):
    try:
        return open(profile_path, 'a+b')
    except OSError:
        print(f'Failed to open path {profile_path}')
        raise

class Pictures(dict):
    def __missing__(self, key):
        value = open_picture(key)
        self[key] = value
        return value

pictures = Pictures()
handle = pictures[path]
handle.seek(0)
image_data = handle.read()
