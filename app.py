import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Barcode Defect Tracker", layout="centered")
st.title("🛠️ Barcode Scanner + Defect Logger")

# ✅ 1. Get scanned tag from URL query parameters (if scanner fills it)
query_params = st.query_params
auto_tag = query_params.get("scanned", [None])[0]

# ✅ 2. Live Camera Barcode Scanner with working JavaScript (html5-qrcode)
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
                    const base = window.location.href.split('?')[0];
                    window.location.href = base + "?scanned=" + encodeURIComponent(decodedText);
                    scanner.stop();
                },
                (errorMessage) => {
                    // ignore scan errors
                }
            );
        });
    </script>
    """,
    height=600,
)

# ✅ 3. Tag Input Field (auto-filled if scanned, manual fallback)
st.markdown("### ✍️ Confirm or Enter Tag Number")
if auto_tag:
    st.success(f"✅ Tag Scanned: `{auto_tag}`")
    tag = st.text_input("Tag Number", value=auto_tag)
else:
    st.info("📷 Scan the tag above, or enter manually if scanning fails.")
    tag = st.text_input("Tag Number")

# ✅ 4. Defect Details Form
if tag:
    defect_type = st.selectbox("❌ Select Defect Type", [
        "Loose Stitching", "Piping Off", "Stain", "Torn Fabric",
        "Broken Frame", "Wrong Fabric", "Others"
    ])

    responsible_person = st.text_input("👷 Name of Person Responsible")
    defect_description = st.text_area("📄 Defect Description (optional)")

    st.markdown("### 📸 Take a Picture of the Defect")
    defect_image = st.camera_input("Capture Defect Photo")

    if st.button("✅ Submit Entry"):
        if not responsible_person:
            st.warning("⚠️ Please enter the name of the responsible person.")
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

            df = pd.DataFrame([entry])
            log_file = "defect_log.csv"

            if not os.path.exists(log_file):
                df.to_csv(log_file, index=False)
            else:
                df.to_csv(log_file, mode='a', header=False, index=False)

            st.success("✅ Entry saved successfully.")
