# 📚 Library Connect (Book Catalog Application)

A Python-based desktop application built with Tkinter and MySQL. This application allows users to build a personal reading catalog, track their progress, and compete on a global leaderboard. It features an automated setup process, making it incredibly easy to run on a new machine.

---

## ✨ Key Features

* **Dual-Role System:** Automated routing for `User` and `Admin` accounts.
* **Admin Dashboard:** Admins can view all users, manage user accounts (delete), and approve password reset requests.
* **User Library:** Users can add books (Title, Author, Total Chapters), update their reading progress, leave a 1-5 Star rating, and remove books.
* **Gamification & Medals:** A dynamic ranking system calculates a user's score based on their reading completion rate and total books read. The top 3 users are awarded 🥇 Gold, 🥈 Silver, and 🥉 Bronze medals on their dashboard.
* **Robust Security:**
  * 8-character minimum password requirement.
  * Hide/Show password toggles (👁 icon).
  * Dynamic temporary passwords for account resets (e.g., `username@123`).
  * Forced password-change screen upon logging in with a reset password.
* **Self-Building Database:** The app automatically creates its own MySQL database and tables (`users` and `books_read`) during the first launch.

---

## 🛠️ Prerequisites & Setup (For New Computers)

If you are on a new laptop and only have **Visual Studio Code (VS Code)** installed, follow these steps to run the project.

---

## 1️⃣ Install Python

1. Download Python from: [https://www.python.org/downloads/](https://www.python.org/downloads/)

2. Run the installer.

3. ⚠️ IMPORTANT:  
   Check the box **"Add Python to PATH"** before clicking Install.

---

## 2️⃣ MySQL Setup

1. Go to the MySQL download website:  [https://dev.mysql.com/downloads/installer/](https://dev.mysql.com/downloads/installer/)

2. Download and install MySQL using the default settings.

3. During installation, set your MySQL root password.

---

## 3️⃣ Download or Clone the Project

### Option 1: Download ZIP

1. Open the GitHub repository.
2. Click the green **Code** button.
3. Click **Download ZIP**.
4. Extract the ZIP file.

### Option 2: Clone Using Git

```bash
git clone https://github.com/your-username/your-repository-name.git
```

After downloading or cloning, open the project folder in VS Code.

---

## 4️⃣ Open the Project in VS Code

1. Open VS Code.
2. Go to `File` > `Open Folder`.
3. Select the downloaded project folder.
4. Open `app.py` and replace the password value with your MySQL password:

```python
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password"
)
```
---

## 5️⃣ Install the Database Connector

Python needs a package to communicate with MySQL.

Open the VS Code terminal:

```bash
pip install mysql-connector-python
```

---

## 🚀 How to Run the Application

1. Make sure MySQL Server is running.
2. Ensure the image files (`Login.png`, `background1.png`, `gold.png`, etc.) are in the same folder as the Python scripts.
3. Open the VS Code terminal and run:

```bash
python app.py
```

If `python` does not work, try:

```bash
python3 app.py
```

---

## 🔑 Default Login Credentials

Because the database is automatically created during the first run, a default Admin account is generated automatically.

* **Username:** `Raja`
* **Password:** `Raj@1234`
* **Role:** `Admin`

To test User features, click **Sign Up** on the login page to create a new user account.

---

## 📁 Project Structure

* `app.py` → Main frontend application (Tkinter UI and layouts).
* `main.py` → Backend database logic, SQL queries, ranking algorithms, and validations.
* `*.png` → UI assets and medal icons used in the dashboard.

---

## 💻 Tech Stack

* **Frontend:** Python (Tkinter)
* **Backend:** MySQL
* **Connector:** `mysql-connector-python`

---

## 📸 Screenshots

### Login Page
<img width="1191" height="665" alt="image" src="https://github.com/user-attachments/assets/1bb9d9c2-7c63-411b-ab29-f0b3c882a84a" />


### Dashboard
<img width="1187" height="662" alt="image" src="https://github.com/user-attachments/assets/c3550947-914e-40c1-af09-f3f7815ab171" />


---

## 👨‍💻 Author

Developed by Raja M.
