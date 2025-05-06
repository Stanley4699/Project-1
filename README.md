# ☄️ NASA Near-Earth Object (NEO) Tracking & Insights

This project focuses on analyzing asteroid (Near-Earth Object) data from NASA to extract meaningful insights, clean and process the data, store it in a SQL database, and visualize patterns and anomalies. It combines data engineering and exploratory data analysis using Python, Pandas, SQL, and Flask.

## 📌 Project Objectives

- Preprocess NASA asteroid data for consistency and quality.
- Store structured data in a SQL database using Python.
- Build a web interface to explore the data (using Flask).
- Perform analysis to answer key questions like:
  - What are the top hazardous asteroids?
  - Which years had the most NEOs?
  - What is the average size of asteroids per year?
  - How many asteroids approached Earth per year?
 
  - 
## 🧰 Technologies Used
- **Python 3.x**
- **Jupyter Notebook**
- **Pandas & NumPy**
- **Matplotlib & Seaborn**
- **SQLite (via Python's sqlite3)**
- **Flask (for web interface)**
  
## 🗃️ Dataset

- **Source**: NASA NEO data (file: `asteroids_data.csv`)
- **Fields**:
  - `id`, `name`, `absolute_magnitude_h`, `is_potentially_hazardous_asteroid`
  - `estimated_diameter_min`, `estimated_diameter_max`
  - `relative_velocity`, `miss_distance`, `orbiting_body`, `close_approach_date`
- **Size**: ~900 records
