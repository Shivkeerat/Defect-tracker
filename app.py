import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Defect Tracker", layout="centered")
st.title("🛠️ Production Defect Tracker")

# Step 1: Select scan method
scan_method = st.selectbox("🔍 How would you like to scan the tag?", ["Enter Number Manually", "Open Camera to Scan"])

tag = ""

# Step 2: Handle input based on scan method
if scan_method == "Enter Number Manually":
    tag = st.text_input("📋 Enter Tag Number")
else:
    barcode_image = st.camera_input("📷 Scan/Take a Picture of the Barcode")
    tag = st.text_input("📝 After scanning, enter the decoded Tag Number manually")

# Step 3: Enter defect and responsible person
defect_type = st.selectbox("❌ Select Defect Type", [
    "Loose Stitching", "Piping Off", "Stain", "Torn Fabric", "Broken Frame", "Wrong Fabric", "Others"
])

responsible_person = st.text_input("👷 Enter Name of Person Responsible")
comment = st.text_area("🗒️ Additional Notes (Optional)")

# Step 4: Take a photo of the actual defect
defect_image = st.camera_input("📸 Take a Picture of the Defect")

if st.button("✅ Submit Entry"):
    if not tag:
        st.warning("Please enter the Tag Number.")
    elif not responsible_person:
        st.warning("Please enter the name of the person responsible.")
    else:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        image_path = None

        if defect_image:
            image_folder = "images"
            os.makedirs(image_folder, exist_ok=True)
            image_path = os.path.join(image_folder, f"{tag}_{timestamp.replace(':', '-')}.png")
            with open(image_path, "wb") as f:
                f.write(defect_image.getbuffer())

        # Prepare data for CSV
        entry = {
            "Timestamp": timestamp,
            "Tag Number": tag,
            "Defect Type": defect_type,
            "Responsible": responsible_person,
            "Comment": comment,
            "Defect Image": image_path if defect_image else "No Image"
        }

        log_file = "defect_log.csv"
        df = pd.DataFrame([entry])

        if not os.path.exists(log_file):
            df.to_csv(log_file, index=False)
        else:
            df.to_csv(log_file, mode='a', header=False, index=False)

        st.success("✅ Defect entry submitted successfully.")
