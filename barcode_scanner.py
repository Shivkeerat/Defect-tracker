import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Live Barcode Scanner", layout="centered")
st.title("📷 Streamlit Barcode Scanner (Webcam-based)")

components.html(
    """
    <script src="https://unpkg.com/html5-qrcode" type="text/javascript"></script>
    <div id="reader" width="600px"></div>
    <script>
        function docReady(fn) {
            if (document.readyState === "complete" || document.readyState === "interactive") {
                setTimeout(fn, 1);
            } else {
                document.addEventListener("DOMContentLoaded", fn);
            }
        }

        docReady(function () {
            var resultContainer = document.createElement('div');
            resultContainer.id = "scan-result";
            document.body.appendChild(resultContainer);

            function onScanSuccess(decodedText, decodedResult) {
                document.getElementById("scan-result").innerHTML = 
                    "<h3>✅ Scanned: " + decodedText + "</h3>";
            }

            var html5QrcodeScanner = new Html5QrcodeScanner(
                "reader", { fps: 10, qrbox: 250 });
            html5QrcodeScanner.render(onScanSuccess);
        });
    </script>
    """,
    height=500,
)
