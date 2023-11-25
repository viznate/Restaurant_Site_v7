from dish import *
from table import *
from restaurant import *

menu = [
    Dish('Wings', 8.99),
    Dish('Beef Burger', 7.99),
    Dish('Taco', 6.99),
    Dish('Brownie', 3.99),
    Dish('Chicken Salad', 5.99)
      ]

table1 = Table(1)
table2 = Table(2)
table3 = Table(3)

tables = [table1, table2, table3]

restaurant = Restaurant(tables)
