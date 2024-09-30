from lib.chatnode_voice import ChatNode
import logging
import os
from datetime import datetime

# Ensure the 'log' folder exists
if not os.path.exists('log'):
    os.makedirs('log')
# Get current date and time for the filename
current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
log_filename = os.path.join('log', f'logfile_{current_time}.log')  # Save inside 'log' folder
# Configure logging with the dynamic filename
logging.basicConfig(filename=log_filename, filemode='a', format='%(asctime)s - %(message)s', level=logging.INFO)
gaol="talk to customer and inquire the customer to give the full information his name and age, if customer don't want the buy just finish done in nan"

messages = [
{"role": "system", "content": "You are a kind helpful call center assestant for the Arena shop , write a respond to customer to inqure the customer name and what is his age . make sure to have the folloing goal {gaol}. start greeting the customer in 20 words."},
]	

status= """ { "done": "true" or "false" or "nan"}"""
output_json_formate=""" { "name":  "  "   ,"age":   "  " }"""
role1="You are a kind helpful call center assistant write a response to the customer."

while True:
    N1=ChatNode(gaol, status,role1,messages,output_json_formate)
    # print(N1)
    results,summary1, json_out, messages=N1.main()
    if results=="true" or results=="nan":
        break
if results=="nan":
    N1.endconv()

logging.info(f'First node results value: {messages} \n {results},\n{summary1}, \n{json_out} ')
####################################################################################################

gaol=f"""  talk to customer and ask the customer if he want his order to be delevered by driver or not so the customer himself will reach the shop after fuew minites, if customer don't want the buy just finish done in nan.  the customer information given "information: {summary1}".  respond to the customer in 30 words."""
print(summary1)
print(">>>>>")
print (gaol)

# new = [
# {"role": "system", "content": f"You are a kind helpful call center assestant in a shop that buy coffee and tea, and want to write a reponse to customer to take his confirmation about his order as follows:  {gaol}"},
# ]	
messages = [
{"role": "system", "content": f"You are a kind helpful call center assestant for the Arena shop , continou the conversation woth the customer and write a respond to customer to inqure the customer name and what is his age . make sure to have the folloing goal {gaol}. start greeting the customer in 20 words."},
]	
messages.append({"role": "system", "content": f"You are a kind helpful call center assestant for the Arena shop , continou the conversation woth the customer and write a respond to customer to make sure to have the folloing goal {gaol}. in 20 words."},
            )

status= """ { "done": "true" or "false" or "nan"}"""
output_json_formate=""" { "delivary: "yes" or "No",}"""
role1="You are a kind helpful call center assistant."



while True:
    N2=ChatNode(gaol, status,role1,messages,output_json_formate)
    # print(N2)
    results,summary2, json_out2, messages=N2.main()
    if results=="true" or results=="nan":
        break
if results=="nan":
    N2.endconv()

logging.info(f'Second node results value: {messages} \n {results},\n{summary2}, \n{json_out2} ')
#################################################################################################3

menu = {
    "Espresso": 2.50,
    "Cappuccino": 3.75,
    "Latte": 4.00,
    "Mocha": 4.50,
    "Iced Americano": 3.00,
    "Caramel Macchiato": 4.25,
    "Tea": 2.00,
    "Turkish Coffee": 3.50
}
menuq = {
    "Espresso": 1,
    "Cappuccino": 1,
    "Latte": 0,
    "Mocha": 0,
    "Iced Americano": 0,
    "Caramel Macchiato": 2,
    "Tea": 0,
    "Turkish Coffee": 0
}
menuS="Espresso, Cappuccino, Latte, Mocha, Iced Americano, Caramel Macchiato, Tea, Turkish Coffee"
gaol=f"""  continou the conversation woth the customer and talk to customer and ask the customer what he requisted from the shop menu tht is shown in the website, and if he did't see the menu tell the customer more about is, the menu is {menuS}, and if customer don't want the buy just finish done in nan.  the customer information given "information: {summary1} and {summary2}".  respond to the customer in 30 words."""
status= """ { "done": "true" or "false" or "nan"}"""
output_json_formate= f""" "item": quantity, and this is a sample of the json output by filling the table {menuq}"""
messages.append({"role": "system", "content": f"You are a kind helpful call center assestant for the Arena shop , continou the conversation woth the customer and write a respond to customer to make sure to have the folloing goal {gaol}. in 20 words."},
            )
