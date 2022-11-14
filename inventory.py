import os
#========The beginning of the class==========
class Shoe:

    #initialising attributes
    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity
    
    #Returns product name
    def get_name(self):
        return self.product

    #Returns product code
    def get_code(self):
        return self.code
        
    #Returns the cost of the shoe
    def get_cost(self):
        return int(self.cost)

    #returns quantity of the shoes
    def get_quantity(self):
        quantity = self.quantity.strip("\n")
        return int(quantity)

    #Returns a string representation of the class
    def __str__(self):
        string = f"""
        Product:    {self.product}
        Code:       {self.cost}
        Made in:    {self.country}
        Price:      {self.cost}
        Quantity:   {self.quantity} 
        """

        return string


#=============Shoe list===========
#Used to store the list of shoes objects
global shoe_list
shoe_list = []


#==========Functions outside the class==============

def delete_shoe(shoe):
    del shoe

#determins if a text file is empty
def is_empty(fileName):
    try:
        if os.path.getsize(fileName) == 0:
            return True
        else:
            return False
    except FileNotFoundError:
        print(f"{fileName} doesn't exist")
        return

def get_codes():
    if is_empty("inventory.txt"):
        return False
    try:
        codes = []
        with open("inventory.txt", "r") as f:
            lines = f.readlines()
            for l in lines:
                list = l.split(",")
                if len(list) > 1:
                    codes.append(list[1])
        return list
    except FileNotFoundError:
        return False


    return False
         
def read_shoes_data():
    #If inventory file exists, read it
    #If not, inform user file doesnt exist
    shoe_list.clear()
    try:
        f = open("inventory.txt", "r")

        #Reading lines in file
        file_lines = f.readlines()
        f.close()

        #Remove line with titles for shoe data
        if len(file_lines) > 0:

            del file_lines[0]
            #iterate through lines and create a Shoe object for each line
            for line in file_lines:
                line_list = line.split(",")

                if len(line_list) > 1:
                    country = line_list[0]
                    code = line_list[1]
                    product = line_list[2]
                    cost = line_list[3]
                    quantity = line_list[4]
                    new_shoe = Shoe(country, code, product, cost, quantity)
                    shoe_list.append(new_shoe)
        print("inventory.txt loaded")
        return True
                
    except FileNotFoundError:   
        print("No inventory.txt file found")
        return False

    
#Allows user to create a new shoe item then
#Adds to shoe list, and writes in inventory.txt file.
def capture_shoes():
    product = input("Please enter the product name: ")
    code = input("Please enter the product code: ")
    code_list = get_codes()
    if code_list is not False:
        while code in code_list:
            code = input("This code already exists, please enter a unique code: ")

    country = input("Where was the product made? ")
    cost = ""
    while cost == "":
        try:
            cost = int(input("How much does the product cost? "))
        except ValueError:
            print("Please enter a number.")

    quantity = ""
    while quantity == "":
        try:
            quantity = int(input("How many do you want to put into stock: "))
        except ValueError:
            print("Please enter a number.")

    new_shoe = Shoe(country, code , product, str(cost) , str(quantity))
    shoe_list.append(new_shoe)

    with open("inventory.txt", "a") as f:
        #adding titles if file is empty
        if is_empty("inventory.txt"):
            f.write("Country,Code,Product,Cost,Quantity\n")

        f.write(f"{country},{code},{product},{cost},{quantity}\n")
        
    print(f"New shoe: {product} added to inventory.")
    read_shoes_data()


#Prints all shoes in inventory in a readable string
def view_all():
    #if data hasnt been imported
        #if data hasnt been imported
    if shoe_list == []:
        #if inventory.txt exists
        if read_shoes_data() == True:
            #checking if inventory.txt is empty    
            if(is_empty("inventory.txt") == True):
                print("inventory.txt is empty")
                return False
        #if inventory.txt doesnt exist: 
        else:
            return False

    print("""========= All Shoes =========""")
    for shoe in shoe_list:
        print(f"""{Shoe.__str__(shoe)}        
    ____________________________""")
    

