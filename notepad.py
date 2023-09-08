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
"""

"""

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

# Chapter 3 - Functions
"""

"""

## Item 19: Never Unpack More Than Three Variables
## When Functions Return Multiple Values
"""
Self explanatory section. Key things to note:
    - You can have functions that return multiple values but returning
    four or more variables is error prone and should be avoided
    - Return a small class or namedtuple instance instead
"""

## Item 20: Prefer Raising Exceptions to Returning None
"""
Functions that return None to indicate special meaning are error prone
    - None and other values (e.g., zero, empty string) all evaluate to False

Raise exceptions to indicate special situations instead of returning None
    - Expect the calling code to handle exceptions properly when they're documented

Type annotations can be used to make it clear that a funciton will never return
the value None, even in special situations
"""
# Use None as an illustration that it can cause bugs
def careful_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None

x, y = 0, 5
result = careful_divide(x, y)  # result is 0
if not result:
    print('Invalid inputs')  # This runs! But shouldn't

# Use exceptions, the preferred method
def careful_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError as e:
        raise ValueError('Invalid inputs')

x, y = 5, 2
try:
    result = careful_divide(x, y)
except ValueError:
    print('Invalid inputs')
else:
    print('Result is %.1f' % result)

# Use type annotations to show the return value is always a float
# Document the exception-raising behaviour
def careful_divide(a: float, b: float) -> float:
    """Divides a by b.
    Raises:
        ValueError: When the inputs cannot be divided.
    """
    try:
        return a / b
    except ZeroDivisionError as e:
        raise ValueError('Invalid inputs')

## Item 21: Know How Closures Interact with Variable Scope
"""
Closure functions can refer to variables from any of the scopes in which they were
defined.

By default, closures can't affect enclosing scopes by assigning variables.

Use the nonloca statement to indicate when a closure can modify a variable in its
enclosing scopes.

Avoid using nonlocal statements for anything beyond simple functions.
"""
# Example of closure functions referring to variables from the scope in which they were defined
def sort_priority(values, group):
    def helper(x):  # helper can reference group
        if x in group:
            return (0, x)
        return (1, x)
    values.sort(key=helper)

numbers = [8, 3, 1, 2, 5, 4, 7, 6]
group = {2, 3, 5, 7}
sort_priority(numbers, group)
print(numbers)

# Example of closures not affecting the enclosing scopes
def sort_priority2(numbers, group):
    found = False
    def helper(x):
        if x in group:
            found = True  # found cannot be referenced by sort_priority2
            return (0, x)
        return (1, x)
    numbers.sort(key=helper)
    return found

found = sort_priority2(numbers, group)
print('Found:', found)
print(numbers)

# Example of how nonlocal can resolve this issue
def sort_priority3(numbers, group):
    found = False
    def helper(x):
        nonlocal found  # Added
        if x in group:
            found = True
            return (0, x)
        return (1, x)
    numbers.sort(key=helper)
    return found

# When nonlocal isn't recommended (non-simple functions), use a helper class
class Sorter:
    def __init__(self, group):
        self.group = group
        self.found = False
    def __call__(self, x):
        if x in self.group:
            self.found = True
            return (0, x)
        return (1, x)

sorter = Sorter(group)
numbers.sort(key=sorter)
assert sorter.found is True

## Item 22: Reduce Visual Noise with Variable Positional Arguments
"""
Functions can accept a variable number of positional arguments by using
*args in the def statement.

You can use the items from a sequence as the positional arguments for a function 
with the * operator

Using the * operator with a generator may cause a program to run out of memory and crash

Adding new positional parameters to functions that accept *args can introduce
hard to detect bugs
"""
# Example w/o variable positional arguments
def log(message, values):
    if not values:
        print(message)
    else:
        values_str = ', '.join(str(x) for x in values)
        print(f'{message}: {values_str}')
log('My numbers are', [1, 2])
log('Hi there', [])  # Need to define an empty list, not ideal!

# Example w/ variable positional arguments
def log(message, *values):  # The only difference
    if not values:
        print(message)
    else:
        values_str = ', '.join(str(x) for x in values)
        print(f'{message}: {values_str}')
log('My numbers are', 1, 2)
log('Hi there')  # Much better

# Example using items from a sequence as the positional argument
favorites = [7, 33, 99]
log('Favorite colors', *favorites)

# Example of using the * operator with a generator
def my_generator():
    for i in range(10):
        yield i
def my_func(*args):
    print(args)
it = my_generator()
my_func(*it)  # Iterates through the generator until it's exhausted, could be bad!

# Example of new positional parameters creating issues!
def log(sequence, message, *values):
    if not values:
        print(f'{sequence} - {message}')
    else:
        values_str = ', '.join(str(x) for x in values)
        print(f'{sequence} - {message}: {values_str}')
log(1, 'Favorites', 7, 33)      # New with *args OK
log(1, 'Hi there')              # New message only OK
log('Favorite numbers', 7, 33)  # Old usage breaks

## Item 23: Provide Optional Behaviour with Keyword Arguments
"""
Function arguments can be specified by position or by keyword.

Keywords make it clear what the purpose of each argument is instead of using
positional arugments and having to reference the implementation of the function.

Keyword arguments with default values make it easy to add new behaviours to a function
without needing to migrate all existing callers.

Optional keyword arguments should always be passed by keyword instead of by position.
"""
# Arguments specified by position and keyword
def remainder(number, divisor):
    return number % divisor

remainder(20, 7)  # Both position
remainder(20, divisor=7)  # position and keyword
remainder(number=20, divisor=7)  # keyword and keyword
remainder(divisor=7, number=20)  # keyword and keyword in different positions

# Positional arguments must be specified before keyword arguments
## Correct
remainder(20, divisor=7)

## Incorrect
remainder(number=20, 7)

# You can use an existing dictionary to pass in keyword arguments
my_kwargs = {
    'number': 20,
    'divisor': 7,
}
remainder(**my_kwargs)

# You can build a function that will receive any named keyword arguments
def print_parameters(**kwargs):
    for key, value in kwargs.items():
        print(f'{key} = {value}')
print_parameters(alpha=1.5, beta=9, gamma=4)

# Use default keyword arguments
def flow_rate(weight_diff, time_diff,
              period=1, units_per_kg=1):
    return ((weight_diff * units_per_kg) / time_diff) * period

# Always use keyword arguments over positional arguments when changing defaults
weight_diff = 0.5
time_diff = 3
pounds_per_hour = flow_rate(weight_diff, time_diff,
                            period=3600, units_per_kg=2.2)

