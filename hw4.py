#Abir Ahmed
import unittest

# The Customer class
# The Customer class represents a customer who will order from the stalls.
class Customer: 
    # Constructor
    def __init__(self, name, wallet = 100):
        self.name = name
        self.wallet = wallet

    # Reload some deposit into the customer's wallet.
    def reload_money(self,deposit):
        self.wallet += deposit

    # The customer orders the food and there could be different cases   
    def validate_order(self, cashier, stall, item_name, quantity):
        if not(cashier.has_stall(stall)):
            print("Sorry, we don't have that vendor stall. Please try a different one.")
        elif not(stall.has_item(item_name, quantity)):  
            print("Our stall has run out of " + item_name + " :( Please try a different stall!")
        elif self.wallet < stall.compute_cost(quantity): 
            print("Don't have enough money for that :( Please reload more money!")
        else:
            bill = cashier.place_order(stall, item_name, quantity) 
            self.submit_order(cashier, stall, bill) 
    
    # Submit_order takes a cashier, a stall and an amount as parameters, 
    # it deducts the amount from the customer’s wallet and calls the receive_payment method on the cashier object
    def submit_order(self, cashier, stall, amount):
        self.wallet = self.wallet - amount
        cashier.receive_payment(stall, amount)

    # The __str__ method prints the customer's information.    
    def __str__(self):
        return "Hello! My name is " + self.name + ". I have $" + str(self.wallet) + " in my payment card."


# The Cashier class
# The Cashier class represents a cashier at the market. 
class Cashier:

    # Constructor
    def __init__(self, name, directory =[]):
        self.name = name
        self.directory = directory[:] # make a copy of the directory

    # Whether the stall is in the cashier's directory
    def has_stall(self, stall):
        return stall in self.directory

    # Adds a stall to the directory of the cashier.
    def add_stall(self, new_stall):
        self.directory.append(new_stall)

    # Receives payment from customer, and adds the money to the stall's earnings.
    def receive_payment(self, stall, money):
        stall.earnings += money

    # Places an order at the stall.
	# The cashier pays the stall the cost.
	# The stall processes the order
	# Function returns cost of the order, using compute_cost method
    def place_order(self, stall, item, quantity):
        stall.process_order(item, quantity)
        return stall.compute_cost(quantity) 
    
    # string function.
    def __str__(self):

        return "Hello, this is the " + self.name + " cashier. We take preloaded market payment cards only. We have " + str(sum([len(category) for category in self.directory.values()])) + " vendors in the farmers' market."

## Complete the Stall class here following the instructions in HW_4_instructions_rubric
class Stall:

    def __init__(self, name, inventory, cost = 7, earnings = 0):
        self.nama = name
        self.inventory = inventory
        self.cost = cost
        self.earnings = earnings

    def process_order(self, food_name, quantity):
        if self.has_item(food_name, quantity):
            self.inventory[food_name] = self.inventory[food_name] - quantity
            self.earnings = self.earnings + (quantity * self.cost)
        else:
            pass

    def has_item(self, food_name, quantity):
        if not(food_name in self.inventory):
            return False
        elif self.inventory[food_name] >= quantity:
            return True
        else:
            return False

    def stock_up(self, food_name, quantity):
        if food_name in self.inventory:
            self.inventory[food_name] = self.inventory[food_name] + quantity
        else:
            self.inventory[food_name] = quantity

    def compute_cost(self, quantity):
        return (quantity * self.cost)

    def __str__(self):
        keys = ""
        for item in self.inventory:
            keys = keys + item + ","
        keys = keys[0:-2]
        keys = keys.lower()
        return "Hello, we are " + self.name + ". This is the current menu" + keys + ". We charge $" + str(self.cost) + " per item. We have $" + str(self.earnings) + " in total."

