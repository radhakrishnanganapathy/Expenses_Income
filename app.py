import streamlit as st
import psycopg2 as psc
from datetime import datetime
from psycopg2 import extensions
from Dashboard.Home import Home, table_view, pie_view, pie_view_income,bar_view_income,bar_view_expenses,bar_view_inc_exp,graph_inc
from Dashboard.Business import Business, b_table_view, b_pie_view,b_bar_view_expenses,b_graph_exp
from Dashboard.Sales import Sales,StocksReport

db_params = {
    "dbname": "rkrish_db",
    "user": "radhakrishnan",
    "password": "weJyKwjSj60UNzr4MXIEZ79FV7sf2ZHY",
    "host": "dpg-coiuro5jm4es739v1hvg-a.oregon-postgres.render.com",
    "port": "5432"  # Default PostgreSQL port is 5432
}
# db_params = " postgresql://radhakrishnan:weJyKwjSj60UNzr4MXIEZ79FV7sf2ZHY@dpg-coiuro5jm4es739v1hvg-a.oregon-postgres.render.com/rkrish_db"
dsn = extensions.make_dsn(**db_params)
conn = psc.connect(dsn)
cursor = conn.cursor()

st.header("Income and Expenses Manager")

tab1, tab2, tab3,tab4,tab5 = st.tabs(['Dashboard','Home','Business','Production','Stocks'])

with tab1:
     st.title("Data Analysis Report")
     date = st.radio('',['This Month','custom date'])
     if date == 'This Month':
          end = datetime.today().date()
          start = datetime(end.year, end.month, 1).date()
     else:
          start = st.date_input('start Date')
          end = st.date_input('end Date')
     st.write(start, end)
     d_tab1, d_tab2, d_tab3,d_tab4 = st.tabs(['Home','Business','Production','Stocks'])
     
     with d_tab1:
          Home(start,end)
          view_type = ['table','pie','bar','graph']
          view = st.selectbox('view type',view_type)
          if view == 'table':
               st.write(table_view(start,end))
          elif view == 'pie':
               inc_exp = st.radio('',['Income','expenses'])
               if inc_exp == 'expenses':
                    st.title("Expenses pie Chart")
                    pie_fig = pie_view(start,end)
                    st.plotly_chart(pie_fig)
               else:
                    st.title("Income pie Chart")
                    pie_fig = pie_view_income(start,end)
                    st.plotly_chart(pie_fig)
               # st.write(pie_view())
          elif view == 'bar':
               type = st.radio('',['Income','Expenses','Both'])
               if type == 'Income':
                    st.title("Income bar Chart")
                    pie_fig = bar_view_income(start,end)
                    st.plotly_chart(pie_fig)
               elif type == 'Expenses':
                    st.title("Expenses Bar Graph")
                    pie_fig = bar_view_expenses(start,end)
                    st.plotly_chart(pie_fig)
               else:
                    st.title("Both Bar Graph")
                    pie_fig = bar_view_inc_exp(start,end)
                    st.plotly_chart(pie_fig)
          else:
               st.title("Line graph")
               line_fig = graph_inc(start,end)
               st.plotly_chart(line_fig)
     # elif select_option == 'Business':
     with d_tab2:
          type_selection = st.radio('',['Goods','Sales'])
          if type_selection == 'Goods':
               Business(start,end)
               view_type = ['table','pie','bar','graph']
               view = st.selectbox('Business view type',view_type)
               if view == 'table':
                    st.write(b_table_view(start,end))
               elif view == 'pie':
                    st.title("Expenses pie Chart")
                    pie_fig = b_pie_view(start,end)
                    st.plotly_chart(pie_fig)
               elif view == 'bar':
                    st.title("Expense bar Chart")
                    pie_fig = b_bar_view_expenses(start,end)
                    st.plotly_chart(pie_fig)
               else:
                    st.title("Line graph")
                    line_fig = b_graph_exp(start,end)
                    st.plotly_chart(line_fig)
          else:
               Sales(start,end)
               st.title('Balance Stocks')
               st.write(StocksReport())
               view_type = ['table','pie','bar','graph']
               view = st.selectbox('Sales view type',view_type)

with tab2:
     h_type = ['Income','Expense']
     type = st.selectbox('Hone - Income/Expenses',h_type)
     date = st.date_input('Home - Date')
     h_catagories = ['Salary','EMI/Loan','Petrol/travel','Vegetables/Fruits','Groceries','Bills','Health','Functions','Festivals','Maintenance','Purchase']
     h_sub_catagories = [
          'Tvs','Ntarq','Passion','Bus',
          'Ind Bank','Uco','Sangam','Direct Person',
          'Vegetables','Fruits',
          'Cleaning','Food Items',
          'TV','Mobile RC','News Paper','EB','Milk',
          'Medicine','Hospital',
          'Marriage','House Warm',
          'Rk','KK','Usha','kRG'
     ]
     cat = st.selectbox('H-Catagories',h_catagories)
     sub_cat = st.selectbox('H-Sub-Catagories',h_sub_catagories)
     # st.text_input('H-Custome')
     desc = st.text_area("H-Description")
     amt = st.number_input("H-Amount")
     
     if st.button('H-Save'):
          parms = (type,date,cat,sub_cat,desc,amt)
          # query = f"insert into expanses (e_type,date,catagories,sub_catagories,description,ammount) values (?,?,?,?,?,?)"
          query = "INSERT INTO expanses (e_type, date, catagories, sub_catagories, description, ammount) VALUES (%s,%s,%s,%s,%s,%s)"  # Assuming you're using parameterized queries to prevent SQL injection
          cursor.execute(query, parms)
          conn.commit()
          st.write('Inserted')
