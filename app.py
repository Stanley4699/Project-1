import streamlit as st
import pandas as pd
from sqlalchemy import create_engine


engine = create_engine('mysql+pymysql://root:12345@localhost:3306/astro')

st.title("🚀 NASA Asteroids Dashboard")

st.sidebar.header("🔍 Filter Options")

name_filter = st.sidebar.text_input("Asteroid Name", "")
hazardous = st.sidebar.selectbox("Potentially Hazardous?", ["All", "Yes", "No"])
diameter_min = float(pd.read_sql("SELECT MIN(estimated_diameter_min) FROM asteroids", engine).iloc[0,0])
diameter_max = float(pd.read_sql("SELECT MAX(estimated_diameter_max) FROM asteroids", engine).iloc[0,0])
diameter_range = st.sidebar.slider("Estimated Diameter Range (km)", min_value=diameter_min, max_value=diameter_max, value=(diameter_min, diameter_max))
h_min = float(pd.read_sql("SELECT MIN(absolute_magnitude_h) FROM asteroids", engine).iloc[0,0])
h_max = float(pd.read_sql("SELECT MAX(absolute_magnitude_h) FROM asteroids", engine).iloc[0,0])
magnitude_range = st.sidebar.slider("Absolute Magnitude Range", min_value=h_min, max_value=h_max, value=(h_min, h_max))

velocity_min = float(pd.read_sql("SELECT MIN(relative_velocity) FROM close_approach", engine).iloc[0,0])
velocity_max = float(pd.read_sql("SELECT MAX(relative_velocity) FROM close_approach", engine).iloc[0,0])
velocity_range = st.sidebar.slider("Relative Velocity Range (km/s)", min_value=velocity_min, max_value=velocity_max, value=(velocity_min, velocity_max))

miss_distance_min = float(pd.read_sql("SELECT MIN(miss_distance_km) FROM close_approach", engine).iloc[0,0])
miss_distance_max = float(pd.read_sql("SELECT MAX(miss_distance_km) FROM close_approach", engine).iloc[0,0])
miss_distance_range = st.sidebar.slider("Miss Distance Range (km)", min_value=miss_distance_min, max_value=miss_distance_max, value=(miss_distance_min, miss_distance_max))

date_range = st.sidebar.date_input("Close Approach Date Range", [])


if st.sidebar.button("Apply Filter"):
    query = """
        SELECT 
            a.id, a.name, a.absolute_magnitude_h, a.estimated_diameter_min, a.estimated_diameter_max,
            a.is_potentially_hazardous_asteroid,
            c.close_approach_date, c.relative_velocity, c.miss_distance_km, c.orbiting_body
        FROM asteroids a
        JOIN close_approach c ON a.id = c.neo_list_id
        WHERE a.estimated_diameter_min >= %s AND a.estimated_diameter_max <= %s
    """
    filters = [diameter_range[0], diameter_range[1]]

    if name_filter:
        query += " AND a.name LIKE %s"
        filters.append(f"%{name_filter}%")

    if hazardous != "All":
        query += " AND a.is_potentially_hazardous_asteroid = %s"
        filters.append(hazardous)

    if magnitude_range:
        query += " AND a.absolute_magnitude_h BETWEEN %s AND %s"
        filters.append(magnitude_range[0])
        filters.append(magnitude_range[1])

    if len(date_range) == 2:
        query += " AND c.close_approach_date BETWEEN %s AND %s"
        filters.append(date_range[0])
        filters.append(date_range[1])

    if velocity_range:
        query += " AND c.relative_velocity BETWEEN %s AND %s"
        filters.append(velocity_range[0])
        filters.append(velocity_range[1])

    if miss_distance_range:
        query += " AND c.miss_distance_km BETWEEN %s AND %s"
        filters.append(miss_distance_range[0])
        filters.append(miss_distance_range[1])

    df_filtered = pd.read_sql(query, engine, params=tuple(filters))

    total_hazardous = df_filtered['is_potentially_hazardous_asteroid'].sum()
    st.metric("Hazardous Count", total_hazardous)

    st.subheader("📄 Filtered Asteroid Data")
    st.dataframe(df_filtered)
