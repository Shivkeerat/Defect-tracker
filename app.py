import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Defect Tracker", layout="centered")
st.title("🛠️ Barcode Scanner + Defect Logger")

# ------------------------- 📤 Get Tag from URL Params if Passed -------------------------
query_params = st.experimental_get_query_params()
auto_tag = query_params.get("scanned", [None])[0]

# ------------------------- 📷 Barcode Scanner Component -------------------------
components.html(
    """
    <script src="https://unpkg.com/html5-qrcode" type="text/javascript"></script>
    <div id="reader" width="600px" style="margin: auto;"></div>
    <script>
        function docReady(fn) {
            if (document.readyState === "complete" || document.readyState === "interactive") {
                setTimeout(fn, 1);
            } else {
                document.addEventListener("DOMContentLoaded", fn);
            }
        }

        docReady(function () {
            const config = {
                fps: 10,
                qrbox: { width: 300, height: 150 },
                formatsToSupport: [
                    Html5QrcodeSupportedFormats.CODE_128,
                    Html5QrcodeSupportedFormats.EAN_13,
                    Html5QrcodeSupportedFormats.UPC_A
                ]
            };

            const scanner = new Html5Qrcode("reader");

            scanner.start(
                { facingMode: "environment" },
                config,
                (decodedText, decodedResult) => {
                    // Send scanned result to parent window (Streamlit)
                    const base = window.location.href.split('?')[0];
                    window.location.href = base + "?scanned=" + encodeURIComponent(decodedText);
                    scanner.stop();
                },
                (errorMessage) => {
                    // Ignore errors
                }
            );
        });
    </script>
    """,
    height=600,
)

# ------------------------- 🧠 Tag Field (auto or manual) -------------------------
st.markdown("### ✍️ Tag Number")

if auto_tag:
    st.success(f"✅ Scanned Tag Detected: `{auto_tag}`")
    tag = st.text_input("Tag Number", value=auto_tag)
else:
    st.info("📷 Please scan a barcode above or enter manually if scanning fails.")
    tag = st.text_input("Tag Number")

# ------------------------- 📄 Form Fields -------------------------
if tag:
    defect_type = st.selectbox("❌ Select Defect Type", [
        "Loose Stitching", "Piping Off", "Stain", "Torn Fabric",
        "Broken Frame", "Wrong Fabric", "Others"
    ])

    responsible_person = st.text_input("👷 Name of Person Responsible")
    defect_description = st.text_area("📄 Defect Description (optional)")

    st.markdown("### 📸 Take a Photo of the Defect")
    defect_image = st.camera_input("Capture Defect Image")

    if st.button("✅ Submit Entry"):
        if not responsible_person:
            st.warning("⚠️ Please enter the responsible person.")
        else:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            image_path = None

            if defect_image:
                image_folder = "images"
                os.makedirs(image_folder, exist_ok=True)
                image_path = os.path.join(image_folder, f"{tag}_{timestamp.replace(':', '-')}.png")
                with open(image_path, "wb") as f:
                    f.write(defect_image.getbuffer())

            entry = {
                "Timestamp": timestamp,
                "Tag Number": tag,
                "Defect Type": defect_type,
                "Responsible Person": responsible_person,
                "Defect Description": defect_description,
                "Defect Image": image_path if image_path else "No Image"
            }

            log_file = "defect_log.csv"
            df = pd.DataFrame([entry])

            if not os.path.exists(log_file):
                df.to_csv(log_file, index=False)
            else:
                df.to_csv(log_file, mode='a', header=False, index=False)

            st.success("✅ Entry saved successfully.")