with tab3:
     b_types = ['Income','Expense']
     b_type = st.selectbox('type',b_types)
     p_date=st.date_input('Dates')
     option = st.radio('Purshase/Sale',['Purchase','Sale'])
     if option == 'Purchase':
          b_catagories = ['Rice','Rice Power','Vegetables','Oil','Gas','Groceries','Packing Covers','Rice Mill']
          b_cat = st.selectbox('B-Catagories',b_catagories)
          b_quantity = st.number_input('B-Quantity')
          b_unit = ['','kg','lt','g']
          b_units = st.selectbox('B-unit',b_unit)
          customer = st.text_input('B-Customer')
          desc = st.text_area("B-Description")
          amt = st.number_input("B-Amount")
          if st.button('p-save'):
               parms = (b_type,p_date,b_cat,b_quantity,b_units,customer,desc,amt)
               query = "INSERT INTO business_purchase (type, date, catagories, quantity,unit,customer, description, amount) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"  # Assuming you're using parameterized queries to prevent SQL injection
               cursor.execute(query, parms)
               conn.commit()
               st.write('Inserted')
     if option == 'Sale':
          # b_items = ['KAI Muruku','LAddai','AchuMuruku','Sweat KothuMuruku','Spice KothuMuruku','Adhirsam','PodalangaUndai']
          query = 'select * from product'
          cursor.execute(query)
          b_items = cursor.fetchall()
          products_name = [item[1] for item in b_items]
          b_item = st.selectbox('b-item',products_name)
          query_id = f"select id from product where product_name = '{b_item}'"
          cursor.execute(query_id)
          item_id = cursor.fetchone()
          col1,col2 = st.columns(2)
          with col1:
               b_packets = st.number_input('b_packets-count')
          with col2:
               @st.cache_data
               def calculate_weight(b_packets):
                    return ((b_packets * 200) / 1000)
               value = calculate_weight(b_packets)
               st.title(f'{value} Kg')
          clients = ['Dept-RPM','Mjith Store','Usian','Pakam','Kumar','Rk Sweats','Local']
          client = st.selectbox('b-clients',clients)
          hint = st.text_input('hint')
          amt = st.number_input("B-Amount")

          if st.button('s-Save'):
               parms = (b_type,p_date,item_id,b_packets,value,client,hint,amt)
               query = "INSERT INTO business_sales (type, date, item_id, packet,value,client, hint, amount) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"  # Assuming you're using parameterized queries to prevent SQL injection
               cursor.execute(query, parms)
               conn.commit()
               st.write('Inserted')
with tab4:
     p_date = st.date_input('P-Date')
     # p_items = ['KAI Muruku','LAddai','AchuMuruku','Sweat KothuMuruku','Spice KothuMuruku','Adhirsam','PodalangaUndai']
     query = 'select * from product'
     cursor.execute(query)
     b_items = cursor.fetchall()
     products_name = [item[1] for item in b_items]
     p_item = st.selectbox('Items',products_name)
     query_id = f"select id from product where product_name = '{p_item}'"
     cursor.execute(query_id)
     item_id = cursor.fetchone()
     p_quantity = st.number_input('Quantity')
     bucket_wight = 1.5
     net_quantiy = p_quantity-bucket_wight
     labour_count = st.number_input('labour Count')
     salary = st.number_input('Salary')
     total_salary = labour_count*salary
     st.write(total_salary)
     if st.button('save'):
          parms = (p_date,item_id,p_quantity,net_quantiy,labour_count,total_salary)
          query = "INSERT INTO productions (date, item_id, quantity,net_quantity,labour_count, salary) VALUES (%s,%s,%s,%s,%s,%s)"  # Assuming you're using parameterized queries to prevent SQL injection
          cursor.execute(query, parms)
          conn.commit()
          st.write('Inserted')
with tab5:
     # s_items = ['KAI Muruku','LAddai','AchuMuruku','Sweat KothuMuruku','Spice KothuMuruku','Adhirsam','PodalangaUndai']
     query = 'select * from product'
     cursor.execute(query)
     b_items = cursor.fetchall()
     products_name = [item[1] for item in b_items]
     s_item = st.selectbox('Is_tems',products_name)
     query_id = f"select id from product where product_name = '{s_item}'"
     cursor.execute(query_id)
     item_id = cursor.fetchone()
     s_packets = st.number_input('s-Packets')
     weight = st.number_input('Wight in Gram')
     s_net_weigth = (s_packets*weight)/1000
     if st.button('s-save'):
          parms = (item_id,s_packets,s_net_weigth)
          query = "INSERT INTO stocks (item_id, packets,kilo_gram) VALUES (%s,%s,%s)"  # Assuming you're using parameterized queries to prevent SQL injection
          cursor.execute(query, parms)
          conn.commit()
          st.write('Inserted')

