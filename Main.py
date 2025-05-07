import Functions

def safe_input_password(prompt):
    """Simple password input (not hidden)"""
    return input(prompt)

def main():
    print("📌 Welcome to the Malaysia Income Tax Filing System")

    user_id = input("Enter your User ID (leave blank to auto-generate): ").strip()
    if user_id == "":
        user_id = Functions.generate_new_user_id()
        print(f"🔐 Auto-generated User ID: {user_id}")

    if Functions.is_registered(user_id):
        print("🔐 User found. Please log in.")
        ic_number = input("Enter your 12-digit IC number: ")
        password = safe_input_password("Enter your password (last 4 digits of IC): ")
        if not Functions.verify_user(ic_number, password):
            print("❌ Login failed. Incorrect IC number or password.")
            return
        print("✅ Login successful!")
    else:
        print("📝 New User Registration")
        ic_number = input("Enter your 12-digit IC number: ")
        if len(ic_number) != 12:
            print("❌ IC number must be exactly 12 digits.")
            return

        password = safe_input_password("Set your password (must be last 4 digits of IC): ")
        if password != ic_number[-4:]:
            print("❌ Password must match the last 4 digits of your IC.")
            return
        print("✅ Registration successful!")

    try:
        income = float(input("Enter your annual income (RM): "))
        if income > 1_000_000:
            confirm = input("⚠️ Are you sure your income exceeds RM 1,000,000? (y/n): ")
            if confirm.lower() != 'y':
                print("❌ Please re-enter your correct income.")
                return

        spouse_income = float(input("Enter spouse income (RM, or 0 if not applicable): "))
        num_children = int(input("Enter number of children (0 if none): "))
        medical_expenses = float(input("Enter total medical expenses (RM): "))
        lifestyle_expenses = float(input("Enter lifestyle expenses (RM): "))
        education_fees = float(input("Enter education fees (RM): "))
        parental_support = float(input("Enter parental support expenses (RM): "))
    except ValueError:
        print("❌ Invalid input. Please ensure all values are numeric.")
        return

    def ask_yes_no(prompt):
        while True:
            ans = input(prompt).strip().lower()
            if ans in ['y', 'n']:
                return ans == 'y'
            print("Please enter 'y' or 'n'.")

    is_disabled = ask_yes_no("Are you or your dependents disabled? (y/n): ")
    bought_breastfeeding = ask_yes_no("Did you purchase breastfeeding equipment? (y/n): ")
    bought_sports = ask_yes_no("Did you purchase sports equipment? (y/n): ")
    bought_books = ask_yes_no("Did you purchase books? (y/n): ")
    paid_insurance = ask_yes_no("Did you pay insurance premiums (life/EPF)? (y/n): ")

    # Calculate total tax relief
    total_relief = Functions.calculate_total_relief(
        individual=True,
        spouse_income=spouse_income,
        num_children=num_children,
        medical_expenses=medical_expenses,
        lifestyle_expenses=lifestyle_expenses,
        education_fees=education_fees,
        parental_support=parental_support
    )

    # Add additional reliefs
    if is_disabled:
        total_relief += 6000
    if bought_breastfeeding:
        total_relief += 1000
    if bought_sports:
        total_relief += 500
    if bought_books:
        total_relief += 200
    if paid_insurance:
        total_relief += 3000

    print(f"💸 Total Tax Relief: RM {total_relief:.2f}")

    # Calculate tax payable
    tax_payable = Functions.calculate_tax(income, total_relief)

    # Ask how much tax was already paid
    try:
        tax_paid = float(input("Enter the amount of tax already paid (e.g. PCB, RM): "))
    except ValueError:
        print("❌ Invalid input. Skipping tax refund calculation.")
        tax_paid = 0

    if tax_payable == 0:
        print("✅ No tax payable. You may be eligible for a full refund.")
    elif tax_paid > tax_payable:
        refund = tax_paid - tax_payable
        print(f"💵 You may be eligible for a tax refund of: RM {refund:.2f}")
    elif tax_paid < tax_payable:
        balance_due = tax_payable - tax_paid
        print(f"📌 You still owe: RM {balance_due:.2f}")
    else:
        print("✅ Tax fully paid. No additional tax or refund.")

    # Save user data
    Functions.save_to_csv([user_id, ic_number, income, total_relief, tax_payable])
    print("✅ Data saved to CSV.")

    # Option to view records
    view = input("Do you want to view all tax records? (y/n): ")
    if view.lower() == 'y':
        print("\n📄 All Tax Records:")
        Functions.read_from_csv()

if __name__ == "__main__":
    main()
