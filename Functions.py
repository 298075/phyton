import csv
import os

def verify_user(ic_number, password):
    """
    Verify the user's credentials by checking if the IC number is 12 digits long
    and if the password matches the last 4 digits of the IC number.
    """
    return len(ic_number) == 12 and ic_number[-4:] == password

def calculate_tax(income, tax_relief):
    """
    Calculate the tax payable based on Malaysian tax rates.
    """
    net_income = income - tax_relief
    if net_income <= 0:
        return 0
    elif net_income <= 50000:
        return net_income * 0.1
    elif net_income <= 100000:
        return 5000 + (net_income - 50000) * 0.2
    else:
        return 15000 + (net_income - 100000) * 0.3

def calculate_total_relief(individual=True, spouse_income=0, num_children=0,
                           medical_expenses=0, lifestyle_expenses=0,
                           education_fees=0, parental_support=0):
    """
    Calculate the total relief based on the conditions specified.
    """
    total = 0
    if individual:
        total += 9000  # Individual relief
    if spouse_income <= 4000:
        total += 4000  # Spouse relief (if spouse income is <= RM4,000)
    total += min(num_children, 12) * 8000  # Child relief, max 12 children
    total += min(medical_expenses, 8000)  # Medical expenses relief
    total += min(lifestyle_expenses, 2500)  # Lifestyle expenses relief
    total += min(education_fees, 7000)  # Education fees relief
    total += min(parental_support, 5000)  # Parental support relief
    return total

def generate_new_user_id(filename="user_data.csv"):
    """
    Generate a new user ID, e.g., user001, user002, etc.
    """
    if not os.path.exists(filename):
        return "user001"
    max_id = 0
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip the header
        for row in reader:
            if row and row[0].startswith("user"):
                try:
                    num = int(row[0][4:])
                    if num > max_id:
                        max_id = num
                except ValueError:
                    continue
    return f"user{max_id + 1:03d}"

def is_registered(user_id, filename="user_data.csv"):
    """
    Check if the user is already registered.
    """
    if not os.path.exists(filename):
        return False
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[0] == user_id:
                return True
    return False

def save_to_csv(data, filename="user_data.csv"):
    """
    Save the user data to a CSV file.
    """
    try:
        file_exists = os.path.exists(filename)
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(['ID', 'IC Number', 'Income', 'Tax Relief', 'Tax Payable'])
            writer.writerow(data)
        print("✅ Data saved to CSV.")
    except Exception as e:
        print(f"❌ Error saving data to CSV: {e}")

def read_from_csv(filename="user_data.csv"):
    """
    Read and display all records from the CSV file.
    """
    if not os.path.exists(filename):
        print("No records found.")
        return
    try:
        with open(filename, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                print(', '.join(row))
    except Exception as e:
        print(f"❌ Error reading from CSV: {e}")
