import sqlite3

def get_db_connection():
    return sqlite3.connect("library.db")

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create Books Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Books (
            BookID INTEGER PRIMARY KEY AUTOINCREMENT,
            Title TEXT NOT NULL,
            Author TEXT NOT NULL,
            Genre TEXT,
            PublishedYear INTEGER,
            AvailableCopies INTEGER DEFAULT 1
        )
    """)

    # Create Members Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Members (
            MemberID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Email TEXT UNIQUE NOT NULL,
            Phone TEXT,
            JoinDate TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Create Transactions Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Transactions (
        TransactionID INTEGER PRIMARY KEY AUTOINCREMENT,
        BookID INTEGER NOT NULL,
        MemberID INTEGER NOT NULL,
        BorrowDate TEXT DEFAULT CURRENT_TIMESTAMP,
        ReturnDate TEXT,
        Status TEXT CHECK(Status IN ('Borrowed', 'Returned')) NOT NULL DEFAULT 'Borrowed',
        FOREIGN KEY (BookID) REFERENCES Books(BookID) ON DELETE CASCADE,
        FOREIGN KEY (MemberID) REFERENCES Members(MemberID) ON DELETE CASCADE
    )
""")


    # Check if DueDate column exists in Transactions
    cursor.execute("PRAGMA table_info(Transactions);")
    columns = [col[1] for col in cursor.fetchall()]
    if "DueDate" not in columns:
        cursor.execute("ALTER TABLE Transactions ADD COLUMN DueDate DATE;")
        print("✅ 'DueDate' column added successfully!")

    conn.commit()
    conn.close()
    print("✅ Tables created successfully!")

def insert_data():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if email exists before inserting
    def email_exists(email):
        cursor.execute("SELECT 1 FROM Members WHERE Email = ?", (email,))
        return cursor.fetchone() is not None

    # Books Data
    books_data = [
        ("The Alchemist", "Paulo Coelho", "Fiction", 1988, 5),
        ("1984", "George Orwell", "Dystopian", 1949, 3),
        ("To Kill a Mockingbird", "Harper Lee", "Classic", 1960, 4)
    ]
    cursor.executemany("INSERT OR IGNORE INTO Books (Title, Author, Genre, PublishedYear, AvailableCopies) VALUES (?, ?, ?, ?, ?)", books_data)

    # Members Data
    members_data = [
        ("Alice Johnson", "alice@example.com", "1234567890"),
        ("Bob Smith", "bob@example.com", "9876543210")
    ]
    for name, email, phone in members_data:
        if not email_exists(email):  # Avoid duplicate emails
            cursor.execute("INSERT INTO Members (Name, Email, Phone) VALUES (?, ?, ?)", (name, email, phone))
        else:
            print(f"⚠️ Skipping duplicate email: {email}")

    conn.commit()
    conn.close()
    print("✅ Data inserted successfully!")

def execute_query(query, params=(), fetch=False):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall() if fetch else None
    conn.commit()
    conn.close()
    return result

# Run database setup
create_tables()
insert_data()