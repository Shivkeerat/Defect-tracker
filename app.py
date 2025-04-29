import streamlit as st
from datetime import datetime
import pandas as pd
import os

st.set_page_config(page_title="Defect Tracker", layout="centered")
st.title("🛠️ Production Defect Tracker")

tag = st.text_input("📋 Scan or Enter Tag Number")
defect_type = st.selectbox("🔧 Select Defect Type", [
    "Loose Stitching", "Piping Off", "Foam Exposure", "Thread Breakage", "Stain", "Torn Fabric", "Others"
])
comment = st.text_area("📝 Additional Comments")

image = st.camera_input("📸 Capture Defect Photo")

if st.button("✅ Submit"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    image_path = None

    if image:
        image_folder = "images"
        os.makedirs(image_folder, exist_ok=True)
        image_path = os.path.join(image_folder, f"{tag}_{timestamp.replace(':', '-')}.png")
        with open(image_path, "wb") as f:
            f.write(image.getbuffer())

    entry = {
        "Timestamp": timestamp,
        "Tag": tag,
        "Defect Type": defect_type,
        "Comment": comment,
        "Image File": image_path if image else "No Image"
    }

    df = pd.DataFrame([entry])

    if not os.path.exists("defect_log.csv"):
        df.to_csv("defect_log.csv", index=False)
    else:
        df.to_csv("defect_log.csv", mode='a', header=False, index=False)

    st.success("✅ Entry recorded successfully!")
