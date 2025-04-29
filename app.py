import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Defect Tracker", layout="centered")
st.title("🛠️ Production Defect Tracker")

# ------------------------- 🔍 BARCODE SCANNER (Working Camera) -------------------------
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
                    // Optional: ignore scan errors
                }
            );
        });
    </script>
    """,
    height=600,
)

# ------------------------- ✍️ MANUAL CONFIRMATION OF TAG -------------------------
st.markdown("### ✍️ Confirm or Enter the Scanned Tag Number")
tag = st.text_input("Enter the Tag Number shown above")

if tag:
    st.success(f"✅ Tag Confirmed: `{tag}`")

    # ------------------ Keep the rest of your original defect tracker logic below ------------------
    defect_type = st.selectbox("❌ Select Defect Type", [
        "Loose Stitching", "Piping Off", "Stain", "Torn Fabric", "Broken Frame", "Wrong Fabric", "Others"
    ])

    responsible_person = st.text_input("👷 Enter Name of Person Responsible")
    comment = st.text_area("📝 Additional Notes (Optional)")
    defect_image = st.camera_input("📸 Take a Picture of the Defect")

    if st.button("✅ Submit Entry"):
        if not responsible_person:
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

            st.success("✅ Defect entry submitted successfully.")
else:
    st.info("📷 Scan a barcode above and enter it here to continue.")
