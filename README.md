# CSPS437Final_Project Restaurant Finder and Dashboard Web Application

## Introduction
Welcome to the Restaurant Finder and Dashboard Web Application, a one-stop solution for exploring and managing your favorite restaurant choices. Featuring a comprehensive listing, personalized dashboards, and detailed menu views, our app is designed to enhance your dining experience.

## Getting Started

### Prerequisites
- Python 3.x
- Flask Python web framework

### Initial Setup
To get the application up and running, follow these steps:

#### 1. Database download:
   - Go to google drive to download necessary csv files. The link is https://drive.google.com/drive/folders/1g1TlG_zCqg9E3Yp5tOgkNMtuvdcOj_KN?usp=sharing. The files need to be downloaded are "restaurant_menus.csv", "restaurant_data_new.csv" and "categories.csv". Put all of these csv files into the "CSV_DATA" folder.
   - **Notice:** The csv files can be about 300 MB.

#### 2. Database Initialization (`db_init.py`):
   - This script sets up your database with necessary tables and initial data.
   - **Important:** The initialization process can take some time, so please be patient.

#### 3. Running the Application (`app.py`):
   - After setting up the database, run `app.py` to start the Flask web server.

### Project Structure
- **CSV_DATA**:
  - Contains CSV files for the database: `categories.csv`, `restaurant_data_new.csv`, `restaurant_menus.csv`.

- **static**:
  - Houses static files like `style.css` for web page styling.

- **app.py**:
  - The Flask application file, including server setup, routes, and backend logic.

- **db_init.py**:
  - Script for initializing the database.

- **templates**:
  - Contains HTML templates (`DashBoard.html`, `Login.html`, `Register.html`, `menu.html`).

### Web Pages
- **DashBoard.html**:
  - Main app display for searching and managing restaurants.

- **Login.html**:
  - User login page for accessing personalized features.

- **Register.html**:
  - Registration page for new users.

- **menu.html**:
  - Displays menus of selected restaurants.

## Usage
1. Run `db_init.py` to set up the database.
2. Execute `app.py` to launch the server.
3. Access the app via `http://127.0.0.1:5000` in your browser.

## Contributing
Weiyi You,	Lindsey Lin

## Contact
linbdsey.lin@yale.edu,   weiyi.you@yale.edu

---

Enjoy exploring dining options with our Restaurant Finder and Dashboard Web Application! 🍽️✨
