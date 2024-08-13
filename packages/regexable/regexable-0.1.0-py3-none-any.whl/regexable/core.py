# regexable/core.py - The main module containing the Regexable class.

import re

class Regexable:
    def __init__(self):
        """
        Initializes a new instance of the Regexable class with an empty pattern.
        """
        self.pattern: str = ""

    def start_of_line(self) -> 'Regexable':
        """
        Appends the start-of-line anchor (^) to the pattern.
        
        Returns:
            Regexable: The instance of Regexable to allow method chaining.
        """
        self.pattern = "^" + self.pattern
        return self

    def end_of_line(self) -> 'Regexable':
        """
        Appends the end-of-line anchor ($) to the pattern.
        
        Returns:
            Regexable: The instance of Regexable to allow method chaining.
        """
        self.pattern += "$"
        return self

    def then(self, text: str) -> 'Regexable':
        """
        Appends the given text to the pattern, escaping any special characters.
        
        Args:
            text (str): The text to append to the pattern.
        
        Returns:
            Regexable: The instance of Regexable to allow method chaining.
        """
        self.pattern += re.escape(text)
        return self

    def maybe(self, text: str) -> 'Regexable':
        """
        Appends an optional (zero or one) occurrence of the given text to the pattern.
        
        Args:
            text (str): The text to append to the pattern optionally.
        
        Returns:
            Regexable: The instance of Regexable to allow method chaining.
        """
        self.pattern += f"({re.escape(text)})?"
        return self

    def anything(self) -> 'Regexable':
        """
        Appends a wildcard pattern that matches any character zero or more times (.*).
        
        Returns:
            Regexable: The instance of Regexable to allow method chaining.
        """
        self.pattern += ".*"
        return self

    def anything_but(self, text: str) -> 'Regexable':
        """
        Appends a pattern that matches any character except the specified text one or more times.
        
        Args:
            text (str): The text that should not be matched.
        
        Returns:
            Regexable: The instance of Regexable to allow method chaining.
        """
        self.pattern += f"[^{re.escape(text)}]+"
        return self

    def something(self) -> 'Regexable':
        """
        Appends a wildcard pattern that matches any character one or more times (.+).
        
        Returns:
            Regexable: The instance of Regexable to allow method chaining.
        """
        self.pattern += ".+"
        return self

    def something_but(self, text: str) -> 'Regexable':
        """
        Appends a pattern that matches any character except the specified text one or more times.
        
        Args:
            text (str): The text that should not be matched.
        
        Returns:
            Regexable: The instance of Regexable to allow method chaining.
        """
        self.pattern += f"[^{re.escape(text)}]+"
        return self

    def digit(self) -> 'Regexable':
        """
        Appends a pattern that matches any digit (\\d).
        
        Returns:
            Regexable: The instance of Regexable to allow method chaining.
        """
        self.pattern += r"\d"
        return self

    def whitespace(self) -> 'Regexable':
        """
        Appends a pattern that matches any whitespace character (\\s).
        
        Returns:
            Regexable: The instance of Regexable to allow method chaining.
        """
        self.pattern += r"\s"
        return self

    def tab(self) -> 'Regexable':
        """
        Appends a pattern that matches a tab character (\\t).
        
        Returns:
            Regexable: The instance of Regexable to allow method chaining.
        """
        self.pattern += r"\t"
        return self

    def newline(self) -> 'Regexable':
        """
        Appends a pattern that matches a newline character (\\n).
        
        Returns:
            Regexable: The instance of Regexable to allow method chaining.
        """
        self.pattern += r"\n"
        return self

    def word(self) -> 'Regexable':
        """
        Appends a pattern that matches any word character (\\w).
        
        Returns:
            Regexable: The instance of Regexable to allow method chaining.
        """
        self.pattern += r"\w"
        return self

    def build(self) -> re.Pattern:
        """
        Compiles the current pattern into a regular expression object.
        
        Returns:
            re.Pattern: The compiled regular expression pattern.
        """
        return re.compile(self.pattern)

    def match(self, text: str) -> re.Match | None:
        """
        Attempts to match the compiled pattern against the given text.
        
        Args:
            text (str): The text to match against the pattern.
        
        Returns:
            re.Match | None: The match object if the text matches the pattern; otherwise, None.
        """
        return re.match(self.pattern, text)

    def ignore_case(self) -> 'Regexable':
        """
        Appends a flag to the pattern to ignore case sensitivity (?i).
        
        Returns:
            Regexable: The instance of Regexable to allow method chaining.
        """
        self.pattern = f"(?i){self.pattern}"
        return self

    def multiline(self) -> 'Regexable':
        """
        Appends a flag to the pattern to treat the target as multiline (?m).
        
        Returns:
            Regexable: The instance of Regexable to allow method chaining.
        """
        self.pattern = f"(?m){self.pattern}"
        return self

    def word_boundary(self) -> 'Regexable':
        """
        Appends a pattern that matches a word boundary (\\b).
        
        Returns:
            Regexable: The instance of Regexable to allow method chaining.
        """
        self.pattern += r"\b"
        return self

    def not_word_boundary(self) -> 'Regexable':
        """
        Appends a pattern that matches a non-word boundary (\\B).
        
        Returns:
            Regexable: The instance of Regexable to allow method chaining.
        """
        self.pattern += r"\B"
        return self

    def zero_or_more(self) -> 'Regexable':
        """
        Appends a quantifier that matches the preceding element zero or more times (*).
        
        Returns:
            Regexable: The instance of Regexable to allow method chaining.
        """
        self.pattern += "*"
        return self

    def one_or_more(self) -> 'Regexable':
        """
        Appends a quantifier that matches the preceding element one or more times (+).
        
        Returns:
            Regexable: The instance of Regexable to allow method chaining.
        """
        self.pattern += "+"
        return self

    def exactly(self, n: int) -> 'Regexable':
        """
        Appends a quantifier that matches the preceding element exactly n times ({n}).
        
        Args:
            n (int): The exact number of times to match the preceding element.
        
        Returns:
            Regexable: The instance of Regexable to allow method chaining.
        """
        self.pattern += f"{{{n}}}"
        return self

    def at_least(self, n: int) -> 'Regexable':
        """
        Appends a quantifier that matches the preceding element at least n times ({n,}).
        
        Args:
            n (int): The minimum number of times to match the preceding element.
        
        Returns:
            Regexable: The instance of Regexable to allow method chaining.
        """
        self.pattern += f"{{{n},}}"
        return self

    def between(self, m: int, n: int) -> 'Regexable':
        """
        Appends a quantifier that matches the preceding element between m and n times ({m,n}).
        
        Args:
            m (int): The minimum number of times to match the preceding element.
            n (int): The maximum number of times to match the preceding element.
        
        Returns:
            Regexable: The instance of Regexable to allow method chaining.
        """
        self.pattern += f"{{{m},{n}}}"
        return self

    def group(self, pattern: str) -> 'Regexable':
        """
        Appends a group pattern to the current pattern.
        
        Args:
            pattern (str): The pattern to be grouped.
        
        Returns:
            Regexable: The instance of Regexable to allow method chaining.
        """
        self.pattern += f"({pattern})"
        return self

    def or_(self, pattern: str) -> 'Regexable':
        """
        Appends an alternative pattern (OR) to the current pattern.
        
        Args:
            pattern (str): The alternative pattern.
        
        Returns:
            Regexable: The instance of Regexable to allow method chaining.
        """
        self.pattern += f"|({pattern})"
        return self

    def range(self, char1: str, char2: str) -> 'Regexable':
        """
        Appends a character range pattern to the current pattern.
        
        Args:
            char1 (str): The start character of the range.
            char2 (str): The end character of the range.
        
        Returns:
            Regexable: The instance of Regexable to allow method chaining.
        """
        self.pattern += f"[{char1}-{char2}]"
        return self
