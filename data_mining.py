import numpy as np
import matplotlib.pyplot as plt
import mysql.connector

def main():
    config = {
        'user': 's352wu',
        'password': 'Myself098!',
        'host': 'marmoset04.shoshin.uwaterloo.ca',
        'database': 'db356_s352wu',
        'raise_on_warnings': True
    }
    cnx = mysql.connector.connect(**config)

    cursor = cnx.cursor()
    sql_file = open("data_mining.sql")
    sql_as_string = sql_file.read()
    cursor.execute(sql_as_string)
    result_array = list(cursor.fetchall())
    
    cursor.close()
    cnx.close()

    web_service_list = []
    freq_list_final = []
    for result in result_array:
        web_service_list.append(result[0])
        freq_list_final.append(result[1:])
    
    hour_list = [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

    plot_results(hour_list, "Hour of a Day", freq_list_final, "Detected Frequency", web_service_list)
    

def plot_results(x, x_label, y, y_label, legend):
    
    for freq_list in y:
        plt.plot(x, freq_list)
    
    plt.title("Frequency of Web Services Detected at Different Time of a Day")
    lgd = plt.legend(legend, bbox_to_anchor=(1.5, 1), loc = 'upper right')
    plt.xlabel("{}".format(x_label))
    plt.ylabel("{}".format(y_label))
    plt.savefig("data_mining_output.png", dpi=300, format='png', bbox_extra_artists=(lgd,), bbox_inches='tight')
    plt.clf()

if __name__ == "__main__":
  main()