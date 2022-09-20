import gspread
from google.oauth2.service_account import Credentials
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')
# sales = SHEET.worksheet('sales')
# data = sales.get_all_values()
# print(data)

def get_sales_data():
    """
    Get sales figures input from the user using a While loop to ensure valid string:
    6 integers, separated by commas
    """
    while True:
        print('Please enter the sales data')
        print('The info should be separated by commas')
        print('Example: 10,20,30,40,50 \n')
        data_str = input("Enter your data here: ")
        sales_data = data_str.split(',')
        if validate_data(sales_data):
            print('Data is valid')
            break
    return sales_data

def validate_data(values):
    """
    Inside the try, converts all string values to integers
    Raises value error if strings can't be converted to int
    or if there aren't exactly 6 values
    """
    try:
        [int(value) for value in values]
        if len(values) !=6:
            raise ValueError(f"Exactly 6 entries are required; you provided only {len(values)}")
    except ValueError as e:
        print(f"invalid data: {e}, please try again \n")
        return False

    return True

def update_sales_worksheet(data):
    """
    Adds data row to bottom of Sales worksheet in love_sandwiches spreadsheet
    """
    print('updating sales worksheet \n')
    sales_worksheet = SHEET.worksheet('sales')
    sales_worksheet.append_row(data)
    print('sales worksheet updated successfully. \n')


data = get_sales_data()
print(data)
sales_data = [int(num) for num in data]
update_sales_worksheet(sales_data)