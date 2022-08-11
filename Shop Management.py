# IMPORTS: 
# sqlite3 FOR DATABASE CONNECTIVITY AND OPERATION
import sqlite3 as db
# coloroma TO COLOR THE TEXT
from colorama import Fore
# datetime TO GET THE CURRENT TIMESTAMP
import datetime
# tabulate IS USED TO TABULAR FORMAT
from tabulate import tabulate

# initDB(): A FUNCTION TO INITIALIZE THE DATABASE BY CREATING TABLE ...
def initDB():

    # connectObj IS THE DB OBJECT
    connectObj = db.connect("shopMgmt.db")
    # cursor IS USED TO RUN QUERIES AND FETCH RECORD FROM SELECT STATEMENT
    cursor = connectObj.cursor()
    
    # STORING THE QUERY AS STRING TO EXECUTE LATER
    # users TABLE TO STORE THE LOGIN DETAILS
    sql = '''
    CREATE TABLE IF NOT EXISTS users(
        userType NUMBER,
        userName STRING PRIMARY KEY,
        password STRING
    )
    '''
    # FORMAL WAY OF EXECUTING QUERIES USING execute() METHOD
    cursor.execute(sql)
    
    # products TABLE TO STORE THE PRODUCT DETAILS LIKE PRICE AND QUANTITY
    sql = '''
    CREATE TABLE IF NOT EXISTS products(
        productId NUMBER PRIMARY KEY,
        productName STRING,
        quantity NUMBER,
        price FLOAT
    )
    '''
    cursor.execute(sql)

    # purchaseHistory TABLE TO STORE PAST SALES
    sql = '''
    CREATE TABLE IF NOT EXISTS purchaseHistory(
        srno INTEGER PRIMARY KEY AUTOINCREMENT,
        customerName STRING,
        productIdsPurchased STRING,
        amountPaid FLOAT,
        date STRING,
        customerPhone NUMBER(10)
    )
    '''
    cursor.execute(sql)

    # employees TABLE TO STORE EMPLOYEE DATA
    sql = '''
    CREATE TABLE IF NOT EXISTS employees(
        empId INTEGER PRIMARY KEY AUTOINCREMENT,
        empName STRING,
        empJob STRING,
        empJoinDate STRING
    )
    '''
    cursor.execute(sql)

    # INITIALIZING THE DEFAULT SYSTEM USER, IF NOT ALREADY.
    # FOR ADMIN
    sql = '''
    SELECT * FROM users WHERE userName = 'shopadmin'
    '''
    cursor.execute(sql)
    if len(cursor.fetchall()) == 0:
        sql = '''
        INSERT INTO users VALUES(0, 'shopadmin', 'admin@1234')
        '''
        cursor.execute(sql)

    # FOR CASHIER
    sql = '''
    SELECT * FROM users WHERE userName = 'cashier'
    '''
    cursor.execute(sql)
    if len(cursor.fetchall()) == 0:
        sql = '''
        INSERT INTO users VALUES(1, 'cashier', 'cash@1234')
        '''
        cursor.execute(sql)

    # commit() ON CONNECT OBJECT WILL SAVE THE CHANGES
    connectObj.commit()

    # TO CLOSE THE CONNECT USE .close()
    connectObj.close()

