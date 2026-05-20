# 📚 Library Connect (Book Catalog Application)

A Python-based desktop application built with Tkinter and MySQL. This application allows users to build a personal reading catalog, track their progress, and compete on a global leaderboard. It features an automated setup process, making it incredibly easy to run on a new machine.

## ✨ Key Features

* **Dual-Role System:** Automated routing for `User` and `Admin` accounts.
* **Admin Dashboard:** Admins can view all users, manage user accounts (delete), and approve password reset requests.
* **User Library:** Users can add books (Title, Author, Total Chapters), update their reading progress, leave a 1-5 Star rating, and remove books.
* **Gamification & Medals:** A dynamic ranking system calculates a user's score based on their reading completion rate and total books read. The top 3 users are awarded 🥇 Gold, 🥈 Silver, and 🥉 Bronze medals on their dashboard!
* **Robust Security:** * 8-character minimum password requirement.
  * Hide/Show password toggles (👁 icon).
  * Dynamic temporary passwords for account resets (e.g., `username@123`).
  * Forced password-change screen upon logging in with a reset password.
* **Self-Building Database:** The app automatically builds its own MySQL database and tables (`users` and `books_read`) on the first launch.

## 🛠️ Prerequisites & Setup (For New Computers)

If you are on a new laptop and only have **Visual Studio Code (VS Code)** installed, follow these steps to run the project.

### 1. Install Python
1. Download Python from [python.org/downloads](https://www.python.org/downloads/).
2. Run the installer.
3. ⚠️ **IMPORTANT:** At the bottom of the installer window, check the box that says **"Add Python to PATH"** before clicking Install.

### 2. Install MySQL (via XAMPP)
This application requires a local database to store users and books.
1. Download **XAMPP** from [apachefriends.org](https://www.apachefriends.org/).
2. Install it with the default settings.
3. Open the XAMPP Control Panel and click **"Start"** next to the **MySQL** module.

### 3. Open the Project in VS Code
1. Download or clone this repository to your computer.
2. Open VS Code.
3. Go to `File` > `Open Folder` and select the downloaded project folder.

### 4. Install the Database Connector
Python needs a package to talk to MySQL.
1. In VS Code, open a terminal by clicking `Terminal` > `New Terminal` at the top of the screen.
2. Type the following command and press Enter:
   ```bash
   pip install mysql-connector-python

```

---

## 🚀 How to Run the Application

1. Make sure MySQL is running in your XAMPP Control Panel.
2. Ensure the image files (`Login.png`, `background1.png`, `gold.png`, etc.) are in the exact same folder as the Python scripts.
3. In your VS Code terminal, run the application:
```bash
python app.py

```



*(Note: If you get an error that 'python' is not recognized, try typing `python3 app.py` instead).*

### 🔑 Default Login Credentials

Because the database builds itself on the first run, a default Admin account is automatically generated for you.

* **Username:** `Raja`
* **Password:** `Raj@1234`
* **Role:** Admin

To test the User features, click **"Sign Up"** on the login screen to create a new standard user account.

---

## 📁 Project Structure

* `app.py` - The main frontend application (Tkinter UI and layouts).
* `main.py` - The backend database logic (SQL queries, ranking algorithms, and data validation).
* `*.png` - UI assets and medal icons required for the dashboard.

## 💻 Tech Stack

* **Frontend:** Python (Tkinter)
* **Backend:** MySQL
* **Connector:** `mysql-connector-python`

```

```
