from flask import Flask, render_template, request, url_for, redirect
from data import *
from flask_sqlalchemy import SQLAlchemy
import csv


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class DiningTable(db.Model):
    __tablename__= 'dining_table'
    tableNum = db.Column(db.Integer, primary_key = True)
    orders = db.relationship('DiningOrders',backref = 'table') # Each instance of the Order model will have an attribute named 'table'. eg. order1.table
    is_occupied = db.Column(db.Boolean)
    is_paid = db.Column(db.Boolean, default = False)
    bill_amount = db.Column(db.Float, default = 0.0)

    def __repr__(self):
        if self.is_occupied:
            return f"{self.tableNum}: occupied"
        return f"{self.tableNum}: available"

class DiningOrders(db.Model):
    __tablename__ = 'dining_orders'
    id = db.Column(db.Integer, primary_key = True)
    tableNum = db.Column(db.Integer, db.ForeignKey('dining_table.tableNum'))
    # 'db.ForeignKey' is used to create a many-to-one relationship. 
    # It refers to a field in another database and is used to establish a link between two database
    # each instance of Order can be associated with one instance of Table
    # a ForeignKey is represented as a column that contains the primary key of another table (database)
    dishes = db.relationship('OrderedDish', backref = 'order')
    # Each instance of the OrderedDish model will have an attribute named order. eg. Burger.order
    bill_amount = db.Column(db.Float, default = 0.0)


class OrderedDish(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30))
    order_id = db.Column(db.Integer, db.ForeignKey('dining_orders.id'))  
    quantity = db.Column(db.Integer, default = 0)
    price = db.Column(db.Float, default = 0.0)
    is_served = db.Column(db.Boolean)

 
with app.app_context():
   
    db.create_all()
    
    if DiningTable.query.first() is None: # retrieve the first row from the dining_table table in the database.
    # Create new table instances
       
        table1 = DiningTable(tableNum=1, is_occupied=False)
        table2 = DiningTable(tableNum=2, is_occupied=False)
        table3 = DiningTable(tableNum=3, is_occupied=False)

        db.session.add(table1)
        db.session.add(table2)
        db.session.add(table3)
        db.session.commit()

    
  
# Initialize some sample data for the buttons
button_data = {
    "button1": [
        {"text": "Menu", "url": "/menu"}, 
        {"text": "Leave Feedback", "url": "/leave_feedback"},
        {"text": "Track Order", "url": "/track_order"}
    ],
    "button2": [
        {"text": "Server", "url": "/serverlogin"},
        {"text": "Cashier", "url": "/cashierlogin"},
        {"text": "Manager", "url": "/managerlogin"}
    ],
}

feedback_data = []

@app.route('/')
def home():
    return render_template('index.html', button_data=button_data)


@app.route('/menu', methods=['GET', 'POST'])
def place_order():
    new_order = None
    selected_table = None
    selected_dishes = {}
    total_bill_amount = 0

    if request.method == 'POST':
        if 'tables' in request.form: # menu.html has two buttons, one for tables, the other for place orders; this one is to handle the "tables" submit button
            selected_table = request.form.get('tables') 
            selected_table_num = int(selected_table)
            
            table = DiningTable.query.filter_by(tableNum=selected_table_num).first()   
            # .first() retrieves the first DiningTable object where tableNum equals selected_table_num, or None if no such object exists.
            if table:
                table.is_occupied = True
                table.is_paid= False
                db.session.commit()
               
                order = DiningOrders(tableNum=selected_table_num)
                db.session.add(order) 
                db.session.commit()   
                process_order = True  # Set to True only if table processing succeeds
       
       
   
        new_order = DiningOrders.query.order_by(DiningOrders.id.desc()).first() # query the new order
        for dish in menu: # Here 'menu' is a list of Dish instances, imported from data.py
            if dish.name in request.form:
                quantity = int(request.form[dish.name])
                if quantity:  # Check if a quantity was entered
                    selected_dishes[dish] = quantity
                    total_bill_amount += dish.price * quantity
                    new_order.bill_amount = total_bill_amount
                    ordered_dishes=OrderedDish(name=dish.name, quantity=quantity, order_id = new_order.id, price = dish.price)
                    db.session.add(ordered_dishes)
                    db.session.commit()     

                    # write order information to csv file
                    orders = DiningOrders.query.all()
                    dishes = OrderedDish.query.all()
                    csv_file_path = 'orders.csv'
                    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
                        writer = csv.writer(file)
                        writer.writerow(['Order ID','Dish Name','Quantity', 'Selling($)'])
                        for dish in dishes:
                            writer.writerow([dish.order_id, dish.name, dish.quantity, dish.price*dish.quantity])
       

    return render_template('menu.html', menu=menu, selected_table=selected_table, selected_dishes=selected_dishes, total_bill = total_bill_amount)




@app.route('/serverlogin', methods = ['GET', 'POST'])
def server_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        return redirect('/server')
    return render_template('server_login.html')
         