# startAdmin: A FUNCTION USED FOR AMDIN LOGIN PROCESS AND PROVIDES NUMEROUS LIST OF
# OF OPERATIONS TO PERFORM. RETURNS 1 INDICATING LOGOUT OR 0 INDICATING EXIT FROM A SYSTEM.
def startAdmin():
    connectObj = db.connect("shopMgmt.db")
    cursor = connectObj.cursor()

    sql = '''
    SELECT userName, password FROM users WHERE userType = 0
    '''
    cursor.execute(sql)
    # STORING THE USERNAME AND PASSWORD OF ADMIN
    userName, password = cursor.fetchall()[0]
    

    # ACCEPTING THE VALID USERNAME AND PASSWORD FOR VERIFICATION
    while True:
        id = input("\n\tEnter User Id of Admin: ").strip()
        if id != userName:
            print()
            print(Fore.RED + "No such admin exists! Please try again.".center(100) + Fore.WHITE)
            continue
        else:
            break
    while True:
        pwd = input("\tEnter your password, " + id + ": ").strip()
        if pwd != password:
            print()
            print(Fore.RED + "Incorrect password! Please try again.".center(100) + Fore.WHITE)
            print()
            continue
        else:
            break
    
    # PROMPTING AFTER SUCCESSFULL LOGIN
    print()
    print(Fore.GREEN + "Login successfull! Welcome, {}.".format(id).center(100) + Fore.WHITE)
    input()

    # A MAIN LOOP TO PERFORM ADMIN OPERATIONS ITERATIVELY UNLESS ADMIN CHOOSE TO EXIT OR LOGOUT
    while True:
        # AN ADMIN MENU.....
        print(Fore.BLUE + "----------Admin Menu----------".center(100) + Fore.WHITE)
        print(Fore.YELLOW + "\n\tSelect option to perform (0 to shutdown):" + Fore.WHITE)
        print("\t1 - View all sales")
        print("\t2 - View available products")
        print("\t3 - Add new product")
        print("\t4 - Update product price")
        print("\t5 - View employees")
        print("\t6 - Add employee")
        print("\t7 - Change password")
        print("\t8 - Logout")

        # ACCEPTING CHOICE FOR THE ABOVE OPTIONS..
        choice = getInt("\n\tEnter your choice: ")

        # EXIT CASE
        if choice == 0: 
            connectObj.close()
            return 0

        # 1 - CASE TO VIEW ALL PREVIOUS SALES
        elif choice == 1:
            sql = '''
            SELECT * FROM purchaseHistory
            '''
            cursor.execute(sql)
            sales = cursor.fetchall()
            print()
            print(tabulate(sales, headers=[Fore.YELLOW + 'Sr No.', Fore.YELLOW + 'Customer Name', Fore.YELLOW + 'Products Purc.', Fore.YELLOW + 'Amount Paid', Fore.YELLOW + 'Date', Fore.YELLOW + 'Phone'+ Fore.WHITE], numalign="center", stralign="center"))
            print()
            input()

        # 2 - CASE TO VIEW AVAILABLE PRODUCTS IN A STORE
        elif choice == 2:
            sql = '''
            SELECT * FROM products
            '''
            cursor.execute(sql)
            products = cursor.fetchall()
            print()
            print(tabulate(products, headers=[Fore.YELLOW + 'Product Id.', Fore.YELLOW + 'Product Name', Fore.YELLOW + 'Quantities Avail.', Fore.YELLOW + 'Price each'+ Fore.WHITE], numalign="center", stralign="center"))
            print()
            input()

        # 3 - TO ADD NEW PRODUCTS TO THE STORE INVENTORY
        elif choice == 3:
            while True: 
                prdId = getInt("\n\tEnter Product Id: ")
                if prdId == 0:
                    print()
                    print(Fore.RED + "Product Id cannot be 0".center(100) + Fore.WHITE)
                    input()
                else:
                    break
                
            sql = '''
            SELECT * FROM products WHERE productId = ?
            '''
            cursor.execute(sql, [prdId])
           
            if len(cursor.fetchall()) == 0:
                prdName = input("\tEnter Product Name: ")
                quantity = getInt("\tEnter Quantity: ")
                prdPrice = input("\tEnter Product Price: ")
                sql = '''
                INSERT INTO products VALUES(?, ?, ?, ?)
                '''
                cursor.execute(sql, (prdId, prdName, quantity, prdPrice))
                connectObj.commit()
            else:
                quantity = getInt("\tEnter Quantity: ")
                prdPrice = input("\tEnter Product Price: ")
                sql = '''
                UPDATE products SET quantity = quantity + ?, price = ? WHERE productId = ?
                '''
                cursor.execute(sql, (quantity, prdPrice, prdId))
                connectObj.commit()

            print()
            print(Fore.GREEN + "Product {} added to the stock.".format(prdId).center(100) + Fore.WHITE)
            input()

        # 4 - TO UPDATE PRICE OF EXISTING PRODUCTS
        elif choice == 4:
            print()
            while True:
                prdId = getInt("\tEnter Product Id to change the price of (0 to abort operation): ")

                if prdId == 0:
                    print()
                    print(Fore.RED + "Price Change operation aborted".center(100) + Fore.WHITE)
                    input()
                    break

                sql = '''
                SELECT * FROM products WHERE productId = ?
                '''
                cursor.execute(sql, [prdId])

                if len(cursor.fetchall()) != 0:
                    prdPrice = getInt("\tEnter new price of product {}: ".format(prdId) )
                    sql = '''
                    UPDATE products SET price = ? WHERE productId = ?
                    '''
                    cursor.execute(sql, (prdPrice, prdId))
                    connectObj.commit()
                    print()
                    print(Fore.GREEN + "Price of product {} has been updated to {}".format(prdId, prdPrice).center(100) + Fore.WHITE)
                    input()
                    break
                else:
                    print()
                    print(Fore.RED + "Product {} is not present in the stock".format(prdId).center(100) + Fore.WHITE)
                    input()

        # 5 - CASE THAT DISPLAYS ALL THE EMPLOYEES IN A STORE
        elif choice == 5:
            sql = '''
            SELECT * FROM employees
            '''
            cursor.execute(sql)
            employees = cursor.fetchall()
            print()
            print(tabulate(employees, headers=[Fore.YELLOW + 'Employee Id.', Fore.YELLOW + 'Employee Name', Fore.YELLOW + 'Employee Job', Fore.YELLOW + 'Join Date'+ Fore.WHITE], numalign="center", stralign="center"))
            print()
            input()

        # 6 - TO ADD NEW EMPLOYEE
        elif choice == 6:
            empName = input("\n\tEnter Name of employee: ")
            empJob = input("\tEnter Designation of employee: ")
            joinDate = str(datetime.datetime.now().date())
            if getInt("\n\tDo you want to insert {} as {}? (0 - No, 1 - Yes): ".format(empName, empJob)):
                sql = '''
                INSERT INTO employees(empName, empJob, empJoinDate)
                VALUES(?, ?, ?)
                '''
                cursor.execute(sql, (empName, empJob, joinDate))
                connectObj.commit()
                print()
                print(Fore.GREEN + "Employee {} has been inserted successfully".format(empName).center(100) + Fore.WHITE)
                input()
            else:
                print()
                print(Fore.RED + "Employee has not been inserted".center(100) + Fore.WHITE)
                input()

        # 7 - TO CHANGE CURRENT USER PASSWORD
        elif choice == 7:
            while True:
                pwd = input("\n\tEnter your current Password: ").strip()
                if pwd != password:
                    print()
                    print(Fore.RED + "Incorrect password! Please try again.".center(100) + Fore.WHITE)
                    continue
                else:
                    break

            while True:
                newPass = input("\tEnter new password (0 to stop changing): ").strip()
                if newPass == '0':
                    print()
                    print(Fore.RED + "You cancelled to change your password.".center(100) + Fore.WHITE)
                    input()
                    break
                if len(newPass) < 8:
                    print()
                    print(Fore.RED + "Password should not be less than 8 characters!.".center(100) + Fore.WHITE)
                    print()
                else:
                    password = newPass
                    sql = '''
                    UPDATE users SET password = ? WHERE userType = ?
                    '''
                    cursor.execute(sql, (password, 0))
                    connectObj.commit()
                    print()
                    print(Fore.GREEN + "Password changed successfully.".center(100) + Fore.WHITE)
                    input()
                    break

        # 8 - LOGOUT
        elif choice == 8:
            connectObj.close()
            print()
            print(Fore.GREEN + "Signed out from Admin!".center(100) + Fore.WHITE)
            input()
            return 1
        
        # DEFAULT CASE
        else:
            print()
            print(Fore.RED + "Invalid choice! Try again".center(100) + Fore.WHITE)