## Item 24: Use None and Docstrings to Specify Dynamic Default Arguments
"""
A default argument value is evaluated only once: during function definition at module
load time. This can cause odd behaviours for dynamic values (e.g., {}, [] or datetime.now())

Use None as the default value for any keyword argument that has a dynamic value. Document
the actual default behaviour in the function's docstring.

Using None to represent keyword argument default values also works correctly with type
annotations.
"""
# How dynamic default argument values can create issues
from time import sleep
from datetime import datetime
def log(message, when=datetime.now()):
    print(f'{when}: {message}')

# These two calls to log will return the same datetime
log('Hi there!')
sleep(0.1)
log('Hello again!')

# This is because the default argument value is evaluated only once!

# Use None as the default value to resolve this issue

def log(message, when=None):
    """Log a message with a timestamp.
    Args:
        message: Message to print.
        when: datetime of when the message occurred.
            Defaults to the present time.
    """
    if when is None:
        when = datetime.now()
    print(f'{when}: {message}')

# These two calls to log will now return different datetimes
log('Hi there!')
sleep(0.1)
log('Hello again!')

# How dynamic default argument values can create issues example 2
import json

def decode(data, default={}):
    try:
        return json.loads(data)
    except ValueError:
        return default

foo = decode('bad data')
foo['stuff'] = 5
bar = decode('also bad')
bar['meep'] = 1

# These return the same dictionary because they reference the same default {}
print('Foo:', foo)
print('Bar:', bar)

# Use None as the default value to resolve this issue
def decode(data, default=None):
    """Load JSON data from a string.
    Args:
        data: JSON data to decode.
        default: Value to return if decoding fails.
            Defaults to an empty dictionary.
    """
    try:
        return json.loads(data)
    except ValueError:
        if default is None:
            default = {}  # Default is now run when the function is called
        return default

foo = decode('bad data')
foo['stuff'] = 5
bar = decode('also bad')
bar['meep'] = 1
print('Foo:', foo)
print('Bar:', bar)
assert foo is not bar

# Type annotations
from typing import Optional
def log_typed(message: str,
              when: Optional[datetime]=None) -> None:
    """Log a message with a timestamp.
    Args:
        message: Message to print.
        when: datetime of when the message occurred.
            Defaults to the present time.
    """
    if when is None:
        when = datetime.now()
    print(f'{when}: {message}')

## Item 25: Enforce Clarity with Keyword-Only and Positional-Only Arguments
"""
Python gives you the option to specify arguments that have to be called by keywords
    - Defined after a single * in the argument list

Python also gives you the option to specify arguments that have to be called positionally
    - Defined before a single / in the argument list

Parameters between / and * characters can be called by keyword or positionally
"""
# Keyword arguments enforced
def safe_division_c(number, divisor, *,  # Use * to enforce keyword arguments
                  ignore_overflow,
                  ignore_zero_division):
    try:
        return number / divisor
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else: raise

# This will not work because ignore_overflow and ignore_zero_division
# are not called via keyword arguments
safe_division_c(1.0, 10**500, True, False)

# This will work though
result = safe_division_c(1.0, 0, ignore_zero_division=True)
assert result == float('inf')

# Positional arguments enforced
def safe_division_d(number, divisor, /, *,  # Use / to enforce positional arguments
                  ignore_overflow,
                  ignore_zero_division):
    try:
        return number / divisor
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else: raise

# works
assert safe_division_d(2, 5) == 0.4

# does not work, using keyword arguments when you should use positional
safe_division_d(numerator=2, denominator=5)

# Flexible arguments between enforced positional and keyword arguments
def safe_division_e(numerator, denominator, /,
                    ndigits=10, *,  # Flexible argument
                    ignore_overflow=False,
                    ignore_zero_division=False):
    try:
        fraction = numerator / denominator
        return round(fraction, ndigits)
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else: raise

# All work
result = safe_division_e(22, 7)
print(result)
result = safe_division_e(22, 7, 5)
print(result)
result = safe_division_e(22, 7, ndigits=2)
print(result)

## Item 26: Define Function Decorators with functools.wraps
"""
Decorators in Python are syntax to allow one function to modify another function
at runtime.

Using decorators can cause strange behaviours in tools that do introspection, such
as debuggers.

Use the wraps decorator from the functools built-in module when you define your
own decorators to avoid issues.
"""
# Example decorator w/o wraps
def trace(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f'{func.__name__}({args!r}, {kwargs!r}) '
              f'-> {result!r}')
        return result
    return wrapper

# Call the decorator using the @ symbol
@trace
def fibonacci(n):
    """Return the n-th Fibonacci number"""
    if n in (0, 1):
        return n
    return (fibonacci(n - 2) + fibonacci(n - 1))

# Call the decorator by wrapping it with the intended function
fibonacci = trace(fibonacci)

# Decorated function
fibonacci(4)

# Issue with introspection!
print(fibonacci)
help(fibonacci)

# Resolve the issue with introspection by using wraps
from functools import wraps

def trace(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f'{func.__name__}({args!r}, {kwargs!r}) '
              f'-> {result!r}')
        return result
    return wrapper

@trace
def fibonacci(n):
    """Return the n-th Fibonacci number"""
    if n in (0, 1):
        return n
    return (fibonacci(n - 2) + fibonacci(n - 1))

# Issue resolved :)
print(fibonacci)
help(fibonacci)

# Chapter 4 - Comprehensions and Generators
"""

"""

## Item 27: Use Comprehensions Instead of map and filter
"""
I'm not overly familiar with map and filter but know comprehensions quite well.
Key message here is that I shouldn't bother to spend much time learning about
those two functions!

Reasons comprehensions are more appropriate than map and filter
- Comprehensions are clearer because they don't require lambda expressions
- Comprehensions allow for conditional statements that can skip items from the input
list whereas map doesn't without help from filter
- Don't forget about dictionary and set comprehensions! It's not just about lists!
"""
a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Do
squares = [x**2 for x in a]  # List comprehension
print(squares)

# Don't - for loop
squares = []
for x in a:
    squares.append(x**2)
print(squares)

# Don't - map
alt = map(lambda x: x ** 2, a)

# Do - comprehension with a filter
even_squares = [x**2 for x in a if x % 2 == 0]
print(even_squares)

# Don't - map with filter (it's unclear!)
alt = map(lambda x: x**2, filter(lambda x: x % 2 == 0, a))
assert even_squares == list(alt)

# Dictionary and set comprehensions
even_squares_dict = {x: x**2 for x in a if x % 2 == 0}
threes_cubed_set = {x**3 for x in a if x % 3 == 0}
print(even_squares_dict)
print(threes_cubed_set)

# Alternative with map and filter - not clear!
alt_dict = dict(map(lambda x: (x, x**2),
                filter(lambda x: x % 2 == 0, a)))
alt_set = set(map(lambda x: x**3,
              filter(lambda x: x % 3 == 0, a)))

