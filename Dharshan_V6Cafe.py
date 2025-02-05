import streamlit as st
st.set_page_config(layout="wide")
import warnings
import pandas as pd
from datetime import datetime
import warnings
import os, fnmatch
from PIL import Image
import glob
warnings.filterwarnings("ignore")

from streamlit_gsheets import GSheetsConnection


cwd = os.getcwd() 
st.write("Current working directory:", cwd) 

# file = []
# file = fnmatch.filter(os.listdir(cwd+"/pages/images"), '*.png')
# st.write(file)
# # images = glob.glob("/Users/xstream/pages/images/")
# totalimage = len(file)
# index= st.number_input('Index', min_value=0)

# if st.button('Next'):
#     index+=1
#     st.write(index)
    
# if st.button('Prev'):
#     if index > 0:
#         index = index -1
#         st.write(index)
        
# image = Image.open(cwd+"/pages/images/"+file[index])
# st.write(cwd+"/pages/images/"+file[index])
# st.image(image, use_column_width=True)


warnings.filterwarnings("ignore")


# st.set_page_config(
# #     page_title="Menu Restoran Xstream",
# #     page_icon="🧊",
#     layout="wide",
# #     initial_sidebar_state="expanded",
#     )
# Function to calculate total order
    
def calculate_total_order(order_list, menu_df):
    total = 0
    item_totals = []
    for item, quantity in order_list.items():
        price = menu_df.loc[menu_df['Item'] == item, 'Price'].values[0]
        item_total = price * quantity
        total += item_total
        item_totals.append((item, item_total))
    return total, item_totals

# Function to save order to CSV
def save_to_csv(order_list, total, item_totals):
    timestamp = datetime.now().strftime("%d/%m/%Y_%H:%M:%S")
    # order_df = pd.DataFrame(list(order_list.items()), columns=['Item', 'Quantity'])
    # order_df['Total'] = order_df['Item'].apply(lambda x: menu_df.loc[menu_df['Item'] == x, 'Price'].values[0])
    # order_df.to_csv(f'order_{timestamp}.csv', index=False)

    # item_totals_df = pd.DataFrame(item_totals, columns=['Item', 'Item Total'])
    dfmerge = pd.DataFrame
    dftotal,dfitem = report_sales(order_list, total_order, item_totals)
    dfmerge = dfmerge.merge(dfitem, dftotal)
    dfmerge.to_csv(f'sales_report_{timestamp}.csv', index=False)
    filename = "item_totals_"+timestamp+".csv"
    return filename
    
def report_sales(order_list, total, item_totals):
    order_df = pd.DataFrame(list(order_list.items()), columns=['Item', 'Quantity'])
    order_df['Price'] = order_df['Item'].apply(lambda x: menu_df.loc[menu_df['Item'] == x, 'Price'].values[0])
    item_totals_df = pd.DataFrame(item_totals, columns=['Item', 'Item Total'])
    return item_totals_df, order_df
    
# Load menu data from CSV
st.sidebar.title("Welcome to UEats!")

# url ="https://docs.google.com/spreadsheets/d/1QlA4nooETi96PUUi3Kwzfsg__tdxqfc4JKv2Ei6WPh0/edit?usp=sharing"
# ----------------------
conn = st.connection("gsheets", type=GSheetsConnection)
# menu_df = conn.read(spreadsheet=url,nrows=7,  worksheet="menu")
menu_df = conn.read(nrows=7, usecols=list(range(3)), ttl="1m",  worksheet="menu")
# --------------------
# menu_df = pd.read_csv("menu.csv")
menu_df = pd.DataFrame(menu_df)
menu_df = menu_df.dropna(subset=["Item"])
menu_df = menu_df.reset_index(drop=True)
menu_df.index = menu_df.index+1
TableNo=0

formside = st.sidebar.form("side_form")
choose = formside.radio("Please Select An Option.",["Order :rice:","Chef :male-cook:", "Admin :shallow_pan_of_food:", "Report :printer:"], index=None)
formside.form_submit_button("Submit")

