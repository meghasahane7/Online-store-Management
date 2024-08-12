import streamlit as st 
from userdata import get_user_data, get_order_data, get_orderitem_data, get_orderitem_detail
import pandas as pd 
import asyncio 
import mysql.connector

headerSection = st.container()
mainSection = st.container()
loginSection = st.container()
logOutSection = st.container()

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='cdac',
        database="books"
    )

def user_data_table():
    df = pd.DataFrame(get_user_data())
    return df
    

def add_book_to_db(title, author, price, stock):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = "INSERT INTO book (title, author, price, stock) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (title, author, price, stock))
        conn.commit()
        st.success(f"Book '{title}' by {author} added successfully!")
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
    finally:
        # cursor.close()
        conn.close()

def add_book(title, author, price, stock):
    st.write(f"Debug: title={title}, author={author}, price={price}, stock={stock}")

    if title and author and price and stock:
        st.write("All fields are provided. Proceeding to add book.")
        # price = float(price)
        # stock = float(stock)
        add_book_to_db(title, author, price, stock)
    else:
        st.error("Please provide all the required details: title, author, price, stock and image_url.")

def show_main_page():
    with mainSection:
        st.header('Admin Panel ')
        if st.session_state.get('role') == 'admin':
            user, orders, add_book_tab = st.tabs(['Users', 'Orders', 'Add Book'])

            with add_book_tab:
                st.subheader('Add a New Book')
                title = st.text_input('Book Title')
                author = st.text_input('Author')
                price = st.number_input('Price')
                stock = st.number_input('stock')
                if st.button('Add Book'):
                    add_book(title, author, price, stock)
        else:
            user, orders = st.tabs(['Users', 'Orders'])
        
        # user, orders = st.tabs(['Users', 'orders' ])
        
        with user:
            hide_table_row_index = """
                <style>
                thead tr th:first-child {display:none}
                tbody th {display:none}
                thead tr th: {display:none}
                </style> """
            st.markdown(hide_table_row_index, unsafe_allow_html=True)
            st.subheader('user data display')
            s = user_data_table()
            st.table(s)
            
        with orders:
            st.subheader('order data display')
            hide_table_row_index = """
                <style>
                thead tr th:first-child {display:none}
                tbody th {display:none}
                thead tr th: {display:none}
                </style> """
            st.markdown(hide_table_row_index, unsafe_allow_html=True)
            order_df = pd.DataFrame(get_order_data())
            st.table(order_df)    
            st.subheader('Select the order id you want to get information of')
            ode_id = st.number_input(label="", min_value=1 )
            orderitem_pd = pd.DataFrame(get_orderitem_detail(ode_id))
            st.table(orderitem_pd)


def LoggedOut_Clicked():
    st.session_state['loggedIn'] = False
    
def show_logout_page():
    loginSection.empty();
    with logOutSection:
        st.button ("Log Out", key="logout", on_click=LoggedOut_Clicked)



def LoggedIn_Clicked(email_id, password):

    if email_id == 'admin' and password == 'admin':
        st.session_state['loggedIn'] = True
        st.session_state['role'] = 'admin'
    else:
        st.session_state['loggedIn'] = False
        st.session_state['role'] = None
        st.error("Invalid user name or password")
        
        
        
def show_login_page():
    with loginSection:
        if st.session_state['loggedIn'] == False:
            st.subheader('Login Here 🎉')         
            email_id = st.text_input (label="", value="", placeholder="Enter your user name")
            password = st.text_input (label="", value="",placeholder="Enter password", type="password")
            st.button ("Login", on_click=LoggedIn_Clicked, args= (email_id, password))
        


with headerSection:
    st.title("Online Book Order System  - Admin Login ")
    if 'loggedIn' not in st.session_state:
        st.session_state['loggedIn'] = False
        show_login_page() 
    else:
        if st.session_state['loggedIn']:
            show_logout_page()    
            show_main_page()
        else:
            show_login_page()