import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError #for control of flow

# ---------------------------------------------------------------- #
# Introductory descriptions

streamlit.title('My Parents New Healthy Diner')
streamlit.header('Breakfast Favorites')
# streamlit.text('')
streamlit.text(' 🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text(' 🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text(' 🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

# ---------------------------------------------------------------- #
# Sourcing random data from web

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries']) # Let's put a pick list here so they can pick the fruit they want to include 
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show) # Display the table on the page.

# ---------------------------------------------------------------- #
# Fruityvice Reatlated Steps 

def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json()) ## take the json text version of the response above and normalize it
    return fruityvice_normalized

#!!# Introducing this structure allows us to separate the code that is loaded once from the code that should be repeated each time a new value is entered.
#!!# Alternately, if we did not encapculate the code, they will be executed over and over again every time there is interaction in the app.

streamlit.header('Fruityvice Fruit Advice') # Display fruityvice api response
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function) # output the result as a table

except URLError as e:
  streamlit.error()

# ---------------------------------------------------------------- #
# Snowflake-related steps
# Loading the list from snowflake and adding user inputted items back to the snowfake table
#!!# The requirements.txt file we added in this project tells Streamlit what libraries we plan to use in our project so it can add them in advance.

streamlit.header("View Our Fruit List - Add Your Favorites!")

def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
        return my_cur.fetchall()

if streamlit.button('Get Fruit List'): #Add a button to load the fruit; the function returns true or false depending if the user clicked the button in the app
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"]) # creating connection between snowflake and streamlit via the Secrets config in streamlit app settings
    my_data_row = get_fruit_load_list()
    my_cnx.close() # we open Snowflake Connection each time a button on the page is clicked, let's also close the connection at the end of each button's scrip
    streamlit.dataframe(my_data_row)

def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values ('" + new_fruit + "')") 
        return "Thanks for adding " + new_fruit
        
add_my_fruit = streamlit.text_input('What fruit would you like to add?') # allow the end user to add a fruit from the list

if streamlit.button('Add a Fruit to the list'): # using this encapsulation button, we only insert or execute the command if the button is clicked or returns true, instead of being executed every interaction made in the app
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_my_fruit)
    my_cnx.close()
    streamlit.text(back_from_function)

# ---------------------------------------------------------------- #

#!!# Archived codes

# fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
# streamlit.text(fruityvice_response.json())

# my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
# streamlit.text("Hello from Snowflake:")

# my_data_row = my_cur.fetchone()

# my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values ('from streamlit')") 
#!!# Note: This command above on its own will result to it being executed over and over again everytime there is interaction in the app
#!!# Note: We need to organize our code and introduce some structure that will ensure all the code doesn't run everytime. A row should only be added when we want a row to be added. 

# ---------------------------------------------------------------- #
