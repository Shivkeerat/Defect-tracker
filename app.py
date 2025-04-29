import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Barcode Defect Tracker", layout="centered")
st.title("📦 Barcode Scanner + Defect Logger")

# ----------------------------------
# ✅ 1. LIVE BARCODE SCANNER CAMERA
# ----------------------------------
components.html(
    """
    <script src="https://unpkg.com/html5-qrcode" type="text/javascript"></script>
    <div id="reader" width="600px" style="margin: auto;"></div>
    <div id="scan-result" style="margin-top:20px; font-size:18px; color:green; text-align:center;"></div>
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
                    document.getElementById("scan-result").innerHTML =
                        "<h3>✅ Scanned: " + decodedText + "</h3>";
                    scanner.stop();
                },
                (errorMessage) => {
                    // Ignore scan errors
                }
            );
        });
    </script>
    """,
    height=600,
)

# ----------------------------------
# ✅ 2. ENTER THE TAG SEEN ABOVE
# ----------------------------------
st.markdown("### ✍️ Confirm the Scanned Tag")
tag = st.text_input("Enter the Tag Number shown above (manually)")

if tag:
    st.success(f"✅ Tag Confirmed: `{tag}`")

    # ----------------------------------
    # ✅ 3. DEFECT DETAILS ENTRY
    # ----------------------------------
    st.markdown("### 🛠️ Enter Defect Details")

    defect_type = st.selectbox("❌ Select Defect Type", [
        "Loose Stitching", "Piping Off", "Stain", "Torn Fabric",
        "Broken Frame", "Wrong Fabric", "Others"
    ])

    responsible_person = st.text_input("👷 Name of Person Responsible")
    comment = st.text_area("📝 Additional Notes (optional)")

    st.markdown("### 📸 Take a Picture of the Defect")
    defect_image = st.camera_input("Capture Defect Photo")

    # ----------------------------------
    # ✅ 4. SAVE LOG
    # ----------------------------------
    if st.button("✅ Submit Entry"):
        if not responsible_person:
            st.warning("Please enter the name of the responsible person.")
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
                "Comment": comment,
                "Defect Image": image_path if defect_image else "No Image"
            }

            df = pd.DataFrame([entry])

            log_file = "defect_log.csv"
            if not os.path.exists(log_file):
                df.to_csv(log_file, index=False)
            else:
                df.to_csv(log_file, mode='a', header=False, index=False)

            st.success("✅ Entry saved successfully.")
else:
    st.info("📷 Scan a barcode above and manually enter the tag to proceed.")