if (choose == "Order :rice:"):
    st.title("Harraz Cafe Village 6")
    # st.image("menu_food.png")
    col1, col2, col3= st.columns(3)
    # Display menu
    col1.subheader("Menu")
    col2.subheader("Place Your Order")
    col3.subheader("Order Collection Status")

    TableNo = col2.number_input(f"Table No", min_value=1, max_value=9 )
    menu_df['Quantity'] = menu_df.apply(lambda x: col2.number_input(f"Quantity of {x['Item']}", min_value=0, max_value=10, key=x['Item']), axis=1)
    menu_display_df = menu_df.drop(columns=['Quantity'])  # Exclude the Quantity column from display
    menu_display_df = menu_display_df.rename(columns={'Price': 'Price (RM)'})
    # col1.write(menu_display_df[["Item","Price (RM)"]])

    col1.data_editor(
    menu_display_df,
    column_config={
        "Price (RM)": st.column_config.NumberColumn(format="RM %.2f"),
        "Picture": st.column_config.ImageColumn(
            "Picture", help="Cadangan Hiasan"
        )
    },disabled=["Item", "Price (RM)", "Picture"],
    hide_index=True,
    )
    
    
    # col1.write(menu_df[["Item","Quantity"]])
    # Order section

    # Create order dictionary
    order_list = {}
    for index, row in menu_df.iterrows():
        quantity = row['Quantity']
        if quantity > 0:
            order_list[row['Item']] = quantity

    # Calculate total order and item totals
    total_order, item_totals = calculate_total_order(order_list, menu_df)

    # Display item totals
    # col1.subheader("Item-wise Totals")
    # for item, item_total in item_totals:
    #     col1.write(f"{item}: RM{item_total:.2f}")

    # Display grand total
    # col1.subheader("Grand Total")
    # col1.write(f"Total Order Amount: RM{total_order:.2f}")

    # Save to CSV button
   
    # with col1.expander("Reports"):
        
    # Total Sales Report
    dfmerge = pd.DataFrame
    col1.subheader("Order Summary")
    col1.write("This section will display the total sales report.")
    dftotal,dfitem = report_sales(order_list, total_order, item_totals)
    dfmerge = dfmerge.merge(dfitem, dftotal)
    dfmerge.index = dfmerge.index+1
    col1.write(dfmerge)
    col1.write(f"Total Price of Order: RM{total_order:.2f}")

        
        # st.write(dfitem)
    if col1.button("Send Order"):
        #timestamp = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
        timestamp = datetime.now().strftime("%d_%m_%Y_%H_%M")
        dfmerge = pd.DataFrame
        dftotal,dfitem = report_sales(order_list, total_order, item_totals)
        dfmerge = dfmerge.merge(dfitem, dftotal)
        dfmerge.to_csv(f'sales_order_{TableNo}_{timestamp}.csv', index=False)
        # conn.update(worksheet="Sales_order", data=dfmerge)
        # st.toast('Hip!')
        # time.sleep(.5)
        # st.toast('Hip!')
        # time.sleep(.5)
        st.toast('Hooray!', icon='🎉')
        col1.success("Your order has been submitted successfully!")
        

    #Display Current Order
    cwd = os.getcwd()
    print (cwd)
    file = []
    file = fnmatch.filter(os.listdir(cwd), 'sales_chef*.csv')
    for order in file:
        tableno = order[11]
        orderdf = pd.read_csv(order)
        orderdf = orderdf.reset_index(drop=True)
        orderdf.index = orderdf.index+1
        col3.subheader(":green[Table No "+tableno+", your order is ready to be collected!]")
        col3.write(orderdf[["Item", "Quantity","Item Total"]])
    # video_file = open('https://youtu.be/Wh66ThpxvI4?si=_2OuZ_t5UBuT3CIC', 'rb')
    # video_bytes = video_file.read()
    col3.video('https://www.youtube.com/watch?v=isCbfE1PEz0&ab_channel=UTPResidentialVillage')
    
    
   
    
elif (choose == "Admin :shallow_pan_of_food:"):
    rahsia = st.number_input('Enter Admin Passcode', format= "%d", placeholder="Enter Passcode", step=1)
    if rahsia == 12345:
    
        st.title("Admin Page")
        # st.image("menu_food.png")
        tab1, tab2, tab3 = st.tabs(["Menu - Edit", "Completed Orders", "Latest Sales"])
        # col1, col2, col3= st.columns(3)
        # Display menu
        # col1.subheader("Menu Makanan - Suntingan/Edit")
        # col2.subheader("Order Kena Hantar")
        # col3.subheader("Jualan Terkini")
        
        # col1 edit menu makanan
        editmenu_df = tab1.data_editor(
                menu_df[["Item", "Price"]], column_config={
                    "Item": "Edit Menu",
                    "Price": st.column_config.NumberColumn(
                        "New Price",
                        help="Change Price",
                        min_value=1.00,
                        max_value=20.00,step=0.10,
                        format="%.2f",
                    ),
                    "Picture": "Link Gambar Baru",
                }, hide_index=True)
        if tab1.button('Click Here To Update Menu'):
            conn.update(worksheet="menu", data=editmenu_df)
            tab1.success("Menu Was Successfully Updated")
            
        # col2 updatesale = pd.DataFrame()
        file = []
        file = fnmatch.filter(os.listdir(cwd), 'sales_chef*.csv')
        for order in file:
            tableno = order[11]
            orderdf = pd.read_csv(order)
            orderdf = orderdf.reset_index(drop=True)
            orderdf.index = orderdf.index+1
            orderdf["Rating"]= 5
            editedorderdf = tab2.data_editor(
                orderdf[["Item", "Quantity", "Price", "Item Total", "Rating"]], column_config={
                    "Rating": st.column_config.NumberColumn(
                        "Your rating",
                        help="Rating Star (1-5)?",
                        min_value=1,
                        max_value=5,step=1,
                        format="%d ⭐",
                    ),
                },disabled=["Item", "Quantity", "Price", "Item Total"], hide_index=True)
            
            tab2.write(f"Chef Has Finished Preparing for Table :{tableno}")
            sale_df = conn.read(worksheet="Sales_report")
            sale_df = pd.DataFrame(sale_df)
            sale_df = sale_df.dropna(subset=["Item"])
            sale_df = sale_df[["Item", "Quantity", "Price", "Item Total", "Rating", "Datetime"]]
            # st.write("data google", sale_df)
            if tab2.button('Click Here if Food Has Been Served to Table'+tableno):
                timestamp = datetime.now().strftime("%d\%m\%Y_%H:%M:%S")
                editedorderdf["Datetime"] = timestamp
                editedorderdf = editedorderdf[["Item", "Quantity", "Price", "Item Total", "Rating", "Datetime"]]
                # st.write("data editedorderdf", editedorderdf)
                updatesale = pd.concat([sale_df, editedorderdf], axis=0)
                
                # st.write(updatesale)
                # editedorderdf.to_csv('sales_report_'+tableno+'_'+timestamp+'.csv')
                conn.update(worksheet="Sales_report", data=updatesale)
                os.rename(order,"served"+order)
                tab2.success("Order Has Been Served To Customer!")
    
