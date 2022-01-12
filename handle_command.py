import mysql.connector
import sys
import map_file

#Get maps and lists
attr_map = map_file.attr_map
condition_map = map_file.condition_map
list_c = map_file.list_c
list_ls = map_file.list_ls
list_stats = map_file.list_stats
list_type = map_file.list_type
list_update = map_file.list_update
list_existing_table = map_file.list_existing_table

# global variables
list_cond = []
list_table = []
attribute = ""

def handle_command(argv, priv):
    
    # Establish MYSQL connection
    config = {
    'user': 's352wu',
    'password': 'Myself098!',
    'host': 'marmoset04.shoshin.uwaterloo.ca',
    'database': 'db356_s352wu',
    'raise_on_warnings': True
    }
    cnx = mysql.connector.connect(**config)
    
    #Attain ans reset variables
    global list_cond
    global list_table
    global attribute
    list_cond = []
    list_table = []
    attribute = ""
    i = 1

    #Require commands
    if len(argv) < 2:
        print("Error: No enough inputs")
        return
    
    #-----------------Read input attributes according to command----------------------
    #------------Available commands: -dc, -c, -max, -min, -sum, -avg------------------
    if(argv[0] == "-dc" or argv[0] == "-c" or argv[0] == "-max" or argv[0] == "-min" or argv[0] == "-sum" or argv[0] == "-avg"):
        attribute = argv[1]
        #Valid attributes must in required lists
        if (argv[1] in attr_map and (argv[0] == "-dc" or argv[0] == "-c")):
            list_table.append(attr_map[attribute])
        elif(argv[1] in list_stats and (argv[0] == "-max" or argv[0] == "-min" or argv[0] == "-sum" or argv[0] == "-avg")):
            list_table.append(attr_map[attribute])
        elif (argv[1][:6] == "total_" or argv[1][:8] == "forward_" or argv[1][:9] == "backward_"):
            res = handle_type("-c", argv[1])
            if(res == -1):
                return
        #Invalid attribute
        else:
            print("Error: Invalid attribute: {}".format(argv[1]))
            return
        i = 2
    
    elif(argv[0] == "-ls"):
        attribute = []
        #Continue getting attributes
        while(i < len(argv)):

            #All attribute has been read
            if(argv[i][:1] == "-" ):
                break
            #Valid attributes must in required lists
            if argv[i] in attr_map:
                list_table.append(attr_map[argv[i]])
                attribute.append(argv[i])
            elif (argv[i][:6] == "total_" or argv[i][:8] == "forward_" or argv[i][:9] == "backward_"):
                res = handle_type("-ls", argv[i])
                if(res == -1):
                    return
            #select * 
            elif(argv[i] == "all"):
                for attr in list_ls:
                    list_table.append(attr_map[attr])
                    attribute.append(argv[i])
            else:
                print("Error: Invalid attribute: {}".format(argv[i]))
                return
            i = i + 1
        #Remove duplicate attributes
        attribute = list(dict.fromkeys(attribute))

    elif(argv[0] == "-update"):
        attribute = []
        #Admin priv is required
        if(priv == 0):
            print("Error: Permission denied")
            return  
        #Keep getting attributes
        while(i < len(argv)):
            if(argv[i][:1] == "-" ):
                break
            #Valid attributes must in required lists
            if argv[i] in attr_map:
                list_table.append(attr_map[argv[i]])
                attribute.append([argv[i], argv[i+1]])  
            elif (argv[i][:6] == "total_" or argv[i][:8] == "forward_" or argv[i][:9] == "backward_"):
                handle_type("-update", argv[i], argv[i+1])
            else:
                print("Error: Invalid attribute: {}".format(argv[1]))
                return
            i = i + 2
      
    elif(argv[0] == "-add"):
        if(priv == 0):
            print("Error: Permission denied")
            return
        table_name = argv[1]  
        i = 2
        # add a new row to an existing table
        if table_name in list_existing_table:
            add_new_row(argv, table_name, cnx)
            return
        # otherwise create a user defined table
        else:
            attribute = argv[1]
    else:
        print("Error: Invalid command: {}".format(argv[0]))
        return
    
    #Initialize variables
    limit = 0
    print_file = ""
    start = i
    operation = "and"

    #-----------------Read conditions ----------------------
    #-Available conditions: -and, -or, --attribute, map-
    while i < len(argv) :
        if(i == start):
            if(argv[i] == "-and"):
                operation = "and"
                i = i + 1
                continue
            elif(argv[i] == "-or"):
                operation = "or"
                i = i + 1
                continue
        #Valid conditions
        if argv[i] in condition_map:
            arg = argv[i + 1]
            list_arg = [condition_map[argv[i]], arg]
            list_cond.append(list_arg)
            list_table.append(attr_map[condition_map[argv[i]]])
        elif (argv[i][:2] == "--"):
            if argv[i][2:] in attr_map:
                arg = argv[i + 1]
                list_arg = [argv[i][2:], arg]
                list_cond.append(list_arg)
                list_table.append(attr_map[argv[i][2:]])
            else:
                print("Error: Invalid condition: {}".format(argv[i]))
                return
        #condition for limit rows     
        elif (argv[i] == "-l"):
            limit = argv[i + 1]
        #Write to file option
        elif (argv[i] == "-w"):
            print_file = argv[i + 1]
        else:
            print("Error: Invalid condition: {}".format(argv[i]))
            return
        i = i + 2

    # construct query
    string_table = ""
    #Remove duplicate rows
    list_table = list(dict.fromkeys(list_table))
    #Combine tables
    for table in list_table:
        string_table = string_table+table
        if(list_table.index(table) != len(list_table)-1):
            string_table = string_table + " natural join "
    
    #-----------------Translate input conditions to SQL ----------------------
    #-----------Available relations: eq, gt, lt, ge, le, in, ni---------------
    list_string_cond =[]
    for cond in list_cond:
        string_cond = ""
        if(cond[1][:2] == "eq"):
            if(cond[1][2:].isdecimal()):
                string_cond = cond[0] + " = " + cond[1][2:]
            else:
                string_cond = cond[0] + " = '" + cond[1][2:] + "'" 
            list_string_cond.append(string_cond)
        elif(cond[1][:2] == "gt"):
            string_cond = cond[0] + " > " + cond[1][2:] 
            list_string_cond.append(string_cond)
        elif(cond[1][:2] == "lt"):
            string_cond = cond[0] + " < " + cond[1][2:] 
            list_string_cond.append(string_cond)
        elif(cond[1][:2] == "ge"):
            string_cond = cond[0] + " >= " + cond[1][2:] 
            list_string_cond.append(string_cond)
        elif(cond[1][:2] == "le"):
            string_cond = cond[0] + " <= " + cond[1][2:] 
            list_string_cond.append(string_cond)
        elif(cond[1][:2] == "ne"):
            string_cond = cond[0] + " <> " + cond[1][2:] 
            list_string_cond.append(string_cond)
        elif(cond[1][:2] == "in" or cond[1][:2] == "ni"):
            string_list = cond[1][2:].split(",") 
            for string_tmp in string_list:
                if(string_list.index(string_tmp) == 0):
                    if(cond[1][:2] == "ni"):
                        string_cond = cond[0] + " not in ("
                    else:
                        string_cond = cond[0] + " in ("
                if(string_list.index(string_tmp) != len(string_list)-1):
                    if(string_tmp.isdecimal()):
                        string_cond = string_cond + string_tmp + ", " 
                    else:
                        string_cond =string_cond + "'" + string_tmp + "', " 
                else:
                    if(string_tmp.isdecimal()):
                        string_cond = string_cond + string_tmp + ")" 
                    else:
                        string_cond = string_cond + "'" + string_tmp + "')" 
            list_string_cond.append(string_cond)
        #Special case for add
        elif(cond[1] == "all"): pass
        else:
            print("Error: Invalid comparison: {}".format(cond[1][:2]))
            return
    
    #-----------------Combine conditions with appropriate relations ----------------------
    #Initialize variables
    string_conds = ""
    list_type_in = []
    type_cond = 0

    #Handle type attribute, must with 'or' relation
    if "type = 'backward'" in list_string_cond:
        list_type_in.append("type = 'backward'")
    if "type = 'forward'" in list_string_cond:
        list_type_in.append("type = 'forward'")
    if "type = 'total'" in list_string_cond:
        list_type_in.append("type = 'total'")
    if(len(list_type_in) > 1):
        for type_in in list_type_in:
            list_string_cond.remove(type_in)
            if(list_type_in.index(type_in) == 0):
                string_conds = string_conds + "(" + type_in + " or "
            elif (list_type_in.index(type_in) == len(list_type_in) - 1):
                string_conds = string_conds +  type_in + ")"
            else:
                string_conds = string_conds + type_in + " or "
    else:
        for type_in in list_type_in:
            list_string_cond.remove(type_in)
            string_conds = string_conds + type_in

    if(len(list_string_cond) != 0 and len(list_type_in) != 0 ):
        string_conds = string_conds + " and "
        type_cond = 1
        if(len(list_string_cond) > 1):
            string_conds = string_conds + "("
    
    #Other conditions, connect with 'and' or 'or'            
    for cond in list_string_cond:
        string_conds = string_conds + cond
        if(list_string_cond.index(cond) != len(list_string_cond)-1):
            if(operation == "and"):
                string_conds = string_conds + " and "
            else:
                string_conds = string_conds + " or "
    if(type_cond == 1 and len(list_string_cond) > 1):
        string_conds = string_conds + ")"
    
     #-----------------Create query according to command----------------------
    if(argv[0] == "-dc"):
        string_attr = attribute
        query = "select count(distinct " + string_attr + ") from " + string_table 
        output = "Count the distinct number of "+ string_attr  
        
    elif(argv[0] == "-c"):  
        string_attr = attribute
        query = "select count(" + string_attr + ") from " + string_table
        output = "Count the number of "+ string_attr 
       
    elif(argv[0] == "-ls"):
        string_attr = ""
        for attr in attribute:
            string_attr = string_attr + attr
            if(attribute.index(attr) != len(attribute)-1):
                string_attr = string_attr + ", "
            #select *
            if(attr == "all"):
                string_attr = "*"
                break
        if(string_attr == "*"):
            output = "List all the columns"
            query = "select " + string_attr + " from " + string_table
        else:
            output = "List column(s) " + string_attr
            query = "select distinct " + string_attr + " from " + string_table
    
    elif(argv[0] == "-max" or argv[0] == "-min" or argv[0] == "-sum" or argv[0] == "-avg"):
        string_attr = attribute
        cal = argv[0][1:]
        query = "select " + cal + "(" + string_attr + ") from " + string_table 
        output = "Find " + cal + " value of "+ string_attr
   
    elif(argv[0] == "-update"):
        string_attr = attribute
        query = "update " + string_table + " set " 
        for col in attribute:
            string_cols = ""
            if(col[1].isdecimal()):
                string_cols = col[0] + " = " + col[1]
            else:
                string_cols = col[0] + " = '" + col[1] + "'"
    
            query = query + string_cols
            if(attribute.index(col)== 0):
                output = "Update " 
            output = output + col[0] +  " to " + col[1]
            if(attribute.index(col) != len(attribute) - 1):
                query = query + ", "
                output = output + ", "  
    
    elif(argv[0] == "-add"):
        query = "create view " + attribute + " as \n" + "select "
        output = "Congrats! You have successfully added the table: " + attribute
        for cond in list_cond:
            query = query + cond[0] + ", "
        query = query[:-2] + " from " + string_table

    #If there's condition
    if(len(list_cond)!=0):
        query = query + " where " + string_conds
        output = output + " with condition(s) " + string_conds 
    #If there's limit
    if(limit != 0):
        query = query + " limit " + limit
    #-----------------Execute query----------------------
    print(query)
    
    cursor = cnx.cursor()
    print(output)
    
    cursor.execute(query)

    #-----------------Print results----------------------
    open_file = 0
    for (data) in cursor:
        if(print_file == ""):
            if(argv[0] == "-ls" or argv[0] == "-update" or argv[0] == "-add"):
                print(data)
            else:
                print("The result is: {}".format(data[0]))
        #Write to file
        else:
            if (open_file == 0):
                data_file = open(print_file,"w")
                open_file = 1
            else:
                data_file = open(print_file,"a")
            if(argv[0] == "-ls" or argv[0] == "-update" or argv[0] == "-add"):
                print(data, file = data_file) 
            else:
                print("The result is: {}".format(data[0]), file = data_file)
            data_file.close()
    cursor.close()
    cnx.close()

