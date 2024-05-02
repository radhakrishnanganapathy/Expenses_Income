import streamlit as st
import psycopg2 as psc
from datetime import datetime


db_params = " postgresql://radhakrishnan:weJyKwjSj60UNzr4MXIEZ79FV7sf2ZHY@dpg-coiuro5jm4es739v1hvg-a.oregon-postgres.render.com/rkrish_db"
conn = psc.connect(db_params)
cursor = conn.cursor()

st.header("Income and Expenses Manager")

tab1, tab2, tab3,tab4,tab5 = st.tabs(['Dashboard','Home','Business','Production','Stocks'])

with tab1:
     options = ['Home','Business','Production','Stocks']
     select_option = st.selectbox('Select',options)
     today = datetime.today().date()
     first_date_of_month = datetime(today.year, today.month, 1).date()
     st.write(today, first_date_of_month)
     if select_option == 'Home':
          col1,col2, status = st.columns(3)
          with col1:
               inc = f"select sum(ammount) from expanses where date between  '{first_date_of_month}' and  '{today}' and e_type = 'Income'"
               cursor.execute(inc)
               income = cursor.fetchall() 
               st.success(income[0][0])
               # pass
          with col2:
               inc = f"select sum(ammount) from expanses where date between  '{first_date_of_month}' and  '{today}' and e_type = 'Expense'"
               cursor.execute(inc)
               expenses = cursor.fetchall() 
               st.error(expenses[0][0])
          view_type = ['table','pie','bar','graph']
          view = st.selectbox('view type',view_type)
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
     b_type = ['Income','Expense']
     st.selectbox('type',b_type)
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
          b_items = ['KAI Muruku','LAddai','AchuMuruku','Sweat KothuMuruku','Spice KothuMuruku','Adhirsam','PodalangaUndai']
          b_item = st.selectbox('b-item',b_items)
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
               parms = (b_type,p_date,b_item,b_packets,value,client,hint,amt)
               query = "INSERT INTO business_sales (type, date, item, packet,value,client, hint, amount) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"  # Assuming you're using parameterized queries to prevent SQL injection
               cursor.execute(query, parms)
               conn.commit()
               st.write('Inserted')
with tab4:
     p_date = st.date_input('P-Date')
     p_items = ['KAI Muruku','LAddai','AchuMuruku','Sweat KothuMuruku','Spice KothuMuruku','Adhirsam','PodalangaUndai']
     p_item = st.selectbox('Items',p_items)
     p_quantity = st.number_input('Quantity')
     bucket_wight = 1.5
     net_quantiy = p_quantity-bucket_wight
     labour_count = st.number_input('labour Count')
     salary = st.number_input('Salary')
     total_salary = labour_count*salary
     st.write(total_salary)
     if st.button('save'):
          parms = (p_date,p_item,p_quantity,net_quantiy,labour_count,total_salary)
          query = "INSERT INTO productions (date, item, quantity,net_quantity,labour_count, salary) VALUES (%s,%s,%s,%s,%s,%s)"  # Assuming you're using parameterized queries to prevent SQL injection
          cursor.execute(query, parms)
          conn.commit()
          st.write('Inserted')
with tab5:
     s_items = ['KAI Muruku','LAddai','AchuMuruku','Sweat KothuMuruku','Spice KothuMuruku','Adhirsam','PodalangaUndai']
     s_item = st.selectbox('Is_tems',s_items)
     s_packets = st.number_input('s-Packets')
     weight = st.number_input('Wight in Gram')
     s_net_weigth = (s_packets*weight)/1000
     if st.button('s-save'):
          parms = (s_item,s_packets,s_net_weigth)
          query = "INSERT INTO stocks (item, packets,kilo_gram) VALUES (%s,%s,%s)"  # Assuming you're using parameterized queries to prevent SQL injection
          cursor.execute(query, parms)
          conn.commit()
          st.write('Inserted')