else:
    st.info("Use the sidebar to filter data and click 'Apply Filter'.")

if 'diameter_range' not in st.session_state:
    st.session_state.diameter_range = (float(pd.read_sql("SELECT MIN(estimated_diameter_min) FROM asteroids", engine).iloc[0,0]),
                                       float(pd.read_sql("SELECT MAX(estimated_diameter_max) FROM asteroids", engine).iloc[0,0]))
if 'magnitude_range' not in st.session_state:
    st.session_state.magnitude_range = (float(pd.read_sql("SELECT MIN(absolute_magnitude_h) FROM asteroids", engine).iloc[0,0]),
                                       float(pd.read_sql("SELECT MAX(absolute_magnitude_h) FROM asteroids", engine).iloc[0,0]))
if 'velocity_range' not in st.session_state:
    st.session_state.velocity_range = (float(pd.read_sql("SELECT MIN(relative_velocity) FROM close_approach", engine).iloc[0,0]),
                                       float(pd.read_sql("SELECT MAX(relative_velocity) FROM close_approach", engine).iloc[0,0]))
if 'miss_distance_range' not in st.session_state:
    st.session_state.miss_distance_range = (float(pd.read_sql("SELECT MIN(miss_distance_km) FROM close_approach", engine).iloc[0,0]),
                                           float(pd.read_sql("SELECT MAX(miss_distance_km) FROM close_approach", engine).iloc[0,0]))
if 'name_filter' not in st.session_state:
    st.session_state.name_filter = ''
if 'hazardous' not in st.session_state:
    st.session_state.hazardous = 'All'
if 'date_range' not in st.session_state:
    st.session_state.date_range = []


st.sidebar.header("🔍 Select a Predefined Query:")
query_options = [
    "Count how many times each asteroid has approached Earth",
    "Average velocity of each asteroid over multiple approaches",
    "List top 10 fastest asteroids",
    "Find potentially hazardous asteroids that have approached Earth more than 3 times",
    "Find the month with the most asteroid approaches",
    "Get the asteroid with the fastest ever approach speed",
    "Sort asteroids by maximum estimated diameter (descending)",
    "Asteroids whose closest approach is getting nearer over time",
    "Display the name of each asteroid along with the date and miss distance of its closest approach to Earth",
    "List names of asteroids that approached Earth with velocity > 50,000 km/h",
    "Count how many approaches happened per month",
    "Find asteroid with the highest brightness (lowest magnitude value)",
    "Get number of hazardous vs non-hazardous asteroids",
    "Find asteroids that passed closer than the Moon (lesser than 1 LD), along with their close approach date and distance",
    "Find asteroids that came within 0.05 AU (astronomical distance)",
    "Find asteroids that passed closer than 0.05 AU (astronomical unit)",
    "List the name and estimated diameter of asteroids that have a diameter greater than 1 km",
    "Find the asteroid with the highest miss distance during its closest approach",
    "List all asteroids that have a close approach date in the future",
    "Find asteroids with a relative velocity between 20,000 km/h and 100,000 km/h"
]

query = st.sidebar.selectbox("Choose a question to run", query_options)