elif (choose == "Chef :male-cook:"):
    rahsia = st.number_input('Enter Chef Passcode', format= "%d", placeholder="Enter Passcode", step=1)
    if rahsia == 123:
        
        st.title("Chef Page")
        cwd = os.getcwd()
        print (cwd)
        file = []
        file = fnmatch.filter(os.listdir(cwd), 'sales_order*.csv')
        ordersum =len(file)
        for order in file:
            tableno = order[12]
            orderdf = pd.read_csv(order)
            orderdf["Done"] = False
            orderdf["TableNo"]= tableno
            editedorderdf = st.data_editor(
                orderdf,disabled=["Item", "Quantity", "Price", "Item Total"], hide_index=True)
            
            if st.button('Confirm Preparation of Table '+tableno):
                editedorderdf.to_csv('sales_chef_'+tableno+'.csv')
                os.rename(order,"chefdone"+order)
                st.success("Order Has Been Submitted Successfully!")

elif (choose == "Report :printer:"):
    sale_df = conn.read(worksheet="Sales_report")
    sale_df = pd.DataFrame(sale_df)
    sale_df = sale_df.dropna(subset=["Item"])
    sale_df = sale_df.reset_index(drop=True)
    sale_df = sale_df[["Item", "Quantity", "Price", "Item Total", "Rating", "Datetime"]]
    sale_df.index = sale_df.index+1
    st.write(sale_df)
    sale_df["Total Sales"] = sale_df["Quantity"] * sale_df["Price"]
    order_list = {}
    order_listSQ = {}
    order_listSS = {}
    
    for index, row in sale_df.iterrows():
        subsales = sale_df[sale_df["Item"] == row["Item"]]["Total Sales"].sum()
        subquantity = sale_df[sale_df["Item"] == row["Item"]]["Quantity"].sum()
        order_listSQ[row["Item"]] =  subquantity
        order_listSS[row["Item"]] =  subsales
   
    
    # st.write(orderSQ.style.highlight_max(axis=0))
    # st.write(orderSS.style.highlight_max(axis=0))
    # editedorderSQ = st.data_editor(
    #         orderSQ,column_config={"Key":"Menu", "Values":"Quantity"})
    # editedorderSS = st.data_editor(
    #         orderSS,column_config={"Key":"Menu", "Values":"Total (RM)"})
    
    
    
    with st.expander("Report"):
        st.subheader("Total Orders")
        st.write("This section will display the total sales report.")
        st.subheader(f"Total Sales = RM{sale_df['Total Sales'].sum():.2f}")
        orderSQ = pd.DataFrame(list(order_listSQ.items()), columns=['Key', 'Values'])
        orderSS = pd.DataFrame(list(order_listSS.items()), columns=['Key', 'Values'])
        orderSQ["Total RM"] = orderSS["Values"]
        orderSQ.rename(columns = {'Values':'Quantity'}, inplace = True) 
        orderSQ.rename(columns = {'Key':'Menu'}, inplace = True) 
        orderSQ.index = orderSQ.index+1
        st.write(orderSQ.style.highlight_min(axis=0))
        st.bar_chart(orderSQ, x="Menu")


        data_df = pd.DataFrame(
            {
                "category": [
                    "🍚 Nasi Goreng",
                    "🥣 Bihun Goreng",
                    "🍗 Ayam Goreng",
                    "🍹 Teh Tarik",
                ],
            }
        )
        
        st.data_editor(
            data_df,
            column_config={
                "category": st.column_config.SelectboxColumn(
                    "App Category",
                    help="The category of the app",
                    width="medium",
                    options=[
                        "🍚 Nasi Goreng",
                        "🥣 Bihun Goreng",
                        "🍗 Ayam Goreng",
                        "🍹 Teh Tarik",
                    ],
                    required=True,
                )
            },
            hide_index=True,
        )
    
        
    #     for _key, value in order_list.items():
    #         st.write(f'Menu: {_key}, Quantity: {value[0]} , RM: {value[1]}')
    # # order_list
        


    #         st.write(f'Menu: {_key}, Quantity: {value[0]} , RM: {value[1]}')
    # # order_list
        

