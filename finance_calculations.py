import math

# Program built to calculate Investment or Bond interest total repayments
# User enters their chosen calculation then inputs the details in relation to the payments
# Ask the user for an input
INTRO = "Investment - to calculate the amount of interest you'll earn on your investment\nBond - to calculate the amount you'll have to pay on a home loan\n"

print(INTRO)
user_input = input("Please enter either 'Investment' or 'Bond' to proceed: ")

# If the user enters 'Investment' - note: this syntax allows the user to enter any casing
if user_input.lower() == "investment":
    deposit = int(input("How much money are you depositing?:  \n£"))
    exchange_rate = int(input("What is the exchange rate?: \n%"))
    invest_years = int(input("How many years are you planning to invest?: \n"))
    # User has a choice between Simple or Compound
    interest_type = input("Do you want Simple or Compound interest?: \n")        
    
    # Simple path starts here
    if interest_type.lower() == "simple":
        simple_interest = int(((exchange_rate/100) * invest_years +1) * deposit)
        print(f"Your Investment interest has been calculated as follows: £{simple_interest}\n\n")

    # Compound path starts here
    if interest_type.lower() == "compound":
        # Compound interest calculation
        compound_interest = int(deposit * math.pow(((exchange_rate/100)+1),invest_years))
        # Calculation for additional charges
        additional_pay = int((compound_interest)-deposit)
        print(f"Your total payment (including interest) is calculated as £{compound_interest}\n")
        print(f"You will be paying £{additional_pay}, in addition to your deposit.\n\n")

    elif interest_type.lower() != "compound" or "simple":
        print("Error: Your selection is invalid. Please enter 'simple' or 'compound'.")

# Separate commands for each path - Bond
elif user_input.lower() == "bond":
    house_value = int(input("How much money are you depositing?: \n£"))
    interest_input = float(input("Please enter the interest rate: \n%"))/100
    # Calculates the interest rate as per the input divided by 12
    interest_rate = float(interest_input/12)
    duration = int(input("Across how many months are you planning to repay the bond?: \n"))
    # Used to support calculation outlined below
    repayment_calc = (interest_rate+1)
    repayment = int((interest_rate * house_value)) / float(abs(1-(1-interest_rate) ** (- duration)))
    # Shows the output as presented in simple terms
    print(f"Your repayment is calculated as £{repayment:.2f} per month\n\n")      
    
else:
    print("Error!")
print("\nGoodbye.")
