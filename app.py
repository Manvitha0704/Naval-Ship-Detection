import streamlit as st
from PIL import Image
import os
import subprocess
import uuid
import pandas as pd

# -------------------------------------
# Page Configuration
# -------------------------------------
st.set_page_config(page_title="Naval Ship Detection", layout="centered")

# -------------------------------------
# Custom Styling
# -------------------------------------
st.markdown(
    """
    <style>
    .main {background-color:#f2f8ff;}
    .title {text-align:center;font-size:40px;font-weight:bold;color:#003366;margin-bottom:10px;}
    .subtitle {text-align:center;font-size:18px;color:#555;margin-bottom:30px;}
    .stButton>button {background-color:#003366;color:white;font-weight:bold;border-radius:8px;padding:10px 20px;}
    .footer {text-align:center;font-size:14px;color:#888;margin-top:40px;}
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------
# Title
# -------------------------------------
st.markdown('<div class="title">🚢 Naval Ship Detection</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Internship project – YOLOv5 × ShipRSImageNet.v39i</div>', unsafe_allow_html=True)
st.markdown("---")

# -------------------------------------
# Performance Metrics
# -------------------------------------
def load_metrics():
    results_csv = os.path.join("yolov5", "runs", "train", "shiprs_yolov5s2", "results.csv")
    if not os.path.exists(results_csv):
        return None
    df = pd.read_csv(results_csv)
    df.columns = [c.strip() for c in df.columns]
    last = df.iloc[-1]
    try:
        return {
            "Epoch": int(last["epoch"]),
            "Precision": round(last["metrics/precision"], 3),
            "Recall": round(last["metrics/recall"], 3),
            "mAP@0.5": round(last["metrics/mAP_0.5"], 3),
            "mAP@0.5:0.95": round(last["metrics/mAP_0.5:0.95"], 3),
        }
    except KeyError:
        return None

st.subheader("📈 Model Performance")
m = load_metrics()
if m:
    for k, v in m.items():
        st.markdown(f"**{k}:** {v}")
else:
    st.info("Metrics CSV not found or columns missing.")
st.markdown("---")

# -------------------------------------
# File Uploader
# -------------------------------------
st.subheader("📤 Upload an Image")
file = st.file_uploader("Upload .jpg / .png", type=["jpg", "jpeg", "png"])

if file:
    img = Image.open(file).convert("RGB")
    uid = str(uuid.uuid4())
    input_img = f"input_{uid}.jpg"
    img.save(input_img)

    st.image(img, caption="Uploaded image", use_container_width=True)

    if st.button("🔍 Run Detection"):
        st.info("Running YOLOv5 detection…")

        # ---- paths ----
        detect_script = os.path.join("yolov5", "detect.py")
        weights = os.path.join("yolov5", "runs", "train", "shiprs_yolov5s2", "weights", "best.pt")
        output_dir = os.path.join("yolov5", "runs", "detect", f"streamlit_{uid}")

        cmd = [
            "python", detect_script,
            "--weights", weights,
            "--source", input_img,
            "--conf", "0.25",
            "--name", f"streamlit_{uid}",
            "--save-txt"
        ]

        # st.write("Command:", " ".join(cmd))  # uncomment to debug
        subprocess.run(cmd)

        output_img = os.path.join(output_dir, os.path.basename(input_img))
        if os.path.exists(output_img):
            st.success("✅ Detection complete!")
            st.image(output_img, caption="Detected output", use_container_width=True)
        else:
            st.error("❌ Detection failed – check model path or Streamlit logs.")

        os.remove(input_img)

# -------------------------------------
# Footer
# -------------------------------------
st.markdown('<div class="footer">🚀 Developed by Manvitha | Internship 2025</div>', unsafe_allow_html=True)
