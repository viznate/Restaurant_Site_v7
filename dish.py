class Dish:
    # name: the dish name
    # price: the price of the dish
    # is_ready: if the dish is ready to be served (from kitchen) (to be updated by cooks)
    # served: if the dish has been served to customer (to be updated by server)
    def __init__(self,name, price, is_ready = False, is_served = False):
        self.name = name
        self.price = price
        is_ready = is_ready
        is_served = is_served

