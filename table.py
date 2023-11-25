from datetime import datetime
class Table:
    # table_num: table number
    # ordered_dishes: a list of all the dishes that a table has ordered (to be updated by customers)
    # uncooked_dishes: a list of dishes that have not been cooked (to be updated by cooks)
    # ready_dishes: a list of dishes that have been cooked and ready to be served (to be updated by cooks)
    # pending_dishes: a list of dishes that has not been served for the table (to be updated by server)
    # feedback: feedback from the customers of a table (to be updated by customers)
    # bill: total bill amount 
    # is_occupied: whether the table is occupied (False) or not (True) (to be updated by server)
    # all_served: "True" if all the dishes for this table have been served or "False" if not 
    # payment_status: if a table has paid their bill (True) or has not paid (False) (to be updated by customers or cashier)
    def __init__ (self, tableID, ordered_dishes=[], uncooked_dishes=None, ready_dishes=None, pending_dishes=None, feedback=None, bill = 0, is_occupied = False, all_served = False, payment_status = False):
        self.time = datetime.now().time()
        self.tableID = tableID
        self.ordered_dishes = ordered_dishes
        self.uncooked_dishes = uncooked_dishes
        self.ready_dishes = ready_dishes
        self.pending_dishes = pending_dishes
        self.feedback = feedback

        for dish in ordered_dishes:
            self.bill += dish.price
       
        self.is_occupied = is_occupied

        if not pending_dishes:
            self.all_served = True

        self.payment_status = payment_status

    def add_order(self, dish):
        self.ordered_dishes.append(dish)

    def add_feedback(self):
        feedback = input("Please enter your feedback for today's dishes and service:")
        self.feedback = feedback 
    
       
    # update_payment_status received is_paid parameter (True if the bill is paid, and False if unpaid)
    def make_payment(self):
        pass

    def display_orders(self):
        pass

    def display_bill(self):
        pass
 



    
   

