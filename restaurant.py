class Restaurant:
    # tables: a list of tables that have placed orders in the restaurant
    # revenue: total earnings from all tables 
    # dish_sales: a dictionary with dish names as keys and the number of times each dish has been sold as values

    def __init__(self, revenue=0, dish_sellers=None,tables=[]):
        self.table = tables
        self.revenue = revenue
        self.dish_sellers = dish_sellers

    # return table instance based on table number:
    def get_table(self, table_number):
        for table in self.tables:
            if table.tableID == table_number:
                return table
        return None
    
    # use dictionary to display each table's service status
    def display_service_status(self):
        pass

    # return the best seller during a specified timeframe
    def best_seller(self):
        pass

    # use dictionary to display table availiblity in restaurant
    def display_table_availability(self):
        pass


    