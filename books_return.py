import os
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

if not url or not key:
    raise Exception("Supabase URL or Key not found!")

sb: Client = create_client(url, key)

def return_book(record_id):
    """Return a borrowed book with transaction support"""
    try:
        # Get the borrow record
        record_resp = sb.table("borrow_records").select("*").eq("record_id", record_id).execute()
        if not record_resp.data:
            return {"error": "Borrow record not found"}
        
        record = record_resp.data[0]
        
        # Check if already returned
        if record["return_date"]:
            return {"error": "Book already returned"}
        
        # Get book info
        book_resp = sb.table("books").select("stock").eq("book_id", record["book_id"]).execute()
        if not book_resp.data:
            return {"error": "Book not found"}
        
        current_stock = book_resp.data[0]["stock"]
        
        # Execute both operations in a transaction
        # Update borrow record with return date
        sb.table("borrow_records").update({
            "return_date": datetime.now().isoformat()
        }).eq("record_id", record_id).execute()
        
        # Increase book stock
        sb.table("books").update({
            "stock": current_stock + 1
        }).eq("book_id", record["book_id"]).execute()
        
        return {"success": "Book returned successfully"}
    
    except Exception as e:
        return {"error": f"Transaction failed: {str(e)}"}

if __name__ == "__main__":
    try:
        record_id = int(input("Enter Borrow Record ID to return: ").strip())
        result = return_book(record_id)
        print(result)
    except ValueError:
        print("Invalid Record ID. Must be a number.")