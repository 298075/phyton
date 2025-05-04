import Functions

def safe_input_password(prompt):
    """
    Simple password input (not hidden for compatibility with all environments)
    """
    return input(prompt)

def main():
    print("📌 Welcome to the Malaysia Tax Input System")

    user_id = input("Enter your User ID (leave blank to auto-generate): ").strip()
    if user_id == "":
        user_id = Functions.generate_new_user_id()
        print(f"🔐 Auto-generated User ID: {user_id}")

    if Functions.is_registered(user_id):
        print("🔐 User found. Please log in.")
        ic_number = input("Enter your 12-digit IC number: ")
        password = safe_input_password("Enter your password (last 4 digits of IC): ")
        if not Functions.verify_user(ic_number, password):
            print("❌ Login failed. Incorrect IC or password.")
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
        tax_relief = float(input("Enter your total tax relief (RM): "))
    except ValueError:
        print("❌ Invalid input. Please enter numeric values.")
        return

    tax_payable = Functions.calculate_tax(income, tax_relief)
    print(f"💰 Tax payable: RM {tax_payable:.2f}")

    Functions.save_to_csv(user_id, ic_number, income, tax_relief, tax_payable)
    print("✅ Data saved to CSV.")

    view = input("Do you want to view all tax records? (y/n): ")
    if view.lower() == 'y':
        print("\n📄 All Tax Records:")
        Functions.read_from_csv()

if __name__ == "__main__":
    main()