#Gets shoe with lowest quantity and give user option to update stock
def re_stock():
    lowest_quantity = None
    lowest_shoe = None

    #if data hasnt been imported
    if shoe_list == []:
        #if inventory.txt exists
        if read_shoes_data() == True:
            #checking if inventory.txt is empty    
            if(is_empty("inventory.txt") == True):
                print("inventory.txt is empty")
                return False
        #if inventory.txt doesnt exist: 
        else:
            return False

    for shoe in shoe_list:
        quantity = int(Shoe.get_quantity(shoe)) 
        if lowest_quantity is None or quantity < lowest_quantity:
            lowest_quantity = int(quantity)
            lowest_shoe = shoe
            

    print(f"The lowest quantity shoe is {Shoe.get_name(lowest_shoe)} with {lowest_quantity} remaining.")
    #Asking user how many they would like to add to stock and ensuring it is an int
    add_stock = ""
    while add_stock == "":
        try:
            add_stock = int(input(f"What quantity do you want to add to {Shoe.get_name(lowest_shoe)} stock? " ))
        except ValueError:
            print("Please enter a number.")

    new_stock = lowest_quantity+add_stock
    print(f"""{add_stock} now added to {Shoe.get_name(lowest_shoe)} stock levels
    New quantity:   {new_stock}""")

    #overwriting all lines and changing line of lowest stock shoe
    #to have new added stock
    f = open("inventory.txt", "r")
    lines = f.readlines()
    f.close()

    f = open("inventory.txt", "w")
    for line in lines:
        code = Shoe.get_code(lowest_shoe)
        
        if code not in line:
            f.write(line)
        else:
            new_info = line.split(",")
            country = new_info[0]
            code = new_info[1]
            product = new_info[2]
            cost = new_info[3]
            quantity = new_stock

            Shoe(country,code,product,cost,quantity)
            new_line = f"{country},{code},{product},{cost},{quantity}\n"           
            f.write(new_line)
    
    delete_shoe(lowest_shoe)
    f.close()
    read_shoes_data()   


#Returns shoe information from a code input by user
def search_shoe():
    #if data hasnt been imported
    if shoe_list == []:
        #if inventory.txt exists
        if read_shoes_data() == True:
            #checking if inventory.txt is empty    
            if(is_empty("inventory.txt") == True):
                print("inventory.txt is empty")
                return False
        #if inventory.txt doesnt exist: 
        else:
            return False

    code = input("Please enter the code of the shoe you want to search for: ")
    exists = False
    for shoe in shoe_list:
        shoe_code = str(Shoe.get_code(shoe))
        if shoe_code == code:
            print(shoe)
            exists = True
            break

    if exists is False:
        print("This shoe code doesnt exist, please try again.")


#Returns total value for each item where value = cost*quantity
def value_per_item():
    #if data hasnt been imported
    if shoe_list == []:
        #if inventory.txt exists
        if read_shoes_data() == True:
            #checking if inventory.txt is empty    
            if(is_empty("inventory.txt") == True):
                print("inventory.txt is empty")
                return False
        #if inventory.txt doesnt exist:    
        else:
            return False

    print("=========== Shoe Total Values ===========")
    for shoe in shoe_list:
        cost = Shoe.get_cost(shoe)
        quantity = Shoe.get_quantity(shoe)
        value = cost * quantity
        print(f"""
        Name:           {Shoe.get_name(shoe)}
        Code:           {Shoe.get_code(shoe)}
        Total Value:    {value}
        ---------------------------------------""")
           

#Determines shoe with the highest quantity in stock and 
# prints it as being for sale
def highest_qty():
    high_quantity = None
    high_shoe = None
    #if data hasnt been imported
    if shoe_list == []:
        #if inventory.txt exists
        if read_shoes_data() == True:
            #checking if inventory.txt is empty
            if(is_empty("inventory.txt") == True):
                print("inventory.txt is empty")
                return False
        #if inventory.txt doesnt exist:
        else:
            return False
 
    for shoe in shoe_list:
        quantity = int(Shoe.get_quantity(shoe))
        if high_quantity is None or quantity > high_quantity:
            high_quantity = int(quantity)
            high_shoe = shoe
        
    print(f"""
    FOR SALE:
    {str(high_shoe)}
    """)




#==========Main Menu=============
while True:
    print("""
    Please select one of the options below""")
    menu = input(f"""
    id - import data from inventory.txt file
    a - add new shoe to stock
    va - view all shoes in stock
    rs - restock lowest quantity shoe
    ss - search for a shoe by code
    v - view the total value for each item in stock
    hq - mark the highest quantity item for sale
    e - exit
    :""".lower())
    if menu == "id":
        read_shoes_data()

    elif menu == "a":
        capture_shoes()
    
    elif menu == "va":
        view_all()
    
    elif menu == "rs":
        re_stock()    
        
    
    elif menu == "ss":
        search_shoe()
    
    elif menu == "v":
        value_per_item()
    
    elif menu == "hq":
        highest_qty()
    
    elif menu == "e":
        print("goodbye!")
        exit()
    
    else:
        print("This is an invalid option, please try again")

