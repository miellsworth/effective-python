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