# startCashier(): A FUNCTION USED FOR CASHIERS LOGIN PROCESS WHICH PROVIDES SOME OPERATIONS TO
# PERFORM. RETURNS 1 INDICATING LOGOUT OR 0 INDICATING EXIT FROM A SYSTEM.
def startCashier():
    connectObj = db.connect("shopMgmt.db")
    cursor = connectObj.cursor()

    sql = '''
    SELECT userName, password FROM users WHERE userType = 1
    '''
    cursor.execute(sql)
    userName, password = cursor.fetchall()[0]

    # sql = '''
    # SELECT userName, password FROM users WHERE userType = 0
    # '''
    # cursor.execute(sql)
    # print(cursor.fetchall()[0])

    while True:
        id = input("\n\tEnter User Id of Cashier: ").strip()
        if id != userName:
            print()
            print(Fore.RED + "No such cashier exists! Please try again.".center(100) + Fore.WHITE)
            continue
        else:
            break
    while True:
        pwd = input("\tEnter your password, " + id + ": ").strip()
        if pwd != password:
            print()
            print(Fore.RED + "Incorrect password! Please try again.".center(100) + Fore.WHITE)
            print()
            continue
        else:
            break
    
    print()
    print(Fore.GREEN + "Login successfull! Welcome, {}.".format(id).center(100) + Fore.WHITE)
    input()

    while True:
        print(Fore.BLUE + "----------Cashier Menu----------".center(100) + Fore.WHITE)
        print(Fore.YELLOW + "\n\tSelect option to perform (0 to shutdown):" + Fore.WHITE)
        print("\t1 - View available products")
        print("\t2 - Generate / Store Bill")
        print("\t3 - Change password")
        print("\t4 - Logout")

        choice = getInt("\n\tEnter your choice: ")
        if choice == 0:
            connectObj.close()
            return 0
        
        elif choice == 1:
            sql = '''
            SELECT * FROM products
            '''
            cursor.execute(sql)
            products = cursor.fetchall()
            print()
            print(tabulate(products, headers=[Fore.YELLOW + 'Product Id.', Fore.YELLOW + 'Product Name', Fore.YELLOW + 'Quantities Avail.', Fore.YELLOW + 'Price each'+ Fore.WHITE], numalign="center", stralign="center"))
            print()
            input()

        elif choice == 2:
            while True:
                customerName = input("\n\tEnter customer name: ")
                if len(customerName) < 4:
                    print()
                    print(Fore.RED + "Name should be atleast 4 characters long! Try again.".center(100) + Fore.WHITE)
                    input()
                else:
                    break
            customerPhone = getPhone("\tEnter 10-digit Phone no.: ")
            date = str(datetime.datetime.now().date())
            print()
            print(Fore.YELLOW + "\n\tAvailable products in the store: " + Fore.WHITE)
            sql = '''
            SELECT * FROM products
            '''
            cursor.execute(sql)
            products = cursor.fetchall()
            print(tabulate(products, headers=[Fore.YELLOW + 'Product Id.', Fore.YELLOW + 'Product Name', Fore.YELLOW + 'Quantities Avail.', Fore.YELLOW + 'Price each'+ Fore.WHITE], numalign="center", stralign="center"))
            input()

            print("\n")
            print(Fore.YELLOW + "\tNow, enter the product details which customer wants to buy: " + Fore.WHITE)
            print()
            items = []
            price = 0
            while True:
                chosen = input("\tKeep entering product id (0 to stop): ")
                if chosen == '0':
                    break
                else:
                    sql = '''
                    SELECT quantity, price FROM products WHERE productId = ?
                    '''
                    cursor.execute(sql, [chosen])
                    prd = cursor.fetchall()
                    if len(prd) == 0:
                        print()
                        print(Fore.RED + "No such product {} is available!".format(chosen).center(100) + Fore.WHITE)
                        input()
                    elif prd[0][0] == 0:
                        print()
                        print(Fore.RED + "Not enough quantity for the product {}.".format(chosen).center(100) + Fore.WHITE)
                        input()
                    else:
                        sql = '''
                        UPDATE products SET quantity = quantity - 1 WHERE productId = ?
                        '''
                        cursor.execute(sql, [chosen])
                        items += [str(chosen)]
                        price += prd[0][1]
            
            if price == 0:
                print()
                print(Fore.RED + "No products were added. Billing failed!".center(100) + Fore.WHITE)
                input()
            else:
                productsPurchased = ', '.join(items)
                sql = '''
                INSERT INTO purchaseHistory(customerName, productIdsPurchased, amountPaid, date, customerPhone)
                VALUES(?, ?, ?, ?, ?)
                '''
                cursor.execute(sql, (customerName, productsPurchased, price, date, customerPhone))
                connectObj.commit()
                print()
                print(Fore.GREEN + "Purchase details has been saved.".center(100) + Fore.WHITE)
                input()
                
        elif choice == 3:
            while True:
                pwd = input("\n\tEnter your current Password: ").strip()
                if pwd != password:
                    print()
                    print(Fore.RED + "Incorrect password! Please try again.".center(100) + Fore.WHITE)
                    continue
                else:
                    break
                
            newPass = input("\tEnter new password (0 to stop changing): ").strip()
            if newPass == '0':
                print()
                print(Fore.RED + "You cancelled to change your password.".center(100) + Fore.WHITE)
                input()
                break
            if len(newPass) < 8:
                print()
                print(Fore.RED + "Password should not be less than 8 characters!.".center(100) + Fore.WHITE)
                print()
            else:
                password = newPass
                sql = '''
                UPDATE users SET password = ? WHERE userType = ?
                '''
                cursor.execute(sql, (password, 1))
                connectObj.commit()
                print()
                print(Fore.GREEN + "Password changed successfully.".center(100) + Fore.WHITE)
                input()

        elif choice == 4:
            connectObj.close()
            print()
            print(Fore.GREEN + "Signed out from Cashier!".center(100) + Fore.WHITE)
            input()
            return 1

