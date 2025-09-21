import os
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

if not url or not key:
    raise Exception("Supabase URL or Key not found!")

sb: Client = create_client(url, key)

def get_top_borrowed_books(limit=5):
    """Get top most borrowed books"""
    # First get all books with their borrow counts
    resp = sb.table("books").select("book_id, title, author").execute()
    books = resp.data
    
    # Get borrow counts for each book
    for book in books:
        borrow_resp = sb.table("borrow_records") \
            .select("record_id", count="exact") \
            .eq("book_id", book["book_id"]) \
            .execute()
        book["borrow_count"] = borrow_resp.count or 0
    
    # Sort by borrow count descending and return top N
    books.sort(key=lambda x: x["borrow_count"], reverse=True)
    return books[:limit]

def get_members_with_overdue_books():
    """Get members with books borrowed for more than 14 days"""
    fourteen_days_ago = (datetime.now() - timedelta(days=14)).isoformat()
    
    # Get overdue borrow records
    resp = sb.table("borrow_records") \
        .select("*, members(*), books(*)") \
        .lt("borrow_date", fourteen_days_ago) \
        .is_("return_date", None) \
        .execute()
    
    return resp.data

def get_borrow_count_per_member():
    """Get total books borrowed per member"""
    # Get all members
    members_resp = sb.table("members").select("member_id, name").execute()
    members = members_resp.data
    
    # Get borrow counts for each member
    for member in members:
        # Total borrowed
        total_resp = sb.table("borrow_records") \
            .select("record_id", count="exact") \
            .eq("member_id", member["member_id"]) \
            .execute()
        member["total_borrowed"] = total_resp.count or 0
        
        # Currently borrowed
        current_resp = sb.table("borrow_records") \
            .select("record_id", count="exact") \
            .eq("member_id", member["member_id"]) \
            .is_("return_date", None) \
            .execute()
        member["currently_borrowed"] = current_resp.count or 0
    
    # Sort by total borrowed descending
    members.sort(key=lambda x: x["total_borrowed"], reverse=True)
    return members

if __name__ == "__main__":
    print("Choose Report:")
    print("1. Top 5 Most Borrowed Books")
    print("2. Members with Overdue Books (>14 days)")
    print("3. Borrow Count per Member")
    
    choice = input("Enter choice (1/2/3): ").strip()
    
    if choice == "1":
        print("\nTop 5 Most Borrowed Books:")
        books = get_top_borrowed_books()
        for i, book in enumerate(books, 1):
            print(f"{i}. {book['title']} by {book['author']} - Borrowed {book['borrow_count']} times")
    
    elif choice == "2":
        print("\nMembers with Overdue Books:")
        overdue = get_members_with_overdue_books()
        if overdue:
            for record in overdue:
                borrow_date = datetime.fromisoformat(record['borrow_date'].replace('Z', '+00:00'))
                days_overdue = (datetime.now() - borrow_date).days
                print(f"Member: {record['members']['name']} ({record['members'].get('email', 'No email')})")
                print(f"Book: {record['books']['title']} - Borrowed {days_overdue} days ago")
                print("---")
        else:
            print("No overdue books found.")
    
    elif choice == "3":
        print("\nBorrow Count per Member:")
        counts = get_borrow_count_per_member()
        for member in counts:
            print(f"{member['name']}: {member['total_borrowed']} total, {member['currently_borrowed']} currently borrowed")
    
    else:
        print("Invalid choice")
