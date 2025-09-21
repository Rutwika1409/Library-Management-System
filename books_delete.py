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

def delete_member(member_id: int):
    borrowed = sb.table("borrow_records") \
        .select("record_id") \
        .eq("member_id", member_id) \
        .is_("return_date", "null") \
        .execute()

    if borrowed.data:
        print("Cannot delete member — they have borrowed books.")
        return None

    resp = sb.table("members").delete().eq("member_id", member_id).execute()
    print("Member deleted.")
    return resp.data

def delete_book(book_id: int):
    borrowed = sb.table("borrow_records") \
        .select("record_id") \
        .eq("book_id", book_id) \
        .is_("return_date", "null") \
        .execute()

    if borrowed.data:
        print("Cannot delete book — it is currently borrowed.")
        return None

    resp = sb.table("books").delete().eq("book_id", book_id).execute()
    print("Book deleted.")
    return resp.data

if __name__ == "__main__":
    choice = input("Delete (1) Member or (2) Book? Enter 1 or 2: ").strip()

    if choice == "1":
        try:
            member_id = int(input("Enter Member ID to delete: ").strip())
            delete_member(member_id)
        except ValueError:
            print("Invalid Member ID. Must be a number.")

    elif choice == "2":
        try:
            book_id = int(input("Enter Book ID to delete: ").strip())
            delete_book(book_id)
        except ValueError:
            print("Invalid Book ID. Must be a number.")

    else:
        print("Invalid choice. Please enter 1 or 2.")