# getInt(): A FUNCTION USED TO STRICTLY ACCEPT ONLY INTEGER TYPE OF DATA
def getInt(s):
    while True:
        try:
            return int(input(s))
        except:
            print()
            print(Fore.RED + "Enter Integer only!".center(100) + Fore.WHITE)
            input()

# getPhone(): A FUNCTION USED TO ACCEPT 10 DIGIT PHONE NUMBER
def getPhone(s):
    while True:
        try:
            ph = int(input(s))
            if len(str(ph)) != 10:
                print()
                print(Fore.RED + "Please enter valid 10 digits phone number!".center(100) + Fore.WHITE)
                input()
                continue
            else:
                return ph 
        except:
            print()
            print(Fore.RED + "Enter Integer only!".center(100) + Fore.WHITE)
            input()

# MAIN EXECTION STARTS FROM HERE
print("\n\n")
while True:
    # HOME PAGE OF SYSTEM PROVIDES TO OPTION, ADMIN LOGIN AND CASHIER LOGIN
    initDB()
    print(Fore.BLUE + "----------Shop Management----------".center(100) + Fore.WHITE)
    print(Fore.YELLOW + "\n\tSelect login type (0 to shutdown):" + Fore.WHITE)
    print("\t1 - Admin Login")
    print("\t2 - Cashier Login")

    # USER CHOICE IS ACCEPTED IN choice
    choice = getInt("\n\tEnter your choice: ")

    # EXIT CASE
    if choice == 0:
        exit()
    
    # ADMIN LOGIN
    elif choice == 1:
        if startAdmin():
            continue
        exit(0)
    
    # CASHIER LOGIN
    elif choice == 2:
        if startCashier():
            continue
        exit(0)
    
    # DEFAULT CASE
    else:
        print()
        print(Fore.RED + "Invalid choice! Try again".center(100) + Fore.WHITE)
        print()
