import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

if not url or not key:
    raise Exception("Supabase URL or Key not found in environment variables!")

sb: Client = create_client(url, key)

# -------------------- INSERT FUNCTIONS --------------------

def add_member(name, email):
    payload = {"name": name, "email": email}
    resp = sb.table("members").insert(payload).execute()
    return resp.data

def add_book(title, author, category, stock=1):
    payload = {"title": title, "author": author, "category": category, "stock": stock}
    resp = sb.table("books").insert(payload).execute()
    return resp.data
if __name__ == "__main__":
    print("Choose table to insert:")
    print("1. Register Member")
    print("2. Add Book")
    choice = input("Enter choice (1/2): ").strip()
    if choice == "1":
        name = input("Enter member name: ").strip()
        email = input("Enter member email: ").strip()
        created = add_member(name, email)
        print(" Member Inserted:", created)

    elif choice == "2":
        title = input("Enter book title: ").strip()
        author = input("Enter author name: ").strip()
        category = input("Enter category: ").strip()
        stock = int(input("Enter stock count: ").strip())
        created = add_book(title, author, category, stock)
        print(" Book Inserted:", created)

    else:
        print(" Invalid choice")