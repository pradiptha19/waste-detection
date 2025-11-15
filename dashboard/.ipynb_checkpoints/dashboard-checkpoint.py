pip install streamlit pandas matplotlib


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

# Set page title
st.set_page_config(page_title="Waste Detection Dashboard", layout="wide")

# Title and Introduction
st.title("🌊 Waste Detection Dashboard")
st.markdown("Real-time monitoring and analytics for plastic waste detection system")

# Load detection data (from your database or CSV)
# For testing, create a sample DataFrame
sample_data = {
    'timestamp': [
        '2025-11-14 10:00:00',
        '2025-11-14 10:15:00',
        '2025-11-14 10:30:00'
    ],
    'waste_count': [2, 5, 3],
    'confidence_avg': [0.85, 0.82, 0.91],
    'location': ['Channasandra, Bangalore', 'Channasandra, Bangalore', 'Channasandra, Bangalore'],
    'image_path': ['waste_2items_62-_20251114_183325.jpg',
                   'waste_5items_61-_20251113_233528.jpg',
                   'waste_3items_85-_20251113_111251.jpg']
}
df = pd.DataFrame(sample_data)

# Display latest detections
st.subheader("Latest Detections")
st.dataframe(df)

# Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("Waste Detected Over Time")
    fig, ax = plt.subplots()
    df_sorted = df.sort_values('timestamp')
    ax.plot(df_sorted['timestamp'], df_sorted['waste_count'], marker='o')
    ax.set_xlabel("Time")
    ax.set_ylabel("Items Detected")
    plt.xticks(rotation=45)
    st.pyplot(fig)

with col2:
    st.subheader("Confidence Level")
    fig, ax = plt.subplots()
    ax.bar(df['timestamp'], df['confidence_avg'])
    ax.set_xlabel("Time")
    ax.set_ylabel("Avg Confidence")
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Show detected images
st.subheader("Detected Images")
images_per_row = 3
for i in range(0, len(df), images_per_row):
    cols = st.columns(images_per_row)
    for col, j in zip(cols, range(i, min(i+images_per_row, len(df)))):
        if j < len(df):
            image_path = df.iloc[j]['image_path']
            # Use the attached image file path
            if os.path.exists(image_path):
                col.image(image_path, caption=f"{df.iloc[j]['waste_count']} items", use_column_width=True)
            else:
                col.write("Image not found")

# Info and help
st.sidebar.title("Info")
st.sidebar.info("Latest 10 detections")
st.sidebar.dataframe(df.tail(10))

st.sidebar.markdown("---")
st.sidebar.markdown("Built with Streamlit for real-time waste detection analytics.")

# Run Streamlit
if __name__ == "__main__":
    pass


