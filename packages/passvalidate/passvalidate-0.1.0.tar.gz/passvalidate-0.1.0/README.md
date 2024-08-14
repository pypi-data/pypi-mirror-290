# Configurable Password Policy Checker

This package provides a configurable password policy checker that allows you to set custom requirements for password strength.

## Installation

You can install this package using Poetry:

```
poetry add password-policy
```

## Usage

```python
from password_policy import PasswordPolicy

# Use default policy
default_policy = PasswordPolicy()
result = default_policy.check_password("YourPassword123!")
if result:
    print(result)
else:
    print("Password meets all requirements")

# Use custom policy
custom_policy = PasswordPolicy(
    min_length=10,
    min_uppercase=1,
    min_lowercase=1,
    min_digits=1,
    min_special=1,
    special_chars="!@#$%^&*",
    allow_spaces=True
)
result = custom_policy.check_password("Your Custom Password 1!")
if result:
    print(result)
else:
    print("Password meets all custom requirements")

# Get policy description
print(custom_policy.get_policy_description())
```

## Development

To set up the development environment:

1. Clone the repository
2. Install Poetry if you haven't already: https://python-poetry.org/docs/#installation
3. Run `poetry install` to install dependencies
4. Run `poetry run pytest` to run tests