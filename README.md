# 📚  Library_management_system-Brainwave_Internship

## 📌 Overview
The **Library Management System** is a **Streamlit-based web application** that allows users to manage books, members, and transactions efficiently. The system provides functionalities such as viewing available books, adding new books, issuing and returning books, managing members, and tracking overdue books with fine calculations.

## 🔥 Features
- 📖 **View Books** – Display available books with details.
- ➕ **Add Books** – Add new books to the library.
- 📤 **Issue Books** – Lend books to members with a due date.
- 🔄 **Return Books** – Process book returns and update availability.
- 👤 **Manage Members** – Add new members to the library.
- ⏳ **Overdue Books** – Track overdue books and calculate fines.
- 🎨 **Enhanced UI** – Colored buttons with gradient effects for better navigation.

## 🛠️ Technologies Used
- **Python** – Core programming language.
- **Streamlit** – For interactive UI development.
- **SQLite** – Database for storing books, members, and transactions.
- **Pandas** – Data handling and manipulation.
- **Datetime** – For handling due dates and fine calculations.

## 🚀 Installation & Setup
Follow these steps to set up and run the project:

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/Library-Management-System.git
cd Library-Management-System
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Set Up the Database
Run the following Python script to create the database tables:
```bash
python library_db.py
```

### 4️⃣ Run the Application
```bash
streamlit run app.py
```

## 🎯 Usage Guide
1. **Navigate via Sidebar** – Click on colored buttons to access different sections.
2. **Add Books** – Enter book details and click **Add Book**.
3. **Issue Books** – Select a book, choose a member, and click **Issue Book**.
4. **Return Books** – Select an issued book and click **Return Book**.
5. **Manage Members** – Add new members by entering their details.
6. **Check Overdue Books** – View books that have passed their due dates and fine details.

