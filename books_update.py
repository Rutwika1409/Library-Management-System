import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

if not url or not key:
    raise Exception("Supabase URL or Key not found!")

sb: Client = create_client(url, key)

# --- Update functions ---
def update_book_stock(book_id, new_stock):
    """Update the stock of a book"""
    resp = sb.table("books").update({"stock": new_stock}).eq("book_id", book_id).execute()
    return resp.data

def update_member_email(member_id, new_email):
    """Update a member's email"""
    resp = sb.table("members").update({"email": new_email}).eq("member_id", member_id).execute()
    return resp.data

# --- Interactive Menu ---
if __name__ == "__main__":
    print("Update Menu:")
    print("1. Update Book Stock")
    print("2. Update Member Email")

    choice = input("Enter choice (1/2): ").strip()

    if choice == "1":
        book_id = int(input("Enter Book ID: ").strip())
        new_stock = int(input("Enter new stock: ").strip())
        result = update_book_stock(book_id, new_stock)
        print("Book stock updated:", result)

    elif choice == "2":
        member_id = int(input("Enter Member ID: ").strip())
        new_email = input("Enter new email: ").strip()
        result = update_member_email(member_id, new_email)
        print(" Member email updated:", result)

    else:
        print(" Invalid choice")