class TestAllMethods(unittest.TestCase):
    
    def setUp(self):
        inventory = {"Burger":40, "Taco":50}
        self.f1 = Customer("Ted")
        self.f2 = Customer("Morgan", 150)
        self.s1 = Stall("The Grill Queen", inventory, cost = 10)
        self.s2 = Stall("Tamale Train", inventory, cost = 9)
        self.s3 = Stall("The Streatery", inventory)
        self.c1 = Cashier("West")
        self.c2 = Cashier("East")
        #the following codes show that the two cashiers have the same directory
        for c in [self.c1, self.c2]:
            for s in [self.s1,self.s2,self.s3]:
                c.add_stall(s)

	## Check to see whether constructors work
    def test_customer_constructor(self):
        self.assertEqual(self.f1.name, "Ted")
        self.assertEqual(self.f2.name, "Morgan")
        self.assertEqual(self.f1.wallet, 100)
        self.assertEqual(self.f2.wallet, 150)

	## Check to see whether constructors work
    def test_cashier_constructor(self):
        self.assertEqual(self.c1.name, "West")
        #cashier holds the directory - within the directory there are three stalls
        self.assertEqual(len(self.c1.directory), 3) 

	## Check to see whether constructors work
    def test_truck_constructor(self):
        self.assertEqual(self.s1.name, "The Grill Queen")
        self.assertEqual(self.s1.inventory, {"Burger":40, "Taco":50})
        self.assertEqual(self.s3.earnings, 0)
        self.assertEqual(self.s2.cost, 9)

	# Check that the stall can stock up properly.
    def test_stocking(self):
        inventory = {"Burger": 10}
        s4 = Stall("Misc Stall", inventory)

		# Testing whether stall can stock up on items
        self.assertEqual(s4.inventory, {"Burger": 10})
        s4.stock_up("Burger", 30)
        self.assertEqual(s4.inventory, {"Burger": 40})
        
    def test_make_payment(self):
		# Check to see how much money there is prior to a payment
        previous_custormer_wallet = self.f2.wallet
        previous_earnings_stall = self.s2.earnings
        
        self.f2.submit_order(self.c1, self.s2, 30)

		# See if money has changed hands
        self.assertEqual(self.f2.wallet, previous_custormer_wallet - 30)
        self.assertEqual(self.s2.earnings, previous_earnings_stall + 30)


	# Check to see that the server can serve from the different stalls
    def test_adding_and_serving_stall(self):
        c3 = Cashier("North", directory = [self.s1, self.s2])
        self.assertTrue(c3.has_stall(self.s1))
        self.assertFalse(c3.has_stall(self.s3)) 
        c3.add_stall(self.s3)
        self.assertTrue(c3.has_stall(self.s3))
        self.assertEqual(len(c3.directory), 3)


	# Test that computed cost works properly.
    def test_compute_cost(self):
        self.assertEqual(self.s1.compute_cost(5), 50)
        self.assertEqual(self.s3.compute_cost(6), 42)

	# Check that the stall can properly see when it is empty
    def test_has_item(self):
        # Set up to run test cases

        # Test to see if has_item returns True when a stall has enough items left
        # Please follow the instructions below to create three different kinds of test cases 
        # Test case 1: the stall does not have this food item: 
        self.assertEqual(self.s1.has_item("Quesadilla",2), False)
        # Test case 2: the stall does not have enough food item: 
        self.assertEqual(self.s1.has_item("Burger", 45), False)
        # Test case 3: the stall has the food item of the certain quantity: 
        self.assertEqual(self.s1.has_item("Burger", 19), True)

	# Test validate order
    def test_validate_order(self):
		# case 1: test if a customer doesn't have enough money in their wallet to order
        print("test_validate_order case 1:")
        self.f1.validate_order(self.c1, self.s1, "Burger", 20)
        print("Should print: Don't have enough money for that :( Please reload more money!")
		# case 2: test if the stall doesn't have enough food left in stock
        print("test_validate_order case 2:")
        self.s2.stock_up("Pizza", 2)
        self.f1.validate_order(self.c2, self.s2, "Pizza", 4)
        print("Should print: Our stall has run out of Pizza :( Please try a different stall!")
		# case 3: check if the cashier can order item from that stall
        print("test_validate_order case 3:")
        self.s4 = Stall("Extra", {"Pizza":3, "Pasta":45})
        self.f2.validate_order(self.c2, self.s4, "Taco", 3)
        print("Should print the following: Sorry, we don't have that vendor stall. Please try a differnt one.")

    # Test if a customer can add money to their wallet
    def test_reload_money(self):
        print("test_reloud_money: starting with not enough-")
        self.f1.validate_order(self.c1,self.s1, "Burger", 20)
        print("Adding money. Customer should have enough to buy 20 burgers so 20 will remain in Stall's inventory.")
        self.f1.reload_money(102)
        self.f1.validate_order(self.c1, self.s1, "Burger", 20)
        print(self.s1__str__())
    
### Write main function
def main():
    #Create different objects
    invent_1 = {'Walking Taco': 15, 'Burrito': 10, 'Quesadilla': 5}
    invent_2 = {'Smoothie': 8, 'Banana Bread': 20, 'Parfait': 14}

    cust_1 = Customer("Adam", 105)
    cust_2 = Customer("Beth", 74)
    cust_3 = Customer("Charlie", 60)

    stall_1 = Stall("Sabrosa", invent_1, cost=6)
    stall_2 = Stall("Morningside", invent_2, cost=10)

    cashier_1 = Cashier("Dave", [stall_1])
    cashier_2 = Cashier("Eddie", [stall_1, stall_2]) 

    #Try all cases in the validate_order function
    #Below you need to have *each customer instance* try the four cases
    #case 1: the cashier does not have the stall 
    print("Cases where cashier does not have the stall:")
    cust_1.validate_order(cashier_1, stall_2, "Parfait", 12)
    cust_2.validate_order(cashier_1, stall_2, "Parfait", 12)
    cust_3.validate_order(cashier_1, stall_2, "Banana Bread", 3)
    #case 2: the casher has the stall, but not enough ordered food or the ordered food item
    print("Cases where cashier has the stall, but not enough ordered food or the ordered food item:")
    cust_1.validate_order(cashier_1, stall_1, "Parfait", 2)
    cust_2.validate_order(cashier_2, stall_2, "Banana Bread", 30)
    cust_3.validate_order(cashier_2, stall_1, "Quesadilla", 6)
    #case 3: the customer does not have enough money to pay for the order:
    print("Cases where the customer does not have enough money to pay for the order:") 
    cust_1.validate_order(cashier_2, stall_2, "Banana Bread", 11)
    cust_2.validate_order(cashier_2, stall_2, "Parfait", 9)
    cust_3.validate_order(cashier_1, stall_1, "Walking Taco", 11)
    #case 4: the customer successfully places an order
    print("Cases where the orders go though. Nothing should be printed after this:")
    cust_1.validate_order(cashier_1, stall_1, "Walking Taco", 2)
    cust_2.validate_order(cashier_2, stall_1, "Quesadilla", 2)
    cust_3.validate_order(cashier_2, stall_2, "Banana Bread", 3)

    pass

if __name__ == "__main__":
	main()
	print("\n")
	unittest.main(verbosity = 2)
