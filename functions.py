#import of packages
import numpy as np 
import matplotlib.pyplot as plt
import requests
import time
import pandas as pd
import os
from csv import writer
from csv import DictWriter

#import data
userbase = pd.read_csv("user base.csv")

#define classes

class User:
    def __init__(self, username, password, balance):
        # set up login data (user name/email, password) upon initation of class
        
        # set username and password and store them into a list
        self.username = username
        self.password = password
        self.balance = balance
        
        #load the data frame and define unique ID for user when the object is instaciated

        df = pd.read_csv("user base.csv", sep=";")        
        self.user_id = len(df.index) + 1


        #create data frame for new user
        
        new_user_df = pd.DataFrame()

        #put data about new user into new data frame
        new = new_user_df.append({
                'id': self.user_id,
                'username': self.username,
                'password': self.password,
                'balance': float(self.balance),
                'total bet amount': 0,
                'nr_win': 0,
                'nr_loss': 0, 
                'nr_bets': 0, 
                'btc_amount': 0, 
                'eth_amount': 0, 
                'doge_amount': 0 ,       
                'litecoin_amount': 0, 
                'tether_amount': 0}, ignore_index=True)

        # save data from data frame into our csv
        new.to_csv("user base.csv", sep = ";", mode='a', index=False, header=False)
        
        
    def reset_password(self):
        user_said_y_or_n = False
        incompetence_counter = 0
        while user_said_y_or_n == False:
            answer = input("Do you want to change your password? (y/n)")
      
            if answer == "y":
                new_password = input("Please type in your new password:")
                self.password = new_password
                user_said_y_or_n = True
                # here I need to call the change_database() to also reset the password in the csv
                

            elif answer == "n":
                print("Ok, no worries mate...")
                user_said_y_or_n = True
            else:
                incompetence_counter += 1
                if incompetence_counter == 1:
                    print("""please type in "y" or "n"!""")

                elif incompetence_counter == 2:
                    print("""All you have to do is type in "y" or "n"...""")

                else:
                    print("""You probably shouldn't play with crypto...""")
                    
        
#define functions

def appender(username, password, balance):
    
    df = pd.read_csv("user base.csv", sep=";")

    new = {
                'id': len(df.index),
                'username': username,
                'password': password,
                'balance': float(balance),
                'total bet amount': 0,
                'nr_win': 0,
                'nr_loss': 0, 
                'nr_bets': 0, 
                'btc_amount': 0, 
                'eth_amount': 0, 
                'doge_amount': 0 ,       
                'litecoin_amount': 0, 
                'tether_amount': 0,
                'logged_in' : 0}

    append_series = pd.Series(new)

    new_df = df.append(append_series, ignore_index = True)

    new_df.to_csv("user base.csv", sep = ";", mode='w', index=False, header=True)

def change_database(user_id, variable_to_change, new_value):

    #1 load csv into data frame
    df = pd.read_csv("user base.csv", sep=";")
    
    #2 identify the column index where the variable we are changing is located
    column_number = df.columns.get_loc(variable_to_change)
    
    #3 change the value in the data frame
    df.iat[user_id, column_number] = new_value
    
    #4 use to_csv in write mode to change the csv
    df.to_csv("user base.csv", sep = ";", mode='w', index=False, header=True)


def add_database(user_id, variable_to_change, new_value):
    #3 change the value in the data frame
    #4 use to csv to in write mode to change the csv

    #1 load csv into data frame
    df = pd.read_csv("user base.csv", sep=";")
    
    #2 identify the column index where the variable we are changing is located
    column_number = df.columns.get_loc(variable_to_change)
    
    #3 change the value in the data frame
    df.iat[user_id, column_number] += new_value
    
    #4 use to_csv in write mode to change the csv
    df.to_csv("user base.csv", sep = ";", mode='w', index=False, header=True)


def sub_database(user_id, variable_to_change, new_value):
    #3 change the value in the data frame
    #4 use to csv to in write mode to change the csv

    #1 load csv into data frame
    df = pd.read_csv("user base.csv", sep=";")
    
    #2 identify the column index where the variable we are changing is located
    column_number = df.columns.get_loc(variable_to_change)
    
    #3 change the value in the data frame
    df.iat[user_id, column_number] -= new_value
    
    #4 use to_csv in write mode to change the csv
    df.to_csv("user base.csv", sep = ";", mode='w', index=False, header=True)        

def get_price(stock):

    url = "https://api2.binance.com/api/v3/ticker/price"
    params = {'symbol': stock}
   
    response = requests.get(url=url, params=params)
    # print(response.url)
    
    if response.status_code != 200:
        
        return None
   
    else:
        info_start = response.json()
        return info_start["price"]

def create_user(username,password, balance):
    
    #1 load csv into data frame

    df = pd.read_csv("user base.csv", sep=";")

    #2 check if user exists in the data base

    if username in list(df["username"]):
        
        print("This username is already taken. Please try again with another one.")
        
    else:
        new_user = User(username, password, balance) #here we must adapt the user class a little bit because we cannot use the input function
   
def login_user(username, password):
    #1 load csv into data frame
    df = pd.read_csv("user base.csv", sep=";")
    #2 check if that username exists (if yes go on, if no tell the user that he doestn exist)
    if username in list(df["username"]):
        #3 find out the id of the user
        user_id = df.index[df['username']==username].tolist()[0] #this gives us the index of the user
                                                    
        #4 compare password in database with password input (if not equal reject: if equal continue)
        if password == df["password"][user_id]: #compare the password the user has typed in whith the password in the data base
            print("This was the right password you are now logged in")
        else:
            print("Wrong password, sorry...")
    else:
        print("Username does not exist.")      

def make_trade(symbol):
    trade_amount[symbol] += 1
    return f"Succesfully traded {symbol}"
 
def plot_trades(diagram):
    x_axis = list(trade_amount.keys())
    values = list(trade_amount.values())
    if diagram == "bar":
        plt.bar(x_axis, values, color = "blue", width = 0.4)
    elif diagram == "pie":
        plt.pie(values, labels=x_axis)
    else:
        print("Argument must be either 'bar' or 'pie' depending on what you want to plot.")





