import re
import getpass
import time
from utilities import generate_account_number,encryptPassword

def register(conn, cursor, MINIMUM_DEPOSIT):

    global user_id

    fullname = input("Enter your fullname: ")


    # Data Clean up
    fullname = fullname.strip()

    # Fullname Validation

    # Empty name rejected
    if fullname == "":
        print("Fullname is required")
        fullname = input("Enter your fullname: ")
       

    # fullname must be greater than 4 characters
    if len(fullname) < 4:
        print("Fullname must not be less than 4 characters")
        fullname = input("Enter your fullname: ")
       
    
    # fullname must not be more than 255 characters
    if len(fullname) > 255:
        print("Fullname must be not more than 255 characters")
        fullname = input("Enter your fullname: ")
        
    
    # fullname must conatin alpha characters i.e. letters and spaces
    if not re.match("^[a-zA-Z ]+$", fullname):
        print("Fullname must contain only letters and spaces")
        fullname = input("Enter your fullname: ")
        

    username = input("Enter your username: ")
    
    # Username validation
    # Empty username rejected
    if username == "":
        print("Username is required")
        username = input("Enter your username: ")
        
    

     # username must be greater than 3 characters
    if len(username) < 3:
        print("Username must not be less than 3 characters")
        username = input("Enter your username: ")
        
    
    # username must not be more than 255 characters
    if len(username) > 20:
        print("Username must be not more than 20 characters")
        username = input("Enter your username: ")
        
    
    # Username contains alpha numeric and underscores
    if not re.match("^[a-zA-Z0-9_]+$", username):
        print("Username must contain only letters, numbers and underscores")
        username = input("Enter your username: ")
         
    #CHECK USERNAME ALREADY EXIST

    cursor.execute(
        """
            SELECT * FROM users WHERE username = ?;
        """, (username,)
    )

    user = cursor.fetchone()

    if user:
        print("Username already exist")
        username = input("Enter another username: ")
       
    
    password = getpass.getpass(prompt='Enter your password: ')
   
    # Password Validation

    # Empty Password rejected
    if password == "":
        print("Password is required")
        password = getpass.getpass(prompt='Enter your password: ')
        

     # Password must be greater than 8 characters
    if len(password) < 8:
        print("Password must not be less than 8 characters")
        password = getpass.getpass(prompt='Enter your password: ')
    
    if len(password) > 30:
        print("Password must not be more than 30 characters")
        password = getpass.getpass(prompt='Enter your password: ')
        
    # Password MUST contain at least 1 Uppercase letter, 1 lowercase letter, 1 number and 1 special character
    if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", password):
        print("Password must contain at least 1 Uppercase letter, 1 lowercase letter, 1 number and 1 special character")
        password = getpass.getpass(prompt='Enter your password: ')



    
    # Encrypt Password
    hashed_password = encryptPassword(password)
    

    # Generate Account Number
    accountExist = True
    account_number = None

    while accountExist:
        
        account_number = generate_account_number()
        # Check if account number already exist

        cursor.execute(
            """
                SELECT * FROM users WHERE account_number = ?;
            """, (account_number,)
        )

        accountExist = cursor.fetchone()


    # Initial Deposit
    initial_deposit = input("Enter your initial deposit: ")

    # Initial Deposit Validation
    if initial_deposit == "":
        print("Initial deposit is required")
        initial_deposit = input("Enter your initial deposit: ")
        
    
    # Initial Deposit must be a number
    if not re.match("^[0-9]+$", initial_deposit):
        print("Initial deposit must be a number")
        initial_deposit = input("Enter your initial deposit: ")
    
    # Cast to float
    initial_deposit = float(initial_deposit)

    if initial_deposit < 0:
        print("Initial deposit must be a positive number")
        initial_deposit = input("Enter your initial deposit: ")

    if initial_deposit < MINIMUM_DEPOSIT:
        print(f"Initial deposit must be at least {MINIMUM_DEPOSIT}")
        initial_deposit = input("Enter your initial deposit: ")

    
    # Balance 

    balance = initial_deposit

    # INSERT INTO DATABASE

    
    cursor.execute(
        """
            INSERT INTO users (
                fullname, 
                username, 
                password, 
                balance,
                account_number)
            VALUES (?, ?, ?, ?, ?);
        """, (fullname, 
              username, 
              hashed_password, 
              balance, 
              account_number)
    )

  
    conn.commit()
    print("Loading... \n")
    time.sleep(3)

    print("Registration successful", "")
    print("-------------------------------------------")
    print(f"Your account number is {account_number}")
    print("-------------------------------------------\n")