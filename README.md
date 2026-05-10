# 🌤️ Modern Weather Dashboard (Asynchronous Python Application)

A professional, high-performance desktop Weather Dashboard built with Python. This project demonstrates advanced software engineering techniques including **Asynchronous I/O**, **Relational Databases**, **RESTful API Integration**, and **Data Visualization**.

## 🚀 Features

* **⚡ Asynchronous API Calls (`aiohttp` & `asyncio`):** Fetches real-time weather and forecast data from the OpenWeatherMap API without blocking or freezing the Graphical User Interface.
* **📊 Data Visualization (`matplotlib`):** Analyzes 5-day forecast data and generates a clean, readable temperature trend line chart.
* **🗄️ Local Database (`sqlite3`):** Implements a local SQLite database to persist search history, allowing users to quickly access their most recently searched cities.
* **🎨 Modern GUI (`customtkinter`):** Features a sleek, dark-mode supported Dashboard interface with rounded corners, dynamic weather icons, and a highly responsive design.
* **🔒 Smart Configuration:** Automatically prompts the user for an API key on first launch and securely saves it to a local configuration file.

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **GUI Framework:** CustomTkinter, Tkinter
* **Async Network:** aiohttp, asyncio
* **Data Visualization:** Matplotlib
* **Database:** SQLite3
* **Image Processing:** Pillow (PIL)

## ⚙️ Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/Weather-App.git
   cd Weather-App
   ```

2. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```
   *Note: On your first run, the app will ask for a free OpenWeatherMap API key. You can get one at [openweathermap.org](https://openweathermap.org/).*

## 📸 Screenshots
*(Buraya uygulamanın ekran görüntüsünü ekleyebilirsiniz)*

---
*Built for educational purposes and portfolio demonstration.*
