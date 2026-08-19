from unittest.mock import Mock
import pytest
from praktikum.burger import Burger


def test_burger_initialization():
    burger = Burger()

    assert burger.bun is None
    assert burger.ingredients == []


def test_set_buns():
    burger = Burger()
    bun = object()

    burger.set_buns(bun)

    assert burger.bun is bun


def test_add_ingredient():
    burger = Burger()
    ingredient = object()

    burger.add_ingredient(ingredient)

    assert burger.ingredients == [ingredient]


def test_remove_ingredient():
    burger = Burger()
    ingredient_1 = object()
    ingredient_2 = object()

    burger.add_ingredient(ingredient_1)
    burger.add_ingredient(ingredient_2)

    burger.remove_ingredient(0)

    assert burger.ingredients == [ingredient_2]


def test_move_ingredient():
    burger = Burger()
    ingredient_1 = object()
    ingredient_2 = object()
    ingredient_3 = object()

    burger.add_ingredient(ingredient_1)
    burger.add_ingredient(ingredient_2)
    burger.add_ingredient(ingredient_3)

    burger.move_ingredient(0, 2)

    assert burger.ingredients == [
        ingredient_2,
        ingredient_3,
        ingredient_1,
    ]


@pytest.mark.parametrize(
    "bun_price, ingredient_prices, expected_price",
    [
        (100, [], 200),
        (100, [50], 250),
        (200, [50, 75], 525),
        (300, [100, 200, 50], 950),
    ],
)
def test_get_price(bun_price, ingredient_prices, expected_price):
    burger = Burger()

    bun = Mock()
    bun.get_price.return_value = bun_price
    burger.set_buns(bun)

    for price in ingredient_prices:
        ingredient = Mock()
        ingredient.get_price.return_value = price
        burger.add_ingredient(ingredient)

    assert burger.get_price() == expected_price


def test_get_receipt():
    burger = Burger()

    bun = Mock()
    bun.get_name.return_value = "Black bun"
    bun.get_price.return_value = 100
    burger.set_buns(bun)

    sauce = Mock()
    sauce.get_type.return_value = "SAUCE"
    sauce.get_name.return_value = "Hot sauce"
    sauce.get_price.return_value = 50

    filling = Mock()
    filling.get_type.return_value = "FILLING"
    filling.get_name.return_value = "Cutlet"
    filling.get_price.return_value = 100

    burger.add_ingredient(sauce)
    burger.add_ingredient(filling)

    receipt = burger.get_receipt()

    expected_receipt = (
        "(==== Black bun ====)\n"
        "= sauce Hot sauce =\n"
        "= filling Cutlet =\n"
        "(==== Black bun ====)\n"
        "\n"
        "Price: 350"
    )

    assert receipt == expected_receipt