# coffee_machine.py

import streamlit as st
from coffee_machine_data import MENU, RESOURCES, COIN_VALUES

resources = RESOURCES.copy()
money = 0.0

def is_resource_sufficient(order_ingredients):
    """Check if there are enough resources to make the coffee."""
    for item in order_ingredients:
        if order_ingredients[item] > resources[item]:
            st.write(f"Sorry, there is not enough {item}.")
            return False
    return True

def process_coins():
    """Process coins inserted by the user and return the total."""
    st.write("Please insert coins.")
    total = 0
    for coin, value in COIN_VALUES.items():
        total += st.number_input(f"How many {coin}?", min_value=0) * value
    return total

def is_transaction_successful(money_received, drink_cost):
    """Return True if the payment is accepted, or False if it is insufficient."""
    if money_received >= drink_cost:
        global money
        change = round(money_received - drink_cost, 2)
        st.write(f"Here is ${change} in change.")
        money += drink_cost
        return True
    else:
        st.write("Sorry, that's not enough money. Money refunded.")
        return False

def make_coffee(drink_name, order_ingredients):
    """Deduct the required ingredients from the resources."""
    for item in order_ingredients:
        resources[item] -= order_ingredients[item]
    st.write(f"Here is your {drink_name}. Enjoy!")

def coffee_machine():
    """Main function to run the coffee machine."""
    global money

    st.title("Coffee Machine")
    
    choice = st.selectbox("What would you like?", ("espresso", "latte", "cappuccino", "report", "off"))

    if choice == "off":
        st.write("Turning off the coffee machine.")
    elif choice == "report":
        st.write(f"Water: {resources['water']}ml")
        st.write(f"Milk: {resources['milk']}ml")
        st.write(f"Coffee: {resources['coffee']}g")
        st.write(f"Money: ${money}")
    elif choice in MENU:
        drink = MENU[choice]
        if is_resource_sufficient(drink["ingredients"]):
            payment = process_coins()
            if is_transaction_successful(payment, drink["cost"]):
                make_coffee(choice, drink["ingredients"])
    else:
        st.write("Invalid choice, please choose again.")

if __name__ == "__main__":
    coffee_machine()
