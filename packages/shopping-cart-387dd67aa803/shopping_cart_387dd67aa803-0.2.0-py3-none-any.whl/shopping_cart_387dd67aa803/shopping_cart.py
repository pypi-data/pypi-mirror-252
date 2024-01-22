import requests
import logging
import json

from shopping_cart_387dd67aa803.utils.utilities import (
    round_two_decimals,
    display_float_with_2_decimals,
)


class ShoppingCart:
    _cart: dict

    def __init__(self) -> None:
        self._cart = {}
        self.base_url = "https://equalexperts.github.io/backend-take-home-test-data/"

    def add_to_cart(self, product_name: str, quantity: int) -> dict:
        """
        Will add the product details to the cart.

        Args:
            product_name (str): the name of the product
            quantity (int): how many of the product

        Raises:
            Exception: Exception, when there is an error adding a product to the cart

        Returns:
            dict: object containing the status_code and message
        """

        try:
            if not product_name:
                raise Exception("Please enter a valid product name")

            product_name = product_name.strip()
            response = requests.get(f"{self.base_url}{product_name}.json")
            response = json.loads(response.text)
            product_price = response.get("price")

            # Handle scenario where an existing item is added to the cart
            if self._cart.get(product_name) is not None:
                quantity = quantity + self._cart.get(product_name).get("quantity", 0)
                product_price = round_two_decimals(product_price * quantity)

            self._cart[product_name] = {"quantity": quantity, "price": product_price}

            return {"status_code": 200, "message": "Successfully added item to cart"}

        except Exception as e:
            logging.error(f"error is {e}")
            return {
                "status_code": 500,
                "message": f"Unable to add {product_name} to cart",
            }

    def calculate_state(self) -> str:
        """
        Will display the current state of the shopping cart

        Returns:
            str: A string representing the state of the shopping cart.
            This includes:
            product_name: the name of the product
            quantity: how many of the product
            sub: sum of all the prices of the products
            tax: the tax payable on the sub
            total: the sum of the sub and tax

        """

        cart_state: str = ""
        sub: float = 0
        tax: float = 0
        total: float = 0

        for key, value in self._cart.items():
            quantity = value.get("quantity")
            product_price = value.get("price")
            product_name = key

            cart_state = cart_state + f"Cart contains {quantity} x {product_name} \n"
            sub += product_price

        # Add sub total, tax and total
        tax = round_two_decimals(sub * (12.5 / 100))
        total = round_two_decimals(sub + tax)

        cart_state = (
            cart_state + f"Subtotal = {display_float_with_2_decimals(sub)} \n"
        )  # noqa: E501
        cart_state = cart_state + f"Tax = {display_float_with_2_decimals(tax)} \n"
        cart_state = cart_state + f"Total = {display_float_with_2_decimals(total)}"

        return cart_state
