#streamlit interface

#import tools and define site bodies

import streamlit as st
import pandas as pd
from functions import *
from PIL import Image
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import datetime
import requests
import os
import time
import numpy as np 
from csv import DictWriter

pageheader = st.container()
main_page = st.container()

#login in check (cache)

df = pd.read_csv("user base.csv", sep=";")

if 1 in list(df["logged_in"]):
    logged_in = True
    logged_in_user = df.index[df["logged_in"]==1].tolist()[0]

if 1 not in list(df["logged_in"]):
    logged_in = False
    logged_in_user = -1

#header bodie (site selection)

with pageheader:
    coli, cold, colf = st.columns(3)
    logo_image = Image.open('logo.png')
    cold.image(logo_image)
    page = st.selectbox("Choose your page", ["Login", "Betting", "Ranking", "Analytics"])

#main bodie (4 different sites)

with main_page:

    #login page

    if page == "Login":

        st.subheader("Welcome to BetCoin™!")

        st.write("Create a user or login with your existing account.")
        st.write("Every new user starts with a blance of 100.")
        st.write("You can bet on 5 different crypto coins to go up or down within the next 15 seconds.")
        st.write("Bets entries range between 1 and 10. The return is double or nothing.")
        st.write("Look on the ranking page how you compare to other players.")
        st.write("Have fun!")

        st.subheader("Login or Create a User")

        if logged_in == False:

            #user login

            st.write("Please login in with your username and password. If you have no account please create a new user")
            
            col1, col2 = st.columns(2)
                
            username = col1.text_input("Username")

            password = col2.text_input("Password")

            if col1.button("Login"):

                if logged_in == True:

                    st.write("You are already logged in. To switch users please log out before!")

                if logged_in == False:
                
                    #create dataframe

                    df = pd.read_csv("user base.csv", sep=";")

                    #check if user is in database

                    if username in list(df["username"]):

                        user_id = df.index[df['username']==username].tolist()[0] #assign index

                        if password == df["password"][user_id]: #compare the password the user has typed in whith the password in the data base
                            
                            logged_in = True

                            logged_in_user = user_id

                            name = df["username"][logged_in_user]

                            st.write(f"Welcome. You are logged in as user {name}") 

                            change_database(logged_in_user, "logged_in", 1)

                            page = "Betting"

                        else:
                            st.write("Wrong Password. Please try again!")    

                    else:

                        st.write("Username does not exist. Try again or create new user!")


            #new user

            st.subheader("")
            st.subheader("")

            st.subheader("Create a new User")
            col3, col4 = st.columns(2)

            username_new = col3.text_input("Select Username")
            
            password_new = col4.text_input("Select Password")

            st.subheader("")

            if st.button("Create User"):
                
                df = pd.read_csv("user base.csv", sep=";")

                if username_new in list(df["username"]):
                    
                    st.write("This username is already taken. Please try again with another one.")

                else:
                    
                    appender(username_new, password_new, 100)

                    st.write(f"A new user {username_new} has been created successfully!")

        if logged_in == True:

            df = pd.read_csv("user base.csv", sep=";")

            log_name = df["username"][logged_in_user]

            st.write(f"You are currently logged in as user {log_name}")

            if st.button("Logout"):

                if logged_in == False:

                    st.write ("You are already logged out!")
                
                if logged_in == True:

                    logged_in = False

                    change_database(logged_in_user, "logged_in", 0)

                    logged_in_user = -1

                    st.write("You were logged out successfully!")

    #betting page

    if page == "Betting":

        df = pd.read_csv("user base.csv", sep=";")

        if logged_in == True:

            name = df["username"][logged_in_user]
            current_balance = df["balance"][logged_in_user]

            if current_balance > 0:

                st.header(f"Hello {name}. Place a Bet!")
                st.write(f"Your current balance is {current_balance}")

            if current_balance == 0:

                st.header(f"Hello {name}!")
                st.write(f"You are our of currency. Please create a new account to bet.")

        if logged_in == False:

            st.header("Please log in to play!")

        #select coin

        st.subheader("")
        st.subheader("")

        st.subheader("Select the Coin to bet on")

        col1, col2, col3, col4, col5 = st.columns(5)

        bitcoin_image = Image.open('Bitcoin.png')
        ether_image = Image.open('Ether.png')
        doge_image = Image.open('Doge.png')
        ltc_image = Image.open('Ltc.png')
        tron_image = Image.open('Tron.png')

        col1.write("**BitCoin** (BTC)")
        col1.image(bitcoin_image)
        col2.write("**Ether** (ETH)")
        col2.image(ether_image)
        col3.write("**DogeCoin** (DOGE)")
        col3.image(doge_image)
        col4.write("**LiteCoin** (LTC)")
        col4.image(ltc_image)
        col5.write("**Tron** (TRX)")
        col5.image(tron_image)

        

        
        st.subheader("")
        coin_options = ("BitCoin","Ether","DogeCoin","LiteCoin","Tron")
        coin_selection = st.radio("Selection", coin_options)
        coin_base = {"BitCoin" : "BTCUSDT", "Ether" : "ETHUSDT", "DogeCoin" : "DOGEUSDT", "LiteCoin" : "LTCUSDT", "Tron" : "TRXUSDT"}
        coin_database = {"BitCoin" : "btc_amount", "Ether" : "eth_amount", "DogeCoin" : "doge_amount", "LiteCoin" : "litecoin_amount", "Tron" : "trx_amount"}


        #select bet amount

        st.subheader("Select the bet amount")

        bet_amount = st.slider("Bet Amount", 1, 10, 3, 1)


        #select up or down

        st.subheader("Slease select movement prediction")

        direction_options = ("Up","Down")
        direction_selection = st.radio("Selection", direction_options)

        #bet area

        col6, col7 = st.columns(2)

        col6.subheader("Confirm you bet")
        col7.subheader("Bet Status")

        col6.write("Please confirm you bet choice. You must be at least the age of 18 to participate.")

        #run bet

        if col6.button("GO!"):

            if logged_in == True:

                direction = direction_selection
                amount = bet_amount

                df = pd.read_csv("user base.csv", sep=";")
                starting_balance = df["balance"][logged_in_user]

                if starting_balance - bet_amount >= 0:

                    add_database(logged_in_user, "total bet amount", amount)

                    add_database(logged_in_user, "nr_bets", 1)

                    add_database(logged_in_user, coin_database[coin_selection], 1)

                    sub_database(logged_in_user, "balance", amount)

                    col7.write(f"Bet Started")

                    col7.write(f"Selection: User paid {amount} to bet on {coin_selection} to move {direction_selection}")

                    bet_inip = get_price(coin_base[coin_selection])
                    col7.write(f"Initial Price: {bet_inip}")

                    with col7.empty():
                        for seconds in range(16):
                            st.write(f"Countdown: {15 - seconds} Seconds")
                            time.sleep(1)

                    bet_endp = get_price(coin_base[coin_selection])

                    difference = float(bet_endp) - float(bet_inip)

                    col7.write(f"Final Price: {bet_endp} (Δ {difference})")

                    #define if win or loose
         
                    if difference > 0:
                        posneg = "positive"

                    if difference < 0:
                        posneg = "negative"
                        
                    if difference == 0:
                        posneg = "0"
                    
                    win = True
                    
                    if direction == "Up":
                        if difference > 0:
                            win = True
                            
                        else:
                            win = False
                            
                    if direction == "Down":
                        if difference < 0:
                            win = True
                            
                        else:
                            win = False
                            
                    #give annoucement
                    
                    if win == True:
                        col7.write(f"Status: Won")
                        col7.write(f"Price Money: {amount*2}")
                        add_database(logged_in_user, "balance", amount*2)
                        add_database(logged_in_user, "nr_win", 1)

                    if win == False:
                        col7.write(f"Status: Loss")
                        add_database(logged_in_user, "nr_loss", 1)

                    

                    df = pd.read_csv("user base.csv", sep=";")

                    user_balance = df["balance"][logged_in_user]

                    col7.write(f"Your new balance is {user_balance}!")

                else:

                    col7.write("Your balance is not sufficient. Please try again with a lower amount!")


            if logged_in == False:

                col7.write("You are not logged in. Please log in to play!")

    #ranking page

    if page == "Ranking":

        df = pd.read_csv("user base.csv", sep=";") 

        criteria = {"Total Wins" : "nr_win", "Balance" : "balance", "Number of Total Bets" : "nr_bets"}

        lables = st.selectbox("Ranking Criteria", ["Total Wins", "Balance", "Number of Total Bets"])

        st.write(df.sort_values(by=[criteria[lables]], ascending = False).head(10)[["username", criteria[lables]]])

    #analytics page

    if page == "Analytics":
        
        df = pd.read_csv("user base.csv", sep=";")

        st.title("Analytics")
        st.text("Here you can check some analytic Infortmation")

        st.subheader("Overall bets on each Crypto Currency")
        data = pd.DataFrame({
            'index': ['BTC', 'ETH', 'DOGE', 'LITECOIN', 'TRON'],
            'amounts': [df["btc_amount"].sum(), df["eth_amount"].sum(), df["doge_amount"].sum(), df["litecoin_amount"].sum(), df["trx_amount"].sum()],
        }).set_index('index')

        st.bar_chart(data)



        identification = logged_in_user

        st.subheader("Pie Chart comparing User Wins to Losses")

        if identification <= len(df.index) and identification >= 0:
            wins_losses = {
                "wins": df["nr_win"][identification],
                "losses": df["nr_loss"][identification]
                }
            values = list(wins_losses.values())
            labels = list(wins_losses.keys())

            fig = px.pie(values = values, names = labels)
            st.write(fig) 
        
        if identification == -1:

            st.write("Please login to access this feature!")

        if identification <= -2:
            st.write("This user does not exist.")













