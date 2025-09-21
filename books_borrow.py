import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load env
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
sb: Client = create_client(url, key)

def borrow_book(member_id, book_id):
    """Simple borrow book logic"""

    # Check stock
    book = sb.table("books").select("stock").eq("book_id", book_id).execute()
    if not book.data:
        return {"error": "Book not found"}

    stock = book.data[0]["stock"]
    if stock <= 0:
        return {"error": "Book not available"}

    # Reduce stock
    sb.table("books").update({"stock": stock - 1}).eq("book_id", book_id).execute()

    # Add borrow record
    borrow = {"member_id": member_id, "book_id": book_id}
    resp = sb.table("borrow_records").insert(borrow).execute()

    return {"success": "Book borrowed", "record": resp.data}

# ---------------- MAIN ----------------
if __name__ == "__main__":
    member_id = int(input("Enter Member ID: "))
    book_id = int(input("Enter Book ID: "))
    print(borrow_book(member_id, book_id))