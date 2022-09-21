import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

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

def update_worksheet(data, worksheet):
    """
    Adds data row to bottom of Sales worksheet in love_sandwiches spreadsheet
    """
    print(f'updating {worksheet} worksheet \n')
    updated_worksheet = SHEET.worksheet(worksheet)
    updated_worksheet.append_row(data)
    print(f'{worksheet} worksheet updated successfully. \n')

def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and see what surplus there is
    """
    print('calculating surplus...\n')
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    return surplus_data

def get_last_5_entries():
    """
    Collects columns of data from sales worksheet
    """
    sales = SHEET.worksheet('sales')
    columns = []
    for ind in range(1,7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    return columns

def calculate_stock_data(data):
    """
    Takes the stock data and makes a recommended number for the following week
    """
    print('calculating stock data... \n')
    new_stock_data = []
    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column)/len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))
    return new_stock_data

# def update_surplus_worksheet(value):
#     """
#     Add a row with the surplus for the day into the surplus worksheet
#     """
#     print('updating surplus worksheet \n')
#     surplus_worksheet = SHEET.worksheet('surplus')
#     surplus_worksheet.append_row(value)
#     print('surplus worksheet updated \n')


def main():
    """
    Runs all programme functions
    """
    data = get_sales_data()
    print(data)
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")
    sales_columns = get_last_5_entries()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, "stock")
    print(stock_data)

print("welcome to love sandwiches")
main()