@app.route('/server', methods = ['GET', 'POST']) 
def server():
    
    table1 = DiningTable.query.filter_by(tableNum=1).first()
    table2 = DiningTable.query.filter_by(tableNum=2).first()
    table3 = DiningTable.query.filter_by(tableNum=3).first()
    new_order_table1 = DiningOrders.query.filter_by(tableNum=1).order_by(DiningOrders.id.desc()).first() # query the new order from Table1
    new_order_table2 = DiningOrders.query.filter_by(tableNum=2).order_by(DiningOrders.id.desc()).first() # query the new order from Table2
    new_order_table3 = DiningOrders.query.filter_by(tableNum=3).order_by(DiningOrders.id.desc()).first() # query the new order from Table3
    
    if table1.is_occupied:
        table1_status = "occupied"
    else:
        table1_status = "available"

    if table2.is_occupied:
        table2_status = "occupied"
    else:
        table2_status = "available"

    if table3.is_occupied:
        table3_status = "occupied"
    else:
        table3_status = "available"

    if 'table1_status' in request.form:
        table1_status = request.form.get('table1_status') 
        if table1_status == "occupied":
            table1.is_occupied = True
        elif table1_status == "available":
            table1.is_occupied = False
    
    if 'table2_status' in request.form:
        table2_status = request.form.get('table2_status')
        if table2_status == "occupied":
            table2.is_occupied = True
        elif table2_status == "available":
            table2.is_occupied = False
             
    if 'table3_status' in request.form:
        table3_status = request.form.get('table3_status') 
        if table3_status == "occupied":
            table3.is_occupied = True
        elif table3_status == "available":
            table3.is_occupied = False
    db.session.commit() # Commit the changes to the database
    return render_template('server.html', table1_status = table1_status, table2_status=table2_status, table3_status= table3_status, table1_order = new_order_table1, table2_order = new_order_table2, table3_order = new_order_table3)



@app.route('/cashierlogin', methods = ['GET', 'POST'])
def cashier_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        return redirect('/cashier')
    return render_template('cashier_login.html')

@app.route('/cashier', methods=['GET', 'POST']) 
def cashier():
    table1 = DiningTable.query.filter_by(tableNum=1).first()
    table2 = DiningTable.query.filter_by(tableNum=2).first()
    table3 = DiningTable.query.filter_by(tableNum=3).first()
    new_order_table1 = DiningOrders.query.filter_by(tableNum=1).order_by(DiningOrders.id.desc()).first() # query the new order from Table1
    new_order_table2 = DiningOrders.query.filter_by(tableNum=2).order_by(DiningOrders.id.desc()).first() # query the new order from Table2
    new_order_table3 = DiningOrders.query.filter_by(tableNum=3).order_by(DiningOrders.id.desc()).first() # query the new order from Table3

    if new_order_table1 is not None:
        table1_bill = new_order_table1.bill_amount
    else:
        table1_bill = 0.0

    if new_order_table2 is not None:
        table2_bill = new_order_table2.bill_amount
    else:
        table2_bill = 0.0

    if new_order_table3 is not None:
        table3_bill = new_order_table3.bill_amount
    else:
        table3_bill = 0.0
        
    if table1.is_paid:
        table1_is_paid = "paid"
    else:
        table1_is_paid = "unpaid"

    if table2.is_paid:
        table2_is_paid = "paid"
    else:
        table2_is_paid = "unpaid"

    if table3.is_paid:
        table3_is_paid = "paid"
    else:
        table3_is_paid = "unpaid"

    if request.method == 'POST':
        if 'pay_table1' in request.form:
            table1.is_paid = True
            table1_is_paid = "paid"
        db.session.commit() # Commit the changes to the database
        if 'pay_table2' in request.form:
            table2.is_paid = True
            table2_is_paid = "paid"
        db.session.commit() # Commit the changes to the database        
        if 'pay_table3' in request.form:
            table3.is_paid = True
            table3_is_paid = "paid"
        db.session.commit() # Commit the changes to the database

    return render_template('cashier.html', table1_bill = table1_bill, table2_bill = table2_bill, table3_bill = table3_bill, table1_is_paid = table1_is_paid, table2_is_paid = table2_is_paid, table3_is_paid = table3_is_paid, table1_order = new_order_table1, table2_order = new_order_table2, table3_order = new_order_table3)


@app.route('/managerlogin', methods = ['GET', 'POST'])
def manager_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        return redirect('/manager')
    return render_template('manager_login.html')


@app.route('/manager', methods=['GET', 'POST'])
def manager():
    if request.method == 'POST':
        if 'table_status' in request.form:
            return redirect('/table_status')
        elif 'order_list' in request.form:
            return redirect('/order_list')

    if 'view_feedback' in request.args:
        return redirect('/leave_feedback')

    return render_template('manager.html')

@app.route('/table_status')
def display_tables():
    tables = DiningTable.query.all()
    return render_template('table_status.html', tables = tables)

@app.route('/order_list')
def display_orders():
    orders = DiningOrders.query.all()
    dishes = OrderedDish.query.all()
    total_income =0
    for order in orders:
        total_income += order.bill_amount
        total_income = round(total_income, 2)

    
    return render_template('order_list.html', orders = orders, dishes = dishes, total_income = total_income)



@app.route('/leave_feedback', methods=['GET', 'POST'])
def leave_feedback():
    if request.method == 'POST':
        name = request.form['name']
        comment = request.form['comment']
        feedback_data.append({"name": name, "comment": comment})
    return render_template('leave_feedback.html', feedback_data=feedback_data)


@app.route('/track_order')
def track_order():
    # Assume you have some order information here
    order_status = "In Transit"  # Replace this with your actual order status
    estimated_delivery_date = "SOON!"  # Replace this with your actual estimated delivery date

    # Render the template with order information
    return render_template('track_order.html', order_status=order_status, estimated_delivery_date=estimated_delivery_date)


if __name__ == '__main__':
    app.run(debug=True)
