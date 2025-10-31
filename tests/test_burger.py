import pytest
from unittest.mock import Mock
from praktikum.burger import Burger
import constants


class TestBurger:
    """
    Тесты для класса Burger с использованием реальных данных из Stellar Burgers.
    Класс Burger отвечает за сборку бургера, расчет стоимости и формирование рецепта.
    """

    def test_set_buns(self, new_bun):
        """
        Тест установки булки в бургер.
        Проверяет, что булка корректно сохраняется в атрибуте бургера.
        """
        burger = Burger()
        burger.set_buns(new_bun)
        assert burger.bun == new_bun


    def test_add_ingredient(self, new_ingredient):
        """
        Тест добавления ингредиента в бургер.
        Проверяет, что ингредиент добавляется в список ингредиентов бургера.
        """
        burger = Burger()
        burger.add_ingredient(new_ingredient)
        assert new_ingredient in burger.ingredients


    def test_remove_ingredient(self, new_ingredient):
        """
        Тест удаления ингредиента из бургера.
        Проверяет, что ингредиент корректно удаляется из списка по индексу.
        """
        burger = Burger()
        burger.add_ingredient(new_ingredient)
        ingredient_index = burger.ingredients.index(new_ingredient)
        burger.remove_ingredient(ingredient_index)
        assert new_ingredient not in burger.ingredients


    def test_move_ingredient(self, new_burger, new_ingredient):
        """
        Тест перемещения ингредиента в списке.
        Проверяет, что ингредиент корректно перемещается на новую позицию.
        """
        new_burger.add_ingredient(new_ingredient)
        ingredient_index = new_burger.ingredients.index(new_ingredient)
        new_index = ingredient_index - 1
        new_burger.move_ingredient(ingredient_index, new_index)
        assert new_burger.ingredients.index(new_ingredient) == new_index


    def test_get_price(self):
        """
        Тест расчета стоимости бургера.
        Проверяет правильность формулы: цена_булки * 2 + сумма_цен_ингредиентов.
        Использует моки для изоляции теста от реальных объектов.
        """
        bun_price = 1000
        ingredient_price = 500
        
        bun_mock = Mock()
        ingredient_mock = Mock()
        bun_mock.get_price.return_value = bun_price
        ingredient_mock.get_price.return_value = ingredient_price
        
        burger = Burger()
        burger.set_buns(bun_mock)
        burger.add_ingredient(ingredient_mock)
        
        assert burger.get_price() == bun_price * 2 + ingredient_price


    @pytest.mark.parametrize("bun_index, sauce_index, filling_index", [
        (0, 0, 0),  # Краторная булка + Spicy-X + Мясо моллюсков
        (1, 1, 1),  # Флюоресцентная булка + Space Sauce + Говяжий метеорит
        (0, 2, 2),  # Краторная булка + Традиционный + Биокотлета
        (1, 3, 3),  # Флюоресцентная булка + Антарианский + Филе тетраодонтимформа
    ])
    def test_get_price_real_combinations(self, bun_index, sauce_index, filling_index):
        """
        Параметризованный тест расчета стоимости с реальными комбинациями из Stellar Burgers.
        Проверяет правильность расчета на реальных данных меню.
        """
        # Создаем моки с реальными данными
        bun_mock = Mock()
        bun_mock.get_price.return_value = constants.bun_prices[bun_index]
        
        sauce_mock = Mock()
        sauce_mock.get_price.return_value = constants.sauces[sauce_index][1]
        
        filling_mock = Mock()
        filling_mock.get_price.return_value = constants.fillings[filling_index][1]
        
        burger = Burger()
        burger.set_buns(bun_mock)
        burger.add_ingredient(sauce_mock)
        burger.add_ingredient(filling_mock)
        
        # Рассчитываем ожидаемую стоимость
        expected_price = (constants.bun_prices[bun_index] * 2 + 
                         constants.sauces[sauce_index][1] + 
                         constants.fillings[filling_index][1])
        
        assert burger.get_price() == expected_price


    def test_get_receipt_right_bun_in_result(self, new_burger):
        """
        Тест формирования рецепта - проверка отображения названия булки.
        Проверяет, что название булки присутствует в сформированном рецепте.
        """
        receipt = new_burger.get_receipt()
        assert new_burger.bun.get_name() in receipt


    @pytest.mark.parametrize("index", [0, 1])
    def test_get_receipt_right_ingredients_in_result(self, new_burger, index):
        """
        Параметризованный тест формирования рецепта - проверка отображения ингредиентов.
        Проверяет, что названия всех ингредиентов присутствуют в рецепте.
        """
        receipt = new_burger.get_receipt()
        assert new_burger.ingredients[index].get_name() in receipt


    def test_get_receipt_right_price_in_result(self, new_burger):
        """
        Тест формирования рецепта - проверка отображения общей стоимости.
        Проверяет, что рассчитанная стоимость присутствует в рецепте.
        """
        receipt = new_burger.get_receipt()
        burger_price = new_burger.get_price()
        assert str(burger_price) in receipt

    # ДОПОЛНИТЕЛЬНЫЕ ТЕСТЫ С РЕАЛЬНЫМИ ДАННЫМИ

    def test_get_price_krator_bun_with_expensive_ingredients(self):
        """
        Тест расчета стоимости с Краторной булкой и дорогими ингредиентами.
        Проверяет корректность расчета максимальной стоимости.
        """
        bun_mock = Mock()
        bun_mock.get_price.return_value = 1255  # Краторная булка
        
        filling_mock = Mock()
        filling_mock.get_price.return_value = 4400  # Мини-салат Экзо-Плантаго
        
        sauce_mock = Mock()
        sauce_mock.get_price.return_value = 90  # Соус Spicy-X
        
        burger = Burger()
        burger.set_buns(bun_mock)
        burger.add_ingredient(filling_mock)
        burger.add_ingredient(sauce_mock)
        
        # 1255*2 + 4400 + 90 = 1255*2 + 4490 = 2510 + 4490 = 7000
        assert burger.get_price() == 7000


    def test_get_price_fluorescent_bun_with_cheap_ingredients(self):
        """
        Тест расчета стоимости с Флюоресцентной булкой и бюджетными ингредиентами.
        Проверяет корректность расчета минимальной стоимости.
        """
        bun_mock = Mock()
        bun_mock.get_price.return_value = 988  # Флюоресцентная булка
        
        filling_mock = Mock()
        filling_mock.get_price.return_value = 300  # Хрустящие минеральные кольца
        
        sauce_mock = Mock()
        sauce_mock.get_price.return_value = 15  # Соус традиционный галактический
        
        burger = Burger()
        burger.set_buns(bun_mock)
        burger.add_ingredient(filling_mock)
        burger.add_ingredient(sauce_mock)
        
        # 988*2 + 300 + 15 = 1976 + 315 = 2291
        assert burger.get_price() == 2291


    def test_move_ingredient_to_same_position(self):
        """
        Тест перемещения ингредиента на ту же позицию.
        Проверяет, что порядок не меняется при перемещении на текущую позицию.
        """
        burger = Burger()
        
        ingredient1 = Mock()
        ingredient2 = Mock()
        ingredient3 = Mock()
        
        burger.add_ingredient(ingredient1)
        burger.add_ingredient(ingredient2)
        burger.add_ingredient(ingredient3)
        
        original_order = burger.ingredients.copy()
        burger.move_ingredient(1, 1)
        assert burger.ingredients == original_order