# function to add a new row to existing tables
def add_new_row(argv, table_name, cnx):
    print("argv: {}".format(argv))

    if argv[2] in map_file.condition_map:
        print("Error! The table {} already exists!".format(table_name))
        return
    column_list = []
    value_list = []

    i = 2
    while i < len(argv):
        column_list.append(argv[i])
        value_list.append(argv[i+1])
        i = i + 2

    query_parent_table = "insert into Flow (flow_key, timeStamp, duration) values ("
    k = 0
    while k < 3:
        query_parent_table = query_parent_table + value_list[k] + ", "
        k = k + 1
    query_parent_table = query_parent_table[:-2] + ")"
    
    query = "insert into " + table_name + " ("
    for column in column_list:
        query = query + column + ", "

    query = query[:-2] + ")\nvalues ("
    for value in value_list:
        query = query + value + ", "
    query = query[:-2] + ")"


    cursor = cnx.cursor()
    cursor.execute(query_parent_table)

    cursor.execute(query)
    cnx.commit()

    output = "Congrats! You have successfully added a row to the table: " + table_name
    print(output)
    cursor.close()
    cnx.close()

#Function to handle attributes with 'type_'
def handle_type(cmd, attr, next_attr = None):
    column = ""
    global list_cond
    global list_table
    global attribute
    if (attr[:6] == "total_"):
        if attr[6:] in list_type:
            column = attr[6:]
            list_cond.append(["type", "eqtotal"])
            
        else:
            print("Error: Invalid attribute: {}".format(argv[1]))
            return -1
            
    elif (attr[:8] == "forward_"):
        if attr[8:] in list_type:
            column = attr[8:]
            list_cond.append(["type", "eqforward"])
        else:
            print("Error: Invalid attribute: {}".format(argv[1]))
            return -1

    elif (attr[:9] == "backward_"):
        if attr[9:] in list_type:
            column = attr[9:]
            list_cond.append(["type", "eqbackward"])
        else:
            print("Error: Invalid attribute: {}".format(argv[1]))
            return -1
 
    list_table.append(attr_map[column])
    if(cmd == "-ls"):
        attribute.append(column)
    elif(cmd == "-update"):
        attribute.append([column, next_attr])
    else:      
        attribute = column
    return 0
    


