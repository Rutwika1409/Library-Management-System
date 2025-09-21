# Library Management System

A complete command-line (CLI) Library Management System built with Python and Supabase. Manage books, members, borrowing operations, and generate reports through an intuitive menu interface.

## Features

- **Book Management**: Add, update, delete, and search books
- **Member Management**: Register members and track their borrowing history
- **Borrow/Return System**: Full transaction handling with automatic stock management
- **Search Functionality**: Find books by title, author, or category
- **Reporting System**: Generate reports on popular books, overdue items, and member activity
- **Data Validation**: Prevent invalid operations like deleting members with active borrows

## Requirements

- Python 3.8+
- Supabase account
- Python packages: `supabase`, `python-dotenv`

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Rutwika1409/Library-Management-System.git
cd Library-Management-System
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your Supabase credentials:
```
SUPABASE_URL=your_project_url
SUPABASE_KEY=your_anon_key
```

## Usage

Run the main program:
```bash
python library.py
```

Follow the on-screen menu to access all features:
1. Add members/books
2. Borrow books
3. Return books
4. View books/members
5. Update information
6. Delete books/members
7. Generate reports
8. Exit system

## Project Structure

- `library.py` - Main menu system
- `book_add.py` - Add books and members
- `books_borrow.py` - Handle book borrowing
- `books_return.py` - Handle book returns
- `books_view.py` - View and search books
- `books_update.py` - Update records
- `books_delete.py` - Delete books/members
- `books_reports.py` - Generate reports
- `requirements.txt` - Dependencies

## Database Schema

The system uses three main tables:
- **books** (book_id, title, author, category, stock)
- **members** (member_id, name, email)
- **borrow_records** (record_id, member_id, book_id, borrow_date, return_date)
