import mysql.connector

def create_account():
    # Establish MYSQL connection
    config = {
        'user': 's352wu',
        'password': 'Myself098!',
        'host': 'marmoset04.shoshin.uwaterloo.ca',
        'database': 'db356_s352wu',
        'raise_on_warnings': True
    }
    cnx = mysql.connector.connect(**config)

    print("The following step will take you through account creation")
    print("You can use 'ctrl+c' to quit the process")
    try:
        username = input("Please enter a username (limit: within 35 characters): ")
        password = input("Please enter a password (limit: within 10 characters): ")
        priv = input("Please enter a account privilege (limit: 0 -- read priviledge, 1 -- admin priviledge): ")
    except KeyboardInterrupt:
        print ("Exit account creation")

    query = "insert into Clients (client_id, username, password, priv) values (uuid(), \"" + username + "\", \"" + password + "\", " + priv + ");"
    
    try:
        cursor = cnx.cursor()
        cursor.execute(query)
        cnx.commit()
        cursor.close()
        cnx.close()
        print("A new user is successfully added!")
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))