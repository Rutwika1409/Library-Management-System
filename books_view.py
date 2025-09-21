import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

if not url or not key:
    raise Exception("Supabase URL or Key not found in environment variables!")

sb: Client = create_client(url, key)

# -------------------- READ FUNCTIONS --------------------

def list_all_books():
    """List all books with availability"""
    resp = sb.table("books").select("*").execute()
    return resp.data

def search_books(title=None, author=None, category=None):
    query = sb.table("books").select("*")

    if title is not None:
        query = query.contains("title", title)
    if author is not None:
        query = query.contains("author", author)
    if category is not None:
        query = query.contains("category", category)

    resp = query.execute()
    return resp.data


def member_details_with_books(member_id):
    resp = (
        sb.table("borrow_records")
        .select("record_id, borrow_date, return_date, members(name,email), books(title,author,category)")
        .eq("member_id", member_id)
        .execute()
    )
    return resp.data
if __name__ == "__main__":
    print("Choose READ option:")
    print("1. List all books")
    print("2. Search books")
    print("3. Show member details with borrowed books")

    choice = input("Enter choice (1/2/3): ").strip()

    if choice == "1":
        books = list_all_books()
        print("Books Available:")
        for b in books:
            print(f"{b['book_id']}. {b['title']} by {b['author']} ({b['stock']} copies)")

    elif choice == "2":
        field = input("Search by (title/author/category): ").strip().lower()
        keyword = input("Enter search keyword: ").strip()
        if field == "title":
            results = search_books(title=keyword)
        elif field == "author":
            results = search_books(author=keyword)
        elif field == "category":
            results = search_books(category=keyword)
        else:
            print(" Invalid field.")
            results = []

        print("Search Results:")
        for b in results:
            print(f"{b['title']} by {b['author']} - {b['category']} ({b['stock']} copies)")

    elif choice == "3":
        member_id = int(input("Enter member ID: ").strip())
        records = member_details_with_books(member_id)
        if records:
            print(f" Borrow history for Member ID {member_id}:")
            for r in records:
                print(f"- {r['books']['title']} by {r['books']['author']} | Borrowed: {r['borrow_date']} | Returned: {r['return_date']}")
        else:
            print("No borrow records found for this member.")

    else:
        print("Invalid choice")