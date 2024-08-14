# Regex String Generator

## Overview

**Regex String Generator** is a Python package that allows you to generate random strings that match a given [regular expression](https://docs.python.org/3/library/re.html) pattern.

## Features

## Installation

Install the package using pip:

```shell
pip install regex-string-generator
```

## Use Cases

Create random strings for various purposes such as database seeding, API testing, form validation, or any other scenario where you need controlled random data that adheres to specific formats.

- **Testing**: Generate test data that matches the input validation rules of your application. This ensures your application handles all expected input formats correctly.
- **Validate Regex**: Check the effectiveness of your regex patterns by generating matching strings. This helps you understand if your regex is too broad or too restrictive.
- **Regex Learning Tool**: For those learning regular expressions, this package provides a way to see examples of strings that match specific patterns, helping to reinforce understanding.

## Usage Examples

Here's how you can use the `generate_string` function.

**Example 1: Generate a simple username**

```python
from regex_string_generator import generate_string

username_pattern = r"[a-z]{8}"  # 8 lowercase letters
username = generate_string(username_pattern)
print(f"Generated username: {username}")
# Output: Generated username: abcdefgh
```

**Example 2: Generate a simple password**

```python
from regex_string_generator import generate_string

password_pattern = r"[A-Za-z0-9]{10}"  # 10 alphanumeric characters
password = generate_string(password_pattern)
print(f"Generated password: {password}")
# Output: Generated password: Ab3d5Fg2h9
```

**Example 3: Generate a simple hexadecimal color code**

```python
from regex_string_generator import generate_string

color_pattern = r"#[A-Fa-f0-9]{6}"  # Hex color code
color = generate_string(color_pattern)
print(f"Generated color code: {color}")
# Output: Generated color code: #1A2B3C
```
