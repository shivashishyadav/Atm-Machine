from tkinter import *
from tkinter import messagebox
import json

timmy = Tk()
timmy.title("My A.T.M Machine")
timmy.config(padx=50, pady=50)

BUTTON_FONT = ("Helvetica", 12, "bold")
PIN_FONT = ("Verdana", 12, "underline")
LABEL_FONT = ("Times New Roman", 14, "normal")
LABEL_BG = "mintcream"
INPUT_FONT = ("Georgia", 12, "bold")
BUTTON_BG = "blue"
BUTTON_FG = "white"
INPUT_FIELD_BORDER_WIDTH = 3
INPUT_FIELD_BORDER_TYPE = "sunken"

# =====================================READING THE JSON DATA==================================
try:
    with open("data.json", "r") as file:
        data = json.load(file)
        total_cash = data["total_cash"]
        accounts = data["accounts"]
except FileNotFoundError:
    # Default values if file does not exist
    total_cash = 100000000
    accounts = [
        {"pin": 1334, "balance": 1000},
        {"pin": 1635, "balance": 2000},
        # Add other accounts as needed
    ]


# =====================================CLEARING INPUT FIELDS LOGIC==================================
def clear_input_fields():
    """This function clears the input fields"""
    pin_input.delete(0, END)
    debit_input.delete(0, END)
    generate_pin_input.delete(0, END)


# =====================================CASH DEBITING LOGIC==================================
def get_cash():
    """Handle cash withdrawal logic"""
    global total_cash
    try:
        # Get and validate PIN
        pin_str = pin_input.get()
        if not pin_str.isdigit():
            raise ValueError("Enter a valid PIN")
        pin = int(pin_str)

        # Get and validate money
        money_str = debit_input.get()
        if not money_str.replace(".", "", 1).isdigit():
            raise ValueError("Enter a valid amount of money")
        money = float(money_str)

        if money <= 0:
            raise ValueError("Amount should be greater than zero")

        # Process the transaction
        account_found = False
        for account in accounts:
            if account["pin"] == pin:
                account_found = True
                if money <= account["balance"] and money <= total_cash:
                    account["balance"] -= money
                    total_cash -= money
                    remain_input_label.config(text=f"$ {account['balance']}")
                    messagebox.showinfo(
                        title="Debit From ATM",
                        message=f"Successfully debited $ {money} from your account.",
                    )
                    clear_input_fields()
                    return
                else:
                    if money > account["balance"]:
                        raise ValueError("Insufficient funds in account")
                    elif money > total_cash:
                        raise ValueError("Insufficient cash in the ATM")

        if not account_found:
            raise ValueError("Invalid PIN")

    except ValueError as e:
        messagebox.showerror(title="Input Error", message=str(e))
        clear_input_fields()


# =====================================Generate a new ATM PIN==================================


def generate_new():
    """This function generate a unique card pin and by default add $ 1000 to the user account"""
    new_pin_str = generate_pin_input.get()
    if len(new_pin_str) != 4 or not new_pin_str.isdigit():
        messagebox.showerror(title="Input Error", message="Enter a 4-digit number")
        return
    try:
        new_pin = int(new_pin_str)

        # Check for existing PINs
        all_pin = [account["pin"] for account in accounts]
        if new_pin in all_pin:
            messagebox.showinfo(
                title="Info", message="Pin already exists, Please choose another one."
            )
        else:
            # Add new account record
            global data
            record = {"pin": new_pin, "balance": 1000}
            data["accounts"].append(record)
            with open("data.json", "w") as file:
                json.dump(data, file, indent=4)

            # Provide feedback
            messagebox.showinfo(
                title="Success",
                message=f"New PIN generated: {new_pin}. Default balance of $1000 added.",
            )
            clear_input_fields()

    except ValueError:
        messagebox.showerror(
            title="Input Error", message="Enter a valid 4-digit number"
        )


# =====================================UI SET-UP==================================

# Label for asking card pin
pin_label = Label(text="Enter Card Pin", font=LABEL_FONT, anchor="w")
pin_label.grid(row=0, column=0, sticky="w")

# input field for entering the card pin
pin_input = Entry(
    font=PIN_FONT, bd=INPUT_FIELD_BORDER_WIDTH, relief=INPUT_FIELD_BORDER_TYPE
)
pin_input.grid(row=0, column=1, pady=5)
pin_input.focus()

# label for asking money to be debit
debit_label = Label(text="How many money you want?", font=LABEL_FONT, anchor="w")
debit_label.grid(row=1, column=0, sticky="w")

# input field for entering the money you want
debit_input = Entry(
    font=INPUT_FONT, bd=INPUT_FIELD_BORDER_WIDTH, relief=INPUT_FIELD_BORDER_TYPE
)
debit_input.grid(row=1, column=1)

# button for getting the money
get_cash = Button(
    text="Get Cash",
    width=43,
    font=BUTTON_FONT,
    fg=BUTTON_FG,
    bg=BUTTON_BG,
    command=get_cash,
)
get_cash.grid(row=2, column=0, columnspan=2, pady=15)

# label for showing the remaining balance
remain_label = Label(text="Remaining balance in accounts", font=LABEL_FONT, anchor="w")
remain_label.grid(row=3, column=0, sticky="w")

# entry to show the remaining money balance
remain_input_label = Label(text="0", font=LABEL_FONT)
remain_input_label.grid(row=3, column=1)


seperator = Label(
    text="---------------------------OR--------------------------",
    font=("Courier New", 10, "bold italic"),
    anchor="w",
)
seperator.grid(row=4, column=0, columnspan=2, pady=15, sticky="w")

# For new user generate the new pin
generate_pin = Label(text="Generate a new pin", font=LABEL_FONT, anchor="w")
generate_pin.grid(row=5, column=0, sticky="w")

generate_pin_input = Entry(
    font=PIN_FONT, bd=INPUT_FIELD_BORDER_WIDTH, relief=INPUT_FIELD_BORDER_TYPE
)
generate_pin_input.grid(row=5, column=1)

generate_btn = Button(
    text="Generate New Pin",
    font=BUTTON_FONT,
    width=43,
    bg=BUTTON_BG,
    fg=BUTTON_FG,
    command=generate_new,
)
generate_btn.grid(row=6, column=0, columnspan=2, pady=5)

timmy.mainloop()