def process_query(query):
    query = query.lower()
    
    if 'approach' in query and 'count' in query:
        return """
            SELECT a.name, COUNT(c.neo_list_id) AS approach_count
            FROM asteroids a
            JOIN close_approach c ON a.id = c.neo_list_id
            GROUP BY a.name
        """
    elif 'velocity' in query and 'average' in query:
        return """
            SELECT a.name, AVG(c.relative_velocity) AS avg_velocity
            FROM asteroids a
            JOIN close_approach c ON a.id = c.neo_list_id
            GROUP BY a.name
        """
    elif 'top 10' in query and 'fastest' in query:
        return """
            SELECT a.name, MAX(c.relative_velocity) AS max_velocity
            FROM asteroids a
            JOIN close_approach c ON a.id = c.neo_list_id
            GROUP BY a.name
            ORDER BY max_velocity DESC
            LIMIT 10
        """
    elif 'hazardous' in query and 'more than 3' in query:
        return """
            SELECT a.name, COUNT(c.neo_list_id) AS approach_count
            FROM asteroids a
            JOIN close_approach c ON a.id = c.neo_list_id
            WHERE a.is_potentially_hazardous_asteroid = 'Yes'
            GROUP BY a.name
            HAVING COUNT(c.neo_list_id) > 3
        """
    elif 'most approaches' in query:
        return """
            SELECT EXTRACT(MONTH FROM c.close_approach_date) AS month, COUNT(*) AS approach_count
            FROM close_approach c
            GROUP BY month
            ORDER BY approach_count DESC
            LIMIT 1
        """
    elif 'fastest ever' in query:
        return """
            SELECT a.name, MAX(c.relative_velocity) AS max_velocity
            FROM asteroids a
            JOIN close_approach c ON a.id = c.neo_list_id
            GROUP BY a.name
            ORDER BY max_velocity DESC
            LIMIT 1
        """
    elif 'largest diameter' in query:
        return """
            SELECT a.name, MAX(a.estimated_diameter_max) AS max_diameter
            FROM asteroids a
            GROUP BY a.name
            ORDER BY max_diameter DESC
        """
    elif 'closer over time' in query:
        return """
            SELECT a.name, c.close_approach_date, c.miss_distance_km
            FROM asteroids a
            JOIN close_approach c ON a.id = c.neo_list_id
            ORDER BY c.close_approach_date ASC, c.miss_distance_km ASC
        """
    elif 'approaches velocity' in query:
        return """
            SELECT a.name, c.close_approach_date, c.relative_velocity
            FROM asteroids a
            JOIN close_approach c ON a.id = c.neo_list_id
            WHERE c.relative_velocity > 50000
        """
    elif 'highest brightness' in query:
        return """
            SELECT a.name, MIN(a.absolute_magnitude_h) AS brightest
            FROM asteroids a
            GROUP BY a.name
            ORDER BY brightest ASC
            LIMIT 1
        """
    elif 'hazardous count' in query:
        return """
            SELECT a.is_potentially_hazardous_asteroid, COUNT(*) AS count
            FROM asteroids a
            GROUP BY a.is_potentially_hazardous_asteroid
        """
    elif 'moon distance' in query:
        return """
            SELECT a.name, c.close_approach_date, c.miss_distance_km
            FROM asteroids a
            JOIN close_approach c ON a.id = c.neo_list_id
            WHERE c.miss_distance_km < 384400
        """
    elif '0.05 au' in query:
        return """
            SELECT a.name, c.close_approach_date, c.miss_distance_km
            FROM asteroids a
            JOIN close_approach c ON a.id = c.neo_list_id
            WHERE c.miss_distance_km < 0.05
        """
    elif 'closer than 0.05 au' in query:
        return """
            SELECT a.name, c.close_approach_date, c.miss_distance_km
            FROM asteroids a
            JOIN close_approach c ON a.id = c.neo_list_id
            WHERE c.miss_distance_km < 0.05
        """
    elif 'diameter greater than 1 km' in query:
        return """
            SELECT a.name, a.estimated_diameter_min, a.estimated_diameter_max
            FROM asteroids a
            WHERE a.estimated_diameter_min > 1 OR a.estimated_diameter_max > 1
        """
    elif 'highest miss distance' in query:
        return """
            SELECT a.name, MAX(c.miss_distance_km) AS max_miss_distance
            FROM asteroids a
            JOIN close_approach c ON a.id = c.neo_list_id
            GROUP BY a.name
            ORDER BY max_miss_distance DESC
            LIMIT 1
        """
    elif 'close approach in future' in query:
        return """
            SELECT a.name, c.close_approach_date
            FROM asteroids a
            JOIN close_approach c ON a.id = c.neo_list_id
            WHERE c.close_approach_date > NOW()
        """
    elif 'relative velocity between' in query:
        return """
            SELECT a.name, c.relative_velocity
            FROM asteroids a
            JOIN close_approach c ON a.id = c.neo_list_id
            WHERE c.relative_velocity BETWEEN 20000 AND 100000
        """
    else:
        return None  

if query:
    sql_query = process_query(query)
    if sql_query:
        df = pd.read_sql(sql_query, engine)
        st.subheader("📄 Query Result")
        st.dataframe(df)
    else:
        st.warning("Sorry, I couldn't understand the query")