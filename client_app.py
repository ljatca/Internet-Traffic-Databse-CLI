import mysql.connector
import sys, getopt
from datetime import datetime
import handle_command
import create_account

def main(argv):
  #config to connect MySQL server
  config = {
        'user': 's352wu',
        'password': 'Myself098!',
        'host': 'marmoset04.shoshin.uwaterloo.ca',
        'database': 'db356_s352wu',
        'raise_on_warnings': True
  }
  cnx = mysql.connector.connect(**config)

  valid_user_has_account = ['n', 'no', 'y', 'yes']
  
  print("\n###########################################")
  print("Welcome to the Internet Traffic CLI!")
  print("###########################################\n")

  #Sign in or Sign up
  user_has_account = input("Do you have an existing user account? (y/n) ")

  while user_has_account not in valid_user_has_account:
    user_has_account = input("Do you have an existing user account? (y/n) ")

  #Sign up
  if user_has_account == "n" or user_has_account == "no":
    create_account.create_account()

  #Sign in
  username = input("Please enter your user ID: ")
  password = input("Please enter your password: ")
  priv_query = "select priv from Clients where username = \"" + username + "\" and password = \"" + password + "\""
  
  #Check whether the account/password is correct
  try:
    cursor = cnx.cursor()
    cursor.execute(priv_query)
  except mysql.connector.Error as err:
    print("Something went wrong: {}".format(err))

  exist = cursor.fetchone() 

  if exist is None:
    sys.exit("The account does not exist!")
  
  priv = exist[0]

  #Start to enter commands
  while True:
    user_input = input("Please enter the commands: ")

    #Exit the kernel
    if user_input == "exit":
        break
    handle_command.handle_command(user_input.split(), priv)


if __name__ == "__main__":
  main(sys.argv[1:])