import subprocess
import sys
import os

def run_script(script_name):
    """Run a Python script and return the return code"""
    try:
        result = subprocess.run([sys.executable, script_name])
        return result.returncode
    except FileNotFoundError:
        print(f"Error: Script '{script_name}' not found!")
        return 1
    except Exception as e:
        print(f"Error running {script_name}: {e}")
        return 1

def main():
    print("\n" + "="*50)
    print("        LIBRARY MANAGEMENT SYSTEM")
    print("="*50)
    print("1. Add Member/Book")
    print("2. Borrow Book")
    print("3. Return Book")
    print("4. View Books/Members")
    print("5. Update Book/Member Info")
    print("6. Delete Book/Member")
    print("7. Reports")
    print("8. Exit")
    print("="*50)
    
    choice = input("Enter your choice (1-8): ").strip()
    
    if choice == "1":
        run_script("book_add.py")
    elif choice == "2":
        run_script("books_borrow.py")
    elif choice == "3":
        run_script("books_return.py")
    elif choice == "4":
        run_script("books_view.py")
    elif choice == "5":
        run_script("books_update.py")
    elif choice == "6":
        run_script("books_delete.py")
    elif choice == "7":
        run_script("books_reports.py")
    elif choice == "8":
        print("Thank you for using the Library Management System!")
        sys.exit(0)
    else:
        print("Invalid choice. Please enter a number between 1-8.")

if __name__ == "__main__":
    # Check if required environment variables are set
    if not os.path.exists('.env'):
        print("Warning: .env file not found. Please make sure to create it with SUPABASE_URL and SUPABASE_KEY.")
    
    while True:
        main()
        input("\nPress Enter to continue...")