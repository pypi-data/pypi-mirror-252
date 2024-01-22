## Code style

This project makes use of black with default settings to format the code
and flake8 as a linter.

## Usage

```
from shopping_cart.shopping_cart import ShoppingCart

cart: ShoppingCart = ShoppingCart()
print(cart.add_to_cart("cornflakes", 1))
print(cart.add_to_cart("cornflakes", 1))
print(cart.add_to_cart("weetabix", 1))
print(cart.calculate_state())
```

![Alt text](image.png)

## API

`add_to_cart(product_name, quantity)`

Will add the product details to the cart.

Args:   
product_name (str): the name of the product  
quantity (int): how many of the product

Raises: Exception: Exception, when there is an error adding a product to the cart

Returns: dict: object containing the status_code and message

`calculate_state()`

Will display the current state of the shopping cart

Returns: str:   
A string representing the state of the shopping cart. 
This includes:   
product_name: the name of the product   
quantity: how many of the product   
sub: sum of all the prices of the products   
tax: the tax payable on the sub   
total: the sum of the sub and tax  

# Requirements
* python >= 3.10
* poetry
* coverage

# Testing

The project uses pytest to run its tests
To run the tests, follow the steps below.

Open up a terminal in the project

1. run `poetry install` this will install the dependencies for the project
2. run `poetry shell` to enter the virtual environment
3. run `poetry run pytest -vv` to run the tests

# Coverage

Open up a terminal in the project

1. run `coverage run -m pytest` run the test suite and get data
2. run `coverage report -m` to get a report of the results

![Alt text](image-1.png)

# Other
The .gitignore file was generated using gitignore.io
https://www.toptal.com/developers/gitignore/#