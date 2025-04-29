import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Defect Entry", layout="centered")
st.title("🛠️ Production Defect Tracker")

# Input fields
tag = st.text_input("📋 Scan or Enter Tag Number")
defect_type = st.selectbox("❌ Select Defect Type", [
    "Loose Stitching", "Piping Off", "Stain", "Torn Fabric", "Broken Frame", "Wrong Fabric", "Others"
])
responsible_person = st.text_input("🧑 Enter Name of Person Responsible")
comment = st.text_area("📝 Additional Notes (Optional)")
image = st.camera_input("📸 Capture Defect Photo")

if st.button("✅ Submit Entry"):
    if not tag:
        st.warning("Tag number is required.")
    elif not responsible_person:
        st.warning("Please enter the name of the person responsible.")
    else:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        image_path = None

        # Save image if provided
        if image:
            image_folder = "images"
            os.makedirs(image_folder, exist_ok=True)
            image_path = os.path.join(image_folder, f"{tag}_{timestamp.replace(':', '-')}.png")
            with open(image_path, "wb") as f:
                f.write(image.getbuffer())

        # Create a log entry
        entry = {
            "Timestamp": timestamp,
            "Tag Number": tag,
            "Defect Type": defect_type,
            "Responsible": responsible_person,
            "Comment": comment,
            "Image File": image_path if image else "No Image"
        }

        log_file = "defect_log.csv"
        df = pd.DataFrame([entry])

        if not os.path.exists(log_file):
            df.to_csv(log_file, index=False)
        else:
            df.to_csv(log_file, mode='a', header=False, index=False)

        st.success("✅ Defect entry saved successfully.")
