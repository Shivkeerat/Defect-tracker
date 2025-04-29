import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Defect Tracker", layout="centered")
st.title("🛠️ Barcode Scanner + Defect Logger")

# ✅ Read scanned tag from URL
query_params = st.query_params
scanned_tag = query_params.get("scanned", [None])[0]

# ✅ Barcode scanner (html5-qrcode)
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

# ✅ Show form ONLY if a tag was scanned
if scanned_tag:
    st.success(f"✅ Tag Scanned: `{scanned_tag}`")

    defect_type = st.selectbox("❌ Select Defect Type", [
        "Loose Stitching", "Piping Off", "Stain", "Torn Fabric",
        "Broken Frame", "Wrong Fabric", "Others"
    ])

    st.markdown("### 📸 Take a Photo of the Defect")
    defect_image = st.camera_input("Capture Defect Image")

    if st.button("✅ Submit Entry"):
        if not defect_image:
            st.warning("⚠️ Please capture the defect image.")
        else:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            image_path = None

            # Save the image
            image_folder = "images"
            os.makedirs(image_folder, exist_ok=True)
            image_path = os.path.join(image_folder, f"{scanned_tag}_{timestamp.replace(':', '-')}.png")
            with open(image_path, "wb") as f:
                f.write(defect_image.getbuffer())

            # Prepare data entry
            entry = {
                "Timestamp": timestamp,
                "Tag Number": scanned_tag,
                "Defect Type": defect_type,
                "Defect Image": image_path
            }

            log_file = "defect_log.csv"
            df = pd.DataFrame([entry])

            if not os.path.exists(log_file):
                df.to_csv(log_file, index=False)
            else:
                df.to_csv(log_file, mode='a', header=False, index=False)

            st.success("✅ Defect entry saved successfully.")
else:
    st.info("📷 Please scan a barcode above to proceed with defect logging.")