cc=True
while cc:
    while True:
        N3=ChatNode(gaol, status,role1,messages,output_json_formate)
        results,summary3, json_out3, messages=N3.main()
        if results=="true" or results=="nan":
            break
    if results=="nan":
        N3.endconv()

    logging.info(f'Third node results value: {messages} \n {results},\n{summary3}, \n{json_out3} ')
    ###########################################################################################

    # Define the menu prices
    menu_prices = {
        "Espresso": 2.50,
        "Cappuccino": 3.75,
        "Latte": 4.00,
        "Mocha": 4.50,
        "Iced Americano": 3.00,
        "Caramel Macchiato": 4.25,
        "Tea": 2.00,
        "Turkish Coffee": 3.50
    }

    # Define the quantities
    # Convert the JSON string to a Python dictionary
    import json
    menu_quantities = json.loads(json_out3)

    # Calculate the total price
    total_price = sum(menu_prices[item] * menu_quantities.get(item, 0) for item in menu_prices)
    print(f"Total price: ${total_price:.2f}")

    gaol=f"""  continou the conversation woth the customer and talk to customer and ask the customer to confirm his order details, his order is summarized in: {summary3}, and the total price in dollar is {total_price} , and if customer don't want the buy just finish done in nan.   respond to the customer in 30 words."""
    status= """ { "done": "true" or "false" or "nan"}"""
    output_json_formate=""" { "confirmed: "yes" or "No",}"""
    messages.append({"role": "system", "content": f"You are a kind helpful call center assestant for the Arena shop , continou the conversation woth the customer and write a respond to customer to make sure to have the folloing goal {gaol}. in 20 words."},
                )


    N4=ChatNode(gaol, status,role1,messages,output_json_formate)
    results,summary4, json_out4, messages=N4.main()
    if results=="true" or results=="nan":
        cc=False
        break
    if results=="nan":
        N4.endconv()
    logging.info(f'Furth node results value: {messages} \n {results},\n{summary4}, \n{json_out4} ')
    menuS="Espresso, Cappuccino, Latte, Mocha, Iced Americano, Caramel Macchiato, Tea, Turkish Coffee"
    gaol=f"""  talk to customer and ask the customer what he requisted from the shop menu , and if customer don't want the buy just finish done in nan.  the customer information given "information: {summary1} and {summary2} and {summary4}".  respond to the customer in 30 words."""
    status= """ { "done": "true" or "false" or "nan"}"""
    output_json_formate= f""" "item": quantity, and this is a sample of the json output by filling the table {menuq}"""
    messages.append({"role": "system", "content": f"You are a kind helpful call center assestant for the Arena shop , write a respond to customer to make sure to have the folloing goal {gaol}. in 20 words."},
                )
logging.info(f'The end of the Furth node results value: {messages} \n {results},\n{summary4}, \n{json_out4} ')

###########################################################################################
#
dd=json.loads(json_out2)
delivery_value = dd.get("delivery")
if delivery_value=="yes":
    gaol=f"""  talk to customer and ask the customer about his address , and if customer don't want the buy just finish done in nan.  the customer information given "information: {summary1} and {summary2} and {summary4}".  respond to the customer in 20 words."""
    status= """ { "done": "true" or "false" or "nan"}"""
    output_json_formate= f""" "address": "  "   """
    messages.append({"role": "system", "content": f"You are a kind helpful call center assestant for the Arena shop , continou the conversation woth the customer and write a respond to customer to make sure to have the folloing goal {gaol}. in 20 words."},
                )
    while True:
        N5=ChatNode(gaol, status,role1,messages,output_json_formate)
        results,summary5, json_out5, messages=N5.main()
        if results=="true" or results=="nan":
            break
    if results=="nan":
        N5.endconv()

    logging.info(f'Fifth node results value: {messages} \n {results},\n{summary5}, \n{json_out5} ')



