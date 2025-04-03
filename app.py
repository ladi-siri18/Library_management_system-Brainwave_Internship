import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from library_db import execute_query

# Set page config
st.set_page_config(page_title="📚 Library Management System", layout="wide")

# Custom Styling
st.markdown(
    """
    <style>
    .main {background-color: #f8f9fa;}
    .stButton>button {border-radius: 8px; padding: 10px;}
    .sidebar .sidebar-content {background: linear-gradient(180deg, #0073e6, #00b4d8); color: white;}
    .stDataFrame {border-radius: 8px; overflow: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

# Title
st.markdown("<h1 style='text-align: center; color: #0073e6;'>📚 Library Management System</h1>", unsafe_allow_html=True)

# Sidebar for navigation
menu = ["View Books", "Add Book", "Issue Book", "Return Book", "Manage Members", "Overdue Books"]
choice = st.sidebar.radio("📌 Menu", menu)

# 1️⃣ View Books
if choice == "View Books":
    st.subheader("📖 Available Books")
    books = execute_query("SELECT * FROM Books", fetch=True)
    if books:
        df = pd.DataFrame(books, columns=["BookID", "Title", "Author", "Genre", "PublishedYear", "AvailableCopies"])
        st.dataframe(df, height=400)
    else:
        st.warning("⚠️ No books available.")

# 2️⃣ Add a New Book
elif choice == "Add Book":
    st.subheader("➕ Add New Book")
    title = st.text_input("📖 Book Title")
    author = st.text_input("✍️ Author")
    genre = st.text_input("📂 Genre")
    year = st.number_input("📅 Published Year", min_value=1000, max_value=9999, step=1)
    copies = st.number_input("📦 Available Copies", min_value=1, step=1)
    
    if st.button("✅ Add Book", key="add_book", help="Click to add a new book"):
        execute_query("INSERT INTO Books (Title, Author, Genre, PublishedYear, AvailableCopies) VALUES (?, ?, ?, ?, ?)",
                      (title, author, genre, year, copies))
        st.success(f"📚 Book '{title}' added successfully!")

# 3️⃣ Issue a Book
elif choice == "Issue Book":
    st.subheader("📤 Issue Book to a Member")
    books = execute_query("SELECT BookID, Title FROM Books WHERE AvailableCopies > 0", fetch=True)
    members = execute_query("SELECT MemberID, Name FROM Members", fetch=True)
    
    if books and members:
        book_dict = {book[1]: book[0] for book in books}
        member_dict = {member[1]: member[0] for member in members}

        selected_book = st.selectbox("📚 Select Book", list(book_dict.keys()))
        selected_member = st.selectbox("👤 Select Member", list(member_dict.keys()))

        if st.button("📩 Issue Book", key="issue_book", help="Click to issue the selected book"):
            book_id = book_dict[selected_book]
            member_id = member_dict[selected_member]
            due_date = (datetime.today() + timedelta(days=14)).strftime('%Y-%m-%d')
            execute_query("INSERT INTO Transactions (BookID, MemberID, DueDate, Status) VALUES (?, ?, ?, 'Borrowed')",
                          (book_id, member_id, due_date))
            execute_query("UPDATE Books SET AvailableCopies = AvailableCopies - 1 WHERE BookID = ?", (book_id,))
            st.success(f"✅ Book '{selected_book}' issued to {selected_member}. Due Date: {due_date}")
    else:
        st.warning("⚠️ No books or members available.")

# 4️⃣ Return a Book
elif choice == "Return Book":
    st.subheader("🔄 Return Book")
    issued_books = execute_query("SELECT t.TransactionID, b.Title, m.Name FROM Transactions t JOIN Books b ON t.BookID = b.BookID JOIN Members m ON t.MemberID = m.MemberID WHERE t.Status = 'Borrowed'", fetch=True)
    
    if issued_books:
        return_dict = {f"{row[1]} (Issued to {row[2]})": row[0] for row in issued_books}
        selected_return = st.selectbox("📘 Select Issued Book to Return", list(return_dict.keys()))
        
        if st.button("🔁 Return Book", key="return_book"):
            transaction_id = return_dict[selected_return]
            execute_query("UPDATE Transactions SET ReturnDate = DATE('now'), Status = 'Returned' WHERE TransactionID = ?", (transaction_id,))
            execute_query("UPDATE Books SET AvailableCopies = AvailableCopies + 1 WHERE BookID = (SELECT BookID FROM Transactions WHERE TransactionID = ?)", (transaction_id,))
            st.success("✅ Book returned successfully!")
    else:
        st.info("📭 No books to return.")

# 5️⃣ Manage Members
elif choice == "Manage Members":
    st.subheader("👤 Add Library Member")
    name = st.text_input("👥 Member Name")
    email = st.text_input("✉️ Email")
    phone = st.text_input("📞 Phone Number")
    
    if st.button("🆕 Add Member", key="add_member"):
        execute_query("INSERT INTO Members (Name, Email, Phone) VALUES (?, ?, ?)", (name, email, phone))
        st.success(f"✅ Member '{name}' added successfully!")
    
    st.subheader("📋 View Members")
    members = execute_query("SELECT * FROM Members", fetch=True)
    if members:
        df = pd.DataFrame(members, columns=["MemberID", "Name", "Email", "Phone", "JoinDate"])
        st.dataframe(df, height=400)
    else:
        st.info("📭 No members found.")

# 6️⃣ Overdue Books
elif choice == "Overdue Books":
    st.subheader("⏳ Overdue Books")
    overdue_books = execute_query("SELECT m.Name, b.Title, t.DueDate FROM Transactions t JOIN Members m ON t.MemberID = m.MemberID JOIN Books b ON t.BookID = b.BookID WHERE DATE(t.DueDate) < DATE('now') AND t.Status = 'Borrowed'", fetch=True)
    
    if overdue_books:
        df = pd.DataFrame(overdue_books, columns=["Member Name", "Book Title", "Due Date"])
        df["Due Date"] = pd.to_datetime(df["Due Date"], errors='coerce')
        df["Fine (₹)"] = df["Due Date"].apply(lambda x: max((datetime.today() - x).days * 10, 0) if pd.notna(x) else 0)
        st.dataframe(df, height=400)
    else:
        st.info("✅ No overdue books.")
