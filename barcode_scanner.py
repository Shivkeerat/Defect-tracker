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
                // Optional: log errors
            }
        );
    });
</script>