## Item 28: Avoid More Than Two Control Subexpressions in Comprehensions
"""
Multiple levels of loops and conditional statements are possible in comprehensions
but one should avoid more than two.
- Either stick with two loops, two conditions or one condition and one loop
as they become difficult to read when there are more than two control subexpressions
"""

# Do
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [x for row in matrix for x in row]
print(flat)

squared = [[x**2 for x in row] for row in matrix]
print(squared)

# Don't - this is clearer as a for loop
my_lists = [
    [[1, 2, 3], [4, 5, 6]],
]
flat = [x for sublist1 in my_lists
        for sublist2 in sublist1
        for x in sublist2]

# For loop is clearer
flat = []
for sublist1 in my_lists:
    for sublist2 in sublist1:
        flat.extend(sublist2)

"""
One other thing to note, multiple if conditions at the same loop level
are possible and have an implicit and expression
"""
# b and c are equivalent
a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
b = [x for x in a if x > 4 if x % 2 == 0]  # if if
c = [x for x in a if x > 4 and x % 2 == 0]  # if and

## Item 29: Avoid Repeated Work in Comprehensions by Using Assignment Expressions
"""
Assignment expressions make it possible for comprehensions and generator expressions
to reuse the value from one condition elsewhere in the same comprehension

Don't use the assignment expression outside of the comprehension's condition. Can result
in leaking of the loop variable.
"""
# Set-up example
stock = {
    'nails': 125,
    'screws': 35,
    'wingnuts': 8,
    'washers': 24,
}
order = ['screws', 'wingnuts', 'clips']
def get_batches(count, size):
    return count // size

# For loop example
result = {}
for name in order:
  count = stock.get(name, 0)
  batches = get_batches(count, 8)
  if batches:
    result[name] = batches
print(result)

# Dictionary comprehension example - somewhat more succinct
found = {name: get_batches(stock.get(name, 0), 8)
         for name in order
         if get_batches(stock.get(name, 0), 8)}
print(found)

# Dictionary comprehension with assignment expression - more succinct
found = {name: batches for name in order
         if (batches := get_batches(stock.get(name, 0), 8))}

