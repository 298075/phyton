import csv
import os

def verify_user(ic_number, password):
    """
    验证IC号码是否为12位，且密码是否为IC号的最后4位
    """
    return len(ic_number) == 12 and ic_number[-4:] == password

def calculate_tax(income, tax_relief):
    """
    根据收入与减免额，计算马来西亚简化税额
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

def save_to_csv(user_id, ic_number, income, tax_relief, tax_payable, filename="user_data.csv"):
    """
    将用户数据写入CSV文件（若文件不存在则创建）
    """
    file_exists = os.path.exists(filename)
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['ID', 'IC Number', 'Income', 'Tax Relief', 'Tax Payable'])
        writer.writerow([user_id, ic_number, income, tax_relief, tax_payable])

def read_from_csv(filename="user_data.csv"):
    """
    从CSV文件中读取并显示数据
    """
    if not os.path.exists(filename):
        print("尚未有记录。")
        return
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            print(', '.join(row))

def is_registered(user_id, filename="user_data.csv"):
    """
    检查用户ID是否已存在于CSV中
    """
    if not os.path.exists(filename):
        return False
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[0] == user_id:
                return True
    return False