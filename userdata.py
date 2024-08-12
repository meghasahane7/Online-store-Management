import mysql.connector
import itertools
import streamlit as st 
def connect_to_database():
  try:
    db = mysql.connector.connect(
        host='localhost',
        user='root',
        password='cdac',
        database="books"
)
    return db
  except mysql.connector.Error as err:
    print("Error connecting to database:", err)
    return None
db=connect_to_database()
bk = db.cursor() 
def login(email, password):
    bk.execute(f"SELECT password FROM users WHERE email = '{email}'")
    detail = bk.fetchall()
    # for i in detail:
    try :
        passw = detail[0][0]
        if passw == password:
            return True
        else:
            return False
    except:
        return False
    
def get_books_from_db():
    db=connect_to_database() 
    if db:
        try:
            bk = db.cursor()
        
            bk.execute("SELECT title, author, price FROM book")
            books = bk.fetchall()
            return books
        except mysql.connector.Error as err:
            st.error(f"Error: {err}")
        # return []
        finally:
            bk.close()
    else:
        return None
    
def signup(email, name, address ,phnumber,sign_password):
    pz = ''
    bk.execute(f"INSERT INTO users (user_id,email, name, password, address, phonenumber) VALUES (DEFAULT, '{email}','{name}', '{sign_password}', '{address}', '{phnumber}')")
    db.commit()
    return True

def get_details(email):
    bk.execute(f"SELECT user_id, name, address, phonenumber, email FROM users WHERE email = '{email}'")
    details = bk.fetchall()
    return [details[0][0], details[0][1], details[0][2], details[0][3], details[0][4]]
    
def place_order(user_id, total_amt, paymentmethod ,book_list, qty_list):
    try :
        bk.execute(f"INSERT INTO orders( user_id, ordertotal, paymentmethod) VALUES ( '{user_id}', '{total_amt}', '{paymentmethod}') " )
        bk.execute("SELECT LAST_INSERT_ID()")
        order_idd= bk.fetchone()[0]
        
        for (book, qty) in zip(book_list, qty_list):
            bk.execute(f"INSERT INTO orderitems ( order_id, item_name, quantity ) VALUES ('{order_idd}', '{book}', '{qty}')")
        db.commit()
        return True
    except:
        return False
    
def get_user_data():
    bk.execute("SELECT user_id, email, name, address, phonenumber FROM users")
    details = bk.fetchall() 
    detail_dict = {'User Id': [i[0] for i in details ],
                   'Email Id' : [i[1] for i in details],
                   'Name' :[i[2] for i in details],
                   'Address':[i[3] for i in details],
                   'Phone Number' : [i[4] for i in details]}
    return detail_dict

    
def get_order_data():
    bk.execute("SELECT * FROM orders")
    details = bk.fetchall()
    details_dict = {'Order Id':[i[0] for i in details],
                  'User Id': [i[1] for i in details],
                  'Total Amount' :[i[2] for i in details],
                  'Payment Method':[i[3] for i in details]}
    return details_dict

def get_orderitem_data():
    bk.execute("SELECT * FROM orderitems")
    details = bk.fetchall()
    details_dict = {'order_id' : [i[0] for i in details],
                    'Book Item' : [i[1] for i in details],
                    'QTY':[i[2] for i in details]}
    return details_dict

def update_details(user_id, email, name ,address, number):
    bk.execute(f"UPDATE users SET email = '{email}', name ='{name}', address ='{address}', phonenumber = '{number}' WHERE user_id ={user_id} ")
    db.commit()
    return True

def update_password(user_id, password):
    bk.execute(f"UPDATE users SET password ='{password}' WHERE user_id={user_id} ")
    db.commit()
    return True

def get_orderitem_detail(order_id):
    bk.execute(f"SELECT * FROM orderitems WHERE order_id = '{order_id}'")
    details = bk.fetchall()
    detail_dict = {'order_id' : [i[0] for i in details],
                    'Book Item' : [i[1] for i in details],
                    'QTY':[i[2] for i in details]}
    return detail_dict

def delete_user(user_id):
    bk.execute("SET FOREIGN_KEY_CHECKS=0")
    bk.execute(f"DELETE users, orders, orderitems FROM users INNER JOIN orders ON users.user_id = orders.user_id INNER JOIN orderitems on orders.order_id = orderitems.order_id  WHERE users.user_id ={user_id}")
    db.commit()
