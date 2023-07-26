import streamlit

streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Favorites')
# streamlit.text('')
streamlit.text(' 🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text(' 🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text(' 🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

## Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

## Display the table on the page.
streamlit.dataframe(fruits_to_show)

## Display fruityvice api response
streamlit.header('Fruityvice Fruit Advice')

fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

import requests
# fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
# streamlit.text(fruityvice_response.json())
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + "kiwi")

## take the json text version of the response above and normalize it
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())

## output the result as a table
streamlit.dataframe(fruityvice_normalized)

# The requirements.txt file we added in this project tells Streamlit what libraries we plan to use in our project so it can add them in advance.

streamlit.stop() #temporarily stop from here while troubleshooting

import snowflake.connector

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()

# my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
# streamlit.text("Hello from Snowflake:")

my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
streamlit.text("The fruit load list contains:")

# my_data_row = my_cur.fetchone()
my_data_row = my_cur.fetchall()
streamlit.dataframe(my_data_row)

## allow the end user to add a fruit from the list
add_my_fruit =  streamlit.text_input('What fruit would you like to add?')
streamlit.write("Thanks for adding ", add_my_fruit)

my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values ('from streamlit')") 
## Note: This command above on its own will result to it being executed over and over again everytime there is interaction in the app
## Note: We need to organize our code and introduce some structure that will ensure all the code doesn't run everytime. A row should only be added when we want a row to be added. 