# Using an assignment expression in a dict comprehension incorrectly
result = {name: (tenth := count // 10)
          for name, count in stock.items() if tenth > 0}

# Correcting the previous example
result = {name: tenth for name, count in stock.items()
          if (tenth := count // 10) > 0}
print(result)

# Example of a leaking loop variable
half = [(last := count // 2) for count in stock.values()]
print(f'Last item of {half} is {last}')

## Item 30: Consider Generators Instead of Returning Lists
"""
- Using generators can be clearer than the alternative of having a
function return a list of accumulated results.
- The iterator returned by a generator produces the set of values
passed to yield expressions within the generator function's body.
- Generators can produce a sequence of outputs for arbitrarily large
inputs because their working memory doesn't include all inputs and
outputs.
"""
# Set-up example - returning lists
def index_words(text):
    result = []
    if text:
        result.append(0)
    for index, letter in enumerate(text):
        if letter == ' ':
            result.append(index + 1)
    return result

address = 'Four score and seven years ago...'
result = index_words(address)
print(result[:10])

# Producing the same result with a generator
def index_words_iter(text):
    if text:
        yield 0
    for index, letter in enumerate(text):
        if letter == ' ':
            yield index + 1

it = index_words_iter(address)
print(next(it))
print(next(it))

# Create a list from the generator
result = list(index_words_iter(address))
print(result[:10])

## Item 31: Be defensive when iterating over arguments
"""
- Beware of functions and methods that iterate over input arguments
multiple times. If these arguments are iterators, you may see
strange behavior and missing values.
- Python's iterator protocol defines how containers and iterators interact
with the iter and next built-in functions, for loops, and related
expressions.
- You can easily define your own iterable container type by implementing
the __iter__ method as a generator.
- You can detect that a value is an iterator (instead of a container)
if calling iter on it produces the same value as what you passed
in.
- Alternatively, you can use the isinstance built-in function along
with the collections.abc.Iterator class.
"""
# Iterating over a list multiple times
def normalize(numbers):
    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result

visits = [15, 35, 80]
percentages = normalize(visits)
print(percentages)
assert sum(percentages) == 100.0

# Iterating over a file using a generator
def read_visits(data_path):
    with open(data_path) as f:
        for line in f:
            yield int(line)

# Test the read_visits function
it = read_visits('my_numbers.txt')
percentages = normalize(it)  # This will exhaust the generator
print(percentages)  # As a result, this will return no result

it = read_visits('my_numbers.txt')
print(list(it))
print(list(it)) # Already exhausted, no result

# Avoid this behaviour, copy as a list (can result in memory issues though!)
def normalize_copy(numbers):
    numbers_copy = list(numbers) # Copy the iterator
    total = sum(numbers_copy)
    result = []
    for value in numbers_copy:
        percent = 100 * value / total
        result.append(percent)
    return result

# Resolves the issue
it = read_visits('my_numbers.txt')
percentages = normalize_copy(it)
print(percentages)
assert sum(percentages) == 100.0

# Resolve potential memory issues by creating a new iterator
def normalize_func(get_iter):
    total = sum(get_iter()) # New iterator
    result = []
    for value in get_iter(): # New iterator
        percent = 100 * value / total
        result.append(percent)
    return result

path = 'my_numbers.txt'
# Requires a lambda function which is a bit clumsy...
percentages = normalize_func(lambda: read_visits(path))
print(percentages)
assert sum(percentages) == 100.0

# Use the iterator protocol instead! This is an iterable container
class ReadVisits:
    def __init__(self, data_path):
        self.data_path = data_path
    def __iter__(self):
        with open(self.data_path) as f:
            for line in f:
                yield int(line)

visits = ReadVisits(path)
percentages = normalize(visits)
print(percentages)
assert sum(percentages) == 100.0

# Create a function to check to ensure the iterator can be repeatedly iterated over
def normalize_defensive(numbers):
    if iter(numbers) is numbers: # An iterator -- bad!
        raise TypeError('Must supply a container')
    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result

# Use collections to check for an iterable container
from collections.abc import Iterator
def normalize_defensive(numbers):
    if isinstance(numbers, Iterator): # Another way to check
        raise TypeError('Must supply a container')
    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result

visits = [15, 35, 80]
percentages = normalize_defensive(visits)
assert sum(percentages) == 100.0
visits = ReadVisits(path)
percentages = normalize_defensive(visits)
assert sum(percentages) == 100.0

# Throws an error if the input is an iterator rather than a container
visits = [15, 35, 80]
it = iter(visits)
normalize_defensive(it)

## Item 32: Consider Generator Expressions for Large List Comprehensions
"""
- List comprehensions can cause problems for large inputs by using
too much memory.
- Generator expressions avoid memory issues by producing outputs
one at a time as iterators.
- Generator expressions can be composed by passing the iterator from
one generator expression into the for subexpression of another.
- Generator expressions execute very quickly when chained together
and are memory efficient.
- Be careful though! The outputs are stateful!
"""
# A list comprehension that can only handle small input files
value = [len(x) for x in open('my_file.txt')]
print(value)

# A generator comprehension that can handle larger input files
it = (len(x) for x in open('my_file.txt'))
print(it)

print(next(it))
print(next(it))

# Use a generator as an input to a generator expression
roots = ((x, x**0.5) for x in it)
print(next(roots))

## Item 33: Compose Multiple Generators with yield from
"""
- The yield from expression allows you to compose multiple nested
generators together into a single combined generator.
- yield from provides better performance than manually iterating
nested generators and yielding their outputs.
"""
# Set-up example
def move(period, speed):
    for _ in range(period):
        yield speed
def pause(delay):
    for _ in range(delay):
        yield 0

# A bit repetitive...
def animate():
    for delta in move(4, 5.0):
        yield delta
    for delta in pause(3):
        yield delta
    for delta in move(2, 3.0):
        yield delta

def render(delta):
    print(f'Delta: {delta:.1f}')
    # Move the images onscreen

def run(func):
    for delta in func():
        render(delta)

run(animate)

# Remove the repetition with yield from and speed things up!
def animate_composed():
    yield from move(4, 5.0)
    yield from pause(3)
    yield from move(2, 3.0)

run(animate_composed)

## Item 34: Avoid Injecting Data into Generators with send
"""
- The send method can be used to inject data into a generator by giving
the yield expression a value that can be assigned to a variable.
- Using send with yield from expressions may cause surprising
behavior, such as None values appearing at unexpected times in the
generator output.
- Providing an input iterator to a set of composed generators is a better
approach than using the send method, which should be avoided.
"""
# Final example...
import math

def transmit(output):
    if output is None:
        print(f'Output is None')
    else:
        print(f'Output: {output:>5.1f}')

def wave_cascading(amplitude_it, steps):
    step_size = 2 * math.pi / steps
    for step in range(steps):
        radians = step * step_size
        fraction = math.sin(radians)
        amplitude = next(amplitude_it) # Get next input
        output = amplitude * fraction
        yield output

def complex_wave_cascading(amplitude_it):
    yield from wave_cascading(amplitude_it, 3)
    yield from wave_cascading(amplitude_it, 4)
    yield from wave_cascading(amplitude_it, 5)

def run_cascading():
    amplitudes = [7, 7, 7, 2, 2, 2, 2, 10, 10, 10, 10, 10]
    it = complex_wave_cascading(iter(amplitudes))
    for amplitude in amplitudes:
        output = next(it)
        transmit(output)

run_cascading()

## Item 35: Avoid Causing State Transitions in Generators with throw
"""
- The throw method can be used to re-raise exceptions within
generators at the position of the most recently executed yield
expression.
- Using throw harms readability because it requires additional nesting
and boilerplate in order to raise and catch exceptions.
- A better way to provide exceptional behavior in generators is to use
a class that implements the __iter__ method along with methods to
cause exceptional state transitions.
"""
# Example of using throw to re-raise Exception instances within generator functions
class MyError(Exception):
    pass
def my_generator():
    yield 1
    yield 2
    yield 3
it = my_generator()
print(next(it)) # Yield 1
print(next(it)) # Yield 2
print(it.throw(MyError('test error')))

## Item 36: Consider itertools for working with iterators and generators
"""
- The itertools functions fall into three main categories for working
with iterators and generators: linking iterators together, filtering
items they output, and producing combinations of items.
- There are more advanced functions, additional parameters, and
useful recipes available in the documentation at help(itertools).
"""
import itertools

# Linking iterators together
## Chain
it = itertools.chain([1, 2, 3], [4, 5, 6])  # Combine multiple iterators
print(list(it))

## Repeat
it = itertools.repeat('hello', 3)  # Output a single value an infinite or n number of times
print(list(it))

## Cycle
it = itertools.cycle([1, 2])  # Repeat an interator's items forever
result = [next(it) for _ in range (10)]
print(result)

## Tee
it1, it2, it3 = itertools.tee(['first', 'second'], 3)  # Split an iterator into multiple iterators
print(list(it1))
print(list(it2))
print(list(it3))

## Zip longest
# Variant of the zip built-in function that returns a placeholder when an iterator is exhausted
keys = ['one', 'two', 'three']
values = [1, 2]

normal = list(zip(keys, values))
print('zip: ', normal)

it = itertools.zip_longest(keys, values, fillvalue='nope')  # fillvalue specifies the placeholder value
longest = list(it)
print('zip_longest:', longest)

# Filtering items from an iterator
## islice
# Slice an interator without copying
values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

first_five = itertools.islice(values, 5)
print('First five: ', list(first_five))

middle_odds = itertools.islice(values, 2, 8, 2)  # start=2, end=8, step size=2
print('Middle odds:', list(middle_odds))

## takewhile
# Returns items from an iterator until a specified function returns False
values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
less_than_seven = lambda x: x < 7
it = itertools.takewhile(less_than_seven, values)
print(list(it))

# dropwhile
# Skips items from an iterator when a specified function returns True, then returns items if False
values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
less_than_seven = lambda x: x < 7
it = itertools.dropwhile(less_than_seven, values)
print(list(it))

## filterfalse
values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
evens = lambda x: x % 2 == 0

# filter() filters an iterator when function is True
filter_result = filter(evens, values)
print('Filter: ', list(filter_result))

# filter() filters an iterator when function is False
filter_false_result = itertools.filterfalse(evens, values)
print('Filter false:', list(filter_false_result))

# Producing Combinations of Items from Iterators
## accumulate
# Returns accumulated sums (or other binary function results)
values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
sum_reduce = itertools.accumulate(values)
print('Sum: ', list(sum_reduce))

def sum_modulo_20(first, second):
    output = first + second
    return output % 20

modulo_reduce = itertools.accumulate(values, sum_modulo_20)
print('Modulo:', list(modulo_reduce))

## product
# Returns a cartesian product of items from one or more iterators
single = itertools.product([1, 2], repeat=2)
print('Single: ', list(single))

multiple = itertools.product([1, 2], ['a', 'b'])
print('Multiple:', list(multiple))

## permutations
# Returns unique ordered permutations of length N
it = itertools.permutations([1, 2, 3, 4], 2)  # N=2
print(list(it))

## combinations
# Returns unique unordered permutations of length N, but no repeated items
# e.g., (1, 2) returned but not (2, 1)
it = itertools.combinations([1, 2, 3, 4], 2)
print(list(it))

## combinations_with_replacement
# same as combintations but with repeated items
it = itertools.combinations_with_replacement([1, 2, 3, 4], 2)
print(list(it))

# Chapter 5 - Classes and Interfaces
"""
Python's classes and inheritance make it easy to express a program's
intended behaviors with objects. They allow you to improve and
expand functionality over time. They provide flexibility in an environment
of changing requirements. Knowing how to use them well
enables you to write maintainable code.
"""

## Item 37: Compose Classes Instead of Nesting Many Levels of Built-in Types
"""
- Avoid making dictionaries with values that are dictionaries, long
tuples, or complex nestings of other built-in types.
- Use namedtuple for lightweight, immutable data containers before
you need the flexibility of a full class.
- Move your bookkeeping code to using multiple classes when your
internal state dictionaries get complicated.
"""

# Set-up example
class SimpleGradebook:
    def __init__(self):
        self._grades = {}

    def add_student(self, name):
        self._grades[name] = []

    def report_grade(self, name, score):
        self._grades[name].append(score)

    def average_grade(self, name):
        grades = self._grades[name]
        return sum(grades) / len(grades)

book = SimpleGradebook()
book.add_student('Isaac Newton')
book.report_grade('Isaac Newton', 90)
book.report_grade('Isaac Newton', 95)
book.report_grade('Isaac Newton', 85)
print(book.average_grade('Isaac Newton'))

# Modify class to include inner dictionary to log grades by subject
from collections import defaultdict

class BySubjectGradebook:
    def __init__(self):
        self._grades = {} # Outer dict
    
    def add_student(self, name):
        self._grades[name] = defaultdict(list) # Inner dict

    # New methods to account for subject
    def report_grade(self, name, subject, grade):
        by_subject = self._grades[name]
        grade_list = by_subject[subject]
        grade_list.append(grade)

    def average_grade(self, name):
        by_subject = self._grades[name]
        total, count = 0, 0
        for grades in by_subject.values():
            total += sum(grades)
            count += len(grades)
        return total / count

book = BySubjectGradebook()
book.add_student('Albert Einstein')
book.report_grade('Albert Einstein', 'Math', 75)
book.report_grade('Albert Einstein', 'Math', 65)
book.report_grade('Albert Einstein', 'Gym', 90)
book.report_grade('Albert Einstein', 'Gym', 95)
print(book.average_grade('Albert Einstein'))

# Modify class to change the weighting of each grade
class WeightedGradebook:
    def __init__(self):
        self._grades = {}
    
    def add_student(self, name):
        self._grades[name] = defaultdict(list)

    def report_grade(self, name, subject, score, weight):
        by_subject = self._grades[name]
        grade_list = by_subject[subject]
        grade_list.append((score, weight))

    # Nested for loops start to make this code complicated
    def average_grade(self, name):
        by_subject = self._grades[name]

        score_sum, score_count = 0, 0
        for subject, scores in by_subject.items():
            subject_avg, total_weight = 0, 0

            for score, weight in scores:
                subject_avg += score * weight
                total_weight += weight
            
            score_sum += subject_avg / total_weight
            score_count += 1

        return score_sum / score_count

book = WeightedGradebook()
book.add_student('Albert Einstein')
book.report_grade('Albert Einstein', 'Math', 75, 0.05)
book.report_grade('Albert Einstein', 'Math', 65, 0.15)
book.report_grade('Albert Einstein', 'Math', 70, 0.80)
book.report_grade('Albert Einstein', 'Gym', 100, 0.40)
book.report_grade('Albert Einstein', 'Gym', 85, 0.60)
print(book.average_grade('Albert Einstein'))

# Refactoring to simplify and prevent nested dictionaries using Classes
## Start with a simple tuple to capture grade and weight
grades = []
grades.append((95, 0.45))
grades.append((85, 0.55))
total = sum(score * weight for score, weight in grades)
total_weight = sum(weight for _, weight in grades)
average_grade = total / total_weight

## Including additional information starts to complicate things
grades = []
grades.append((95, 0.45, 'Great job'))
grades.append((85, 0.55, 'Better next time'))
total = sum(score * weight for score, weight, _ in grades)
total_weight = sum(weight for _, weight, _ in grades)
average_grade = total / total_weight

## Using named tuples resolves some issues
from collections import namedtuple
Grade = namedtuple('Grade', ('score', 'weight'))

# Use a class to represent a single subject that contains a set of grades
class Subject:
    def __init__(self):
        self._grades = []
    def report_grade(self, score, weight):
        self._grades.append(Grade(score, weight))
    def average_grade(self):
        total, total_weight = 0, 0
        for grade in self._grades:
            total += grade.score * grade.weight
            total_weight += grade.weight
        return total / total_weight

# Use a class to represent a set of subjects tied to a particular student
class Student:
    def __init__(self):
        self._subjects = defaultdict(Subject)
    def get_subject(self, name):
        return self._subjects[name]
    def average_grade(self):
        total, count = 0, 0
        for subject in self._subjects.values():
            total += subject.average_grade()
            count += 1
        return total / count

# Use a class to create a container for all students
class Gradebook:
    def __init__(self):
        self._students = defaultdict(Student)
    def get_student(self, name):
        return self._students[name]

book = Gradebook()
albert = book.get_student('Albert Einstein')
math_albert = albert.get_subject('Math')
math_albert.report_grade(75, 0.05)
math_albert.report_grade(65, 0.15)
math_albert.report_grade(70, 0.80)
gym_albert = albert.get_subject('Gym')
gym_albert.report_grade(100, 0.40)
gym_albert.report_grade(85, 0.60)
print(albert.average_grade())

## Item 38: Accept Functions Instead of Classes for Simple Interfaces
"""
- Instead of defining and instantiating classes, you can often simply
use functions for simple interfaces between components in Python.
- References to functions and methods in Python are first class,
meaning they can be used in expressions (like any other type).
- The __call__ special method enables instances of a class to be
called like plain Python functions.
- When you need a function to maintain state, consider defining a
class that provides the __call__ method instead of defining a stateful
closure.
"""

# Example of customizing behaviour based on passing in a function
names = ['Socrates', 'Archimedes', 'Plato', 'Aristotle']
names.sort(key=len)  # len() is the function that determines the behaviour of .sort()
print(names)

# Example of customizing the behaviour of defaultdict using a function log_missing()
def log_missing():
    print('Key added')
    return 0

from collections import defaultdict
current = {'green': 12, 'blue': 3}
increments = [
    ('red', 5),
    ('blue', 17),
    ('orange', 9),
]
result = defaultdict(log_missing, current)
print('Before:', dict(result))
for key, amount in increments:
    result[key] += amount
print('After: ', dict(result))

# Define a helper function with a stateful closure to count # of missing keys
def increment_with_report(current, increments):
    added_count = 0
    
    def missing():
        nonlocal added_count # Stateful closure
        added_count += 1
        return 0
    
    result = defaultdict(missing, current)
    for key, amount in increments:
        result[key] += amount
    return result, added_count

result, count = increment_with_report(current, increments)
assert count == 2

# Define a class that encapsulates the state you want to track
## Easier to read than stateful hooks like missing() above
class CountMissing:
    def __init__(self):
        self.added = 0

    def missing(self):
        self.added += 1
        return 0

counter = CountMissing()
## counter.missing can now be used to provide the behaviour of a stateful closure
result = defaultdict(counter.missing, current) # Method ref
for key, amount in increments:
    result[key] += amount
assert counter.added == 2

## This class can be confusing though as it's not clear that its purpose is to be used with defaultdict

# A more clear example of using a class to provide the behaviour of a stateful closure
class BetterCountMissing:
    def __init__(self):
        self.added = 0
    
    # This indicates that a class's instance will be used somewhere
    # a function argument would be suitable (like API hooks)
    def __call__(self):
        self.added += 1
        return 0

counter = BetterCountMissing()
assert counter() == 0
assert callable(counter)  # __call__ makes this class a "callable"

# Use the new class in the defaultdict example
counter = BetterCountMissing()
result = defaultdict(counter, current) # Relies on __call__
for key, amount in increments:
    result[key] += amount
assert counter.added == 2

## Item 39: Use @classmethod Polymorphism to Construct Objects Generically
"""
- Python only supports a single constructor per class: the __init__ method.
- Use @classmethod to define alternative constructors for your classes.
- Use class method polymorphism to provide generic ways to build and connect many concrete subclasses.
"""

# Create a common class to represent input data with a read method to be defined by subclasses
class InputData:
    def read(self):
        raise NotImplementedError

# Concrete subclass of InputData that reads data from a file on disk
class PathInputData(InputData):
    def __init__(self, path):
        super().__init__()
        self.path = path
    def read(self):
        with open(self.path) as f:
            return f.read()

# A common class for a MapReduce example, similar to InputData
class Worker:
    def __init__(self, input_data):
        self.input_data = input_data
        self.result = None
    
    def map(self):
        raise NotImplementedError
    
    def reduce(self, other):
        raise NotImplementedError

# A concrete subclass of Worker
class LineCountWorker(Worker):
    def map(self):
        data = self.input_data.read()
        self.result = data.count('\n')
    
    def reduce(self, other):
        self.result += other.result

# Manually build and connect the objects with helper functions
import os

## List the contents of a directory and construct a PathInputData instance for each file it contains
def generate_inputs(data_dir):
    for name in os.listdir(data_dir):
        yield PathInputData(os.path.join(data_dir, name))

## Create the LineCountWorker instances by using the InputData instances returned by generate_inputs
def create_workers(input_list):
    workers = []
    for input_data in input_list:
        workers.append(LineCountWorker(input_data))
    return workers

## Execute Worker instances by fanning out the map step to multiple threads
from threading import Thread
def execute(workers):
    threads = [Thread(target=w.map) for w in workers]
    for thread in threads: thread.start()
    for thread in threads: thread.join()

    # call reduce repeatedly to combine the results into one final value
    first, *rest = workers
    for worker in rest:
        first.reduce(worker)
    return first.result

## Connect all the pieces together in a function to run each step
def mapreduce(data_dir):
    inputs = generate_inputs(data_dir)
    workers = create_workers(inputs)
    return execute(workers)

# Run the mapreduce function on a set of test input files
import os
import random

def write_test_files(tmpdir):
    os.makedirs(tmpdir)
    for i in range(100):
        with open(os.path.join(tmpdir, str(i)), 'w') as f:
            f.write('\n' * random.randint(0, 100))

tmpdir = 'test_inputs'
write_test_files(tmpdir)

result = mapreduce(tmpdir)
print(f'There are {result} lines')

## This mapreduce function is not generic and would require a rewrite of 
## generate_inputs, create_workers, and mapreduce if we wanted to write another
## InputData or Worker subclass

# Use class method polymorphism to solve this problem
class GenericInputData:
    def read(self):
        raise NotImplementedError

    @classmethod
    def generate_inputs(cls, config):
        raise NotImplementedError

# 
class PathInputData(GenericInputData):
    ...
    
    @classmethod
    def generate_inputs(cls, config):
        data_dir = config['data_dir']
        for name in os.listdir(data_dir):
            yield cls(os.path.join(data_dir, name))

# Make creater_workers a part of the GenericWorker class
class GenericWorker:
    def __init__(self, input_data):
        self.input_data = input_data
        self.result = None

    def map(self):
        raise NotImplementedError

    def reduce(self, other):
        raise NotImplementedError

    @classmethod
    def create_workers(cls, input_class, config):  # cls() constructs GenericWorker objects
        workers = []
        for input_data in input_class.generate_inputs(config):
            workers.append(cls(input_data))
        return workers

# Change the parent class
class LineCountWorker(GenericWorker):
    ...

# Re-write the mapreduce function to be completely generic by calling create_workers
def mapreduce(worker_class, input_class, config):
    workers = worker_class.create_workers(input_class, config)
    return execute(workers)

# Run on test files
config = {'data_dir': tmpdir}
result = mapreduce(LineCountWorker, PathInputData, config)
print(f'There are {result} lines')

## This now allows for the ability to flexibly create GenericInputData or GenericWorker subclasses

## Item 40: Initialize Parent Classes with super
"""
- Python's standard method resolution order (MRO) solves the problems
of superclass initialization order and diamond inheritance.
- Use the super built-in function with zero arguments to initialize
parent classes.
"""

# Simple (but potentially error prone) way of initializing a parent class from a child class
class MyBaseClass:
    def __init__(self, value):
        self.value = value

class MyChildClass(MyBaseClass):
    def __init__(self):
        MyBaseClass.__init__(self, 5)  # Can lead to unpredictable behaviour

class TimesTwo:
    def __init__(self):
        self.value *= 2

class PlusFive:
    def __init__(self):
        self.value += 5

class OneWay(MyBaseClass, TimesTwo, PlusFive):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        TimesTwo.__init__(self)
        PlusFive.__init__(self)

foo = OneWay(5)
# MyBaseClass.__init__(self, value), value == 5
# TimesTwo.__init__(self), value == 5 * 2 = 10
# PlusFive.__init__(self), value == 10 + 5 = 15
print('First ordering value is (5 * 2) + 5 =', foo.value)

# Slightly different order in the class set-up
## This class's behavior doesn't match the order of the parent classes in its definition
class AnotherWay(MyBaseClass, PlusFive, TimesTwo):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        TimesTwo.__init__(self)
        PlusFive.__init__(self)

bar = AnotherWay(5)
# MyBaseClass.__init__(self, value), value == 5
# TimesTwo.__init__(self), value == 5 * 2 = 10
# PlusFive.__init__(self), value == 10 + 5 = 15
print('Second ordering value is', bar.value)

# Issue with diamond inheritance
class TimesSeven(MyBaseClass):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        self.value *= 7

class PlusNine(MyBaseClass):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        self.value += 9

class ThisWay(TimesSeven, PlusNine):
    def __init__(self, value):
        TimesSeven.__init__(self, value)
        PlusNine.__init__(self, value)

foo = ThisWay(5)
# TimesSeven.__init__(self, value), value == 5 * 7 = 35
# PlusNine.__init__(self, value), value == 5 + 9 == 14 (MyBaseClass gets called again)
print('Should be (5 * 7) + 9 = 44 but is', foo.value)  # value is 14

# Solve this problem via super
## Same base class
class MyBaseClass:
    def __init__(self, value):
        self.value = value

# Different sub classes with super to initialize the parent class
class TimesSevenCorrect(MyBaseClass):
    def __init__(self, value):
        super().__init__(value)
        self.value *= 7

class PlusNineCorrect(MyBaseClass):
    def __init__(self, value):
        super().__init__(value)
        self.value += 9

class GoodWay(TimesSevenCorrect, PlusNineCorrect):
    def __init__(self, value):
        super().__init__(value)

foo = GoodWay(5)
print('Should be 7 * (5 + 9) = 98 and is', foo.value)

# Print Method Resolution Order (MRO)
mro_str = '\n'.join(repr(cls) for cls in GoodWay.mro())
print(mro_str)

## When GoodWay(5) is called, it calls TimesSevenCorrect.__init__, which calls
## PlusNineCorrect.__init__, which calls MyBaseClass.__init__
## All initialization methods then do their work in opposite order
### MyBaseClass.__init__, value == 5
### PlusNineCorrect.__init__, value == 5 + 9
### TimesSevenCorrect.__init__, value == (5 + 9) * 7

# Using super without any parameters is the same as providing parameters
class ExplicitTrisect(MyBaseClass):
    def __init__(self, value):
        super(ExplicitTrisect, self).__init__(value)
        self.value /= 3

class AutomaticTrisect(MyBaseClass):
    def __init__(self, value):
        super(__class__, self).__init__(value)
        self.value /= 3

class ImplicitTrisect(MyBaseClass):
    def __init__(self, value):
        super().__init__(value)
        self.value /= 3

assert ExplicitTrisect(9).value == 3
assert AutomaticTrisect(9).value == 3
assert ImplicitTrisect(9).value == 3

## Item 41: Consider Composing Functionality with Mix-in Classes
"""
- Mix-in is a class that defines only a small set of additional methods for its
child classes to provide
- Mix-in classes don't define their own instance attributes (don't require __init__)
- Avoid using multiple inheritance with instance attributes and
__init__ if mix-in classes can achieve the same outcome.
- Use pluggable behaviors at the instance level to provide per-class
customization when mix-in classes may require it.
- Mix-ins can include instance methods or class methods, depending
on your needs.
- Compose mix-ins to create complex functionality from simple
behaviors.
"""

# Convert a python object to convert a python object to a dict
# Write it generically so that it can be used in all classes
class ToDictMixin:
    def to_dict(self):
        return self._traverse_dict(self.__dict__)

    def _traverse_dict(self, instance_dict):
        output = {}
        for key, value in instance_dict.items():
            output[key] = self._traverse(key, value)
        return output
    
    def _traverse(self, key, value):
        if isinstance(value, ToDictMixin):
            return value.to_dict()
        elif isinstance(value, dict):
            return self._traverse_dict(value)
        elif isinstance(value, list):
            return [self._traverse(key, i) for i in value]
        elif hasattr(value, '__dict__'):
            return self._traverse_dict(value.__dict__)
        else:
            return value

# Define an example class that uses the mix-in
class BinaryTree(ToDictMixin):
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

# Use the to_dict() method to translate the python object into a dict
tree = BinaryTree(10,
    left=BinaryTree(7, right=BinaryTree(9)),
    right=BinaryTree(13, left=BinaryTree(11)))
print(tree.to_dict())

# Mix-ins' generic functionality can be pluggable, meaning behaviours can be overridden if necessary

class BinaryTreeWithParent(BinaryTree):
    def __init__(self, value, left=None,
                 right=None, parent=None):
        super().__init__(value, left=left, right=right)
        self.parent = parent
    
    # Override the _traverse method to only process values that matter
    # This prevents cycles encountered by the mix-inn
    def _traverse(self, key, value):
        if (isinstance(value, BinaryTreeWithParent) and
            key == 'parent'):
            return value.value # Prevent cycles
        else:
            return super()._traverse(key, value)

# Calling BinaryTreeWithParent.to_dict works because the circular reference properties aren't followed
root = BinaryTreeWithParent(10)
root.left = BinaryTreeWithParent(7, parent=root)
root.left.right = BinaryTreeWithParent(9, parent=root.left)
print(root.to_dict())

# By defining BinaryTreeWithParent._traverse, any class with attribute type BinaryTreeWithParent automatically
# works with the ToDictMixin
class NamedSubTree(ToDictMixin):
    def __init__(self, name, tree_with_parent):
        self.name = name
        self.tree_with_parent = tree_with_parent

my_tree = NamedSubTree('foobar', root.left.right)
print(my_tree.to_dict()) # No infinite loop

# Composing mix-ins together
import json
class JsonMixin:
    @classmethod
    def from_json(cls, data):
        kwargs = json.loads(data)
        return cls(**kwargs)
    
    def to_json(self):
        return json.dumps(self.to_dict())

# The Jsonixin makes it simple to create hierarchies of utility classes that can be serialized to and from JSON
class DatacenterRack(ToDictMixin, JsonMixin):
    def __init__(self, switch=None, machines=None):
        self.switch = Switch(**switch)
        self.machines = [
            Machine(**kwargs) for kwargs in machines]
    
class Switch(ToDictMixin, JsonMixin):
    def __init__(self, ports=None, speed=None):
        self.ports = ports
        self.speed = speed

class Machine(ToDictMixin, JsonMixin):
    def __init__(self, cores=None, ram=None, disk=None):
        self.cores = cores
        self.ram = ram
        self.disk = disk


serialized = """{
    "switch": {"ports": 5, "speed": 1e9},
    "machines": [
        {"cores": 8, "ram": 32e9, "disk": 5e12},
        {"cores": 4, "ram": 16e9, "disk": 1e12},
        {"cores": 2, "ram": 4e9, "disk": 500e9}
    ]
}"""
deserialized = DatacenterRack.from_json(serialized)
roundtrip = deserialized.to_json()
assert json.loads(serialized) == json.loads(roundtrip)

# Yeah I don't really know what's going on here....

## Item 42: Prefer Public Attributes Over Private Ones
"""
- Private attributes aren't rigorously enforced by the Python compiler.
- Plan from the beginning to allow subclasses to do more with your
internal APIs and attributes instead of choosing to lock them out.
- Use documentation of protected fields to guide subclasses instead of
trying to force access control with private attributes.
- Only consider using private attributes to avoid naming conflicts
with subclasses that are out of your control.
"""

# Class attributes can be public or private
class MyObject:
    def __init__(self):
        self.public_field = 5
        self.__private_field = 10
    
    def get_private_field(self):
        return self.__private_field

# Access a public field
foo = MyObject()
assert foo.public_field == 5

# Access a private field (using the method of the containing class)
assert foo.get_private_field() == 10

# Cannot access a private attribute directly from outside of the class
foo.__private_field  # throws an error

# Class methods have access to private attributes
class MyOtherObject:
    def __init__(self):
        self.__private_field = 71
    
    @classmethod
    def get_private_field_of_instance(cls, instance):
        return instance.__private_field

bar = MyOtherObject()
assert MyOtherObject.get_private_field_of_instance(bar) == 71

# Subclasses cannot access private attributes of its parent's class
class MyParentObject:
    def __init__(self):
        self.__private_field = 71

class MyChildObject(MyParentObject):
    def get_private_field(self):
        return self.__private_field

baz = MyChildObject()
baz.get_private_field() # throws an error

# With a bit of trickery, you can access the parent class's private attribute
# because Python converts _MyChildObject__private_field to _MyParentObject__private_field
assert baz._MyParentObject__private_field == 71

# The object's attribute dictionary shows the private attributes stored with the names
# as they appear after the naming transformation
print(baz.__dict__)

# Using private fields to indicate an internal API that shouldn't be 
# accessed (externally or by subclasses) is the wrong approach
class MyStringClass:
    def __init__(self, value):
        self.__value = value
    
    def get_value(self):
        return str(self.__value)
foo = MyStringClass(5)
assert foo.get_value() == '5'

# This creates issues when you want to subclass your class to add new behaviour
class MyIntegerSubclass(MyStringClass):
    def get_value(self):
        return int(self._MyStringClass__value)

foo = MyIntegerSubclass('5')
assert foo.get_value() == 5


class MyBaseClass:
    def __init__(self, value):
        self.__value = value   
    def get_value(self):
        return self.__value

class MyStringClass(MyBaseClass):
    def get_value(self):
        return str(super().get_value()) # Updated

class MyIntegerSubclass(MyStringClass):
    def get_value(self):
        return int(self._MyStringClass__value) # Not updated

foo = MyIntegerSubclass(5)
foo.get_value()  # throws an error

# It's better to use protected attributes that are well documented
class MyStringClass:
    def __init__(self, value):
    # This stores the user-supplied value for the object.
    # It should be coercible to a string. Once assigned in
    # the object it should be treated as immutable.
        self._value = value   
    def get_value(self):
        return self._value

# The only time to use private attributes is if you're worried about naming conflicts in subclasses
class ApiClass:
    def __init__(self):
        self._value = 5

    def get(self):
        return self._value

class Child(ApiClass):
    def __init__(self):
        super().__init__()
        self._value = 'hello' # Conflicts

a = Child()
print(f'{a.get()} and {a._value} should be different')

# Using private attributes prevents this conflict
class ApiClass:
    def __init__(self):
        self.__value = 5 # Double underscore

    def get(self):
        return self.__value # Double underscore

class Child(ApiClass):
    def __init__(self):
        super().__init__()
        self._value = 'hello' # OK!

a = Child()
print(f'{a.get()} and {a._value} are different')

## Item 43: Inherit from collections.abc for Custom Container Types
"""
- Inherit directly from Python's container types (like list or dict) for
simple use cases.
- Beware of the large number of methods required to implement custom
container types correctly.
- Have your custom container types inherit from the interfaces
defined in collections.abc to ensure that your classes match
required interfaces and behaviors.
"""

# Custom list type for counting frequency
class FrequencyList(list):
    def __init__(self, members):
        super().__init__(members)
    def frequency(self):
        counts = {}
        for item in self:
            counts[item] = counts.get(item, 0) + 1
        return counts

foo = FrequencyList(['a', 'b', 'a', 'c', 'b', 'a', 'd'])
print('Length is', len(foo))

foo.pop()
print('After pop:', repr(foo))
print('Frequency:', foo.frequency())

# Object that allows indexing (similar to a list) but isn't a list subclass
class BinaryNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

## Python containers have instance methods that have special names
bar = [1, 2, 3]
bar[0]  # interpreted as bar.__getitem__(0)

# Create a custom implementation of __getitem__
class IndexableNode(BinaryNode):
    def _traverse(self):
        if self.left is not None:
            yield from self.left._traverse()
        yield self
        if self.right is not None:
            yield from self.right._traverse()
    def __getitem__(self, index):
        for i, item in enumerate(self._traverse()):
            if i == index:
                return item.value
        raise IndexError(f'Index {index} is out of range')

tree = IndexableNode(
    10,
    left=IndexableNode(
        5,
        left=IndexableNode(2),
        right=IndexableNode(
            6,
            right=IndexableNode(7))),
    right=IndexableNode(
        15,
        left=IndexableNode(11)))

# Access of binary tree elements is similar to a list now with __getitem__ implementation
print('LRR is', tree.left.right.right.value)
print('Index 0 is', tree[0])
print('Index 1 is', tree[1])
print('11 in the tree?', 11 in tree)
print('17 in the tree?', 17 in tree)
print('Tree is', list(tree))

# Not all sequence semantics are available though
len(tree)  # throws an error because we would require the __len__ special method

# Create the __len__ special method
class SequenceNode(IndexableNode):
    def __len__(self):
        for count, _ in enumerate(self._traverse(), 1):
            pass
        return count

tree = SequenceNode(
    10,
    left=SequenceNode(
        5,
        left=SequenceNode(2),
        right=SequenceNode(
            6,
            right=SequenceNode(7))),
    right=SequenceNode(
        15,
        left=SequenceNode(11))
)

print('Tree length is', len(tree))

# Defining these special methods is cumbersome, especially when they are expected
# Instead, we can use the abstract base classes available in collections.abc
# These provide all of the typical methods for each container type

from collections.abc import Sequence

class BadType(Sequence):
    pass

foo = BadType()  # throws an error because you forgot to implement required methods

# Inheriting SequenceNode gives you the required __getitem__ and __len__ methods
# Additional methods like index and count now come with it for free!
class BetterNode(SequenceNode, Sequence):
    pass

tree = BetterNode(
    10,
    left=BetterNode(
        5,
        left=BetterNode(2),
        right=BetterNode(
            6,
            right=BetterNode(7))),
    right=BetterNode(
        15,
        left=BetterNode(11))
)

print('Index of 7 is', tree.index(7))
print('Count of 10 is', tree.count(10))