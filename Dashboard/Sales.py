import streamlit as st
from datetime import datetime
from DataBase import database
import pandas as pd
import plotly.express as px

cursor = database()
def Sales(start,end):
  
     st.write('Sales Income')
     exp = f"select sum(amount) from business_sales where date between  '{start}' and  '{end}'"
     cursor.execute(exp)
     expenses = cursor.fetchall() 
     st.title(f'₹ {expenses[0][0]} Income')

def s_table_view(start,end):
     table = inc = f"select * from business_sales where date between  '{start}' and  '{end}'"
     cursor.execute(inc)
     income = cursor.fetchall()
     column_name = [description[0] for description in cursor.description]
     df = pd.DataFrame(income, columns=column_name)
     return df

def s_pie_view(start,end):
     query = f"select catagories, sum(amount) as amt from business_sales where e_type = 'Expense' and date between '{start}' and  '{end}' group by catagories"
     cursor.execute(query)
     pie_data = cursor.fetchall()
     column_name = [description[0] for description in cursor.description]
     df = pd.DataFrame(pie_data, columns=column_name)
     fig = px.pie(df,values='amt',names='catagories', title="Expenses Pie chart")
     # pie_fig = fig.show()
     return fig


def s_bar_view_expenses(start,end):
     query = f"select catagories, sum(amount) as amt from business_sales where e_type = 'Expense' and date between '{start}' and  '{end}' group by catagories"
     cursor.execute(query)
     pie_data = cursor.fetchall()
     column_name = [description[0] for description in cursor.description]
     df = pd.DataFrame(pie_data, columns=column_name)
     fig = px.bar(df,x='catagories',y='amt', title="Expenses Pie chart")
     return fig


def s_graph_exp(start,end):
    query = f"SELECT date, SUM(amount) as amt FROM business_sales WHERE e_type = 'Expense' AND date BETWEEN '{start}' AND '{end}' GROUP BY date order by date asc"
    cursor.execute(query)
    line_data = cursor.fetchall()
    column_name = [description[0] for description in cursor.description]
    df = pd.DataFrame(line_data, columns=column_name)
    fig = px.line(df, x='date', y='amt', title="Expenses Line Chart")
    return fig

def StocksReport():
     query = '''
     select p.product_name as product ,(sum(st.packets) - sum(sa.packet)) as total_stocks from product p
     join business_sales sa on sa.item_id = p.id
     join stocks st on st.item_id = p.id
     group by p.product_name
     '''
     cursor.execute(query)
     data = cursor.fetchall()
     column_name = [description[0] for description in cursor.description]
     df = pd.DataFrame(data, columns=column_name)
     return df

