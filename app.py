import streamlit as st
import re
import pandas as pd

st.set_page_config(page_title="Train Mobility Parser", layout="centered")
st.title("🚉 WhatsApp Train Mobility Parser")
st.markdown("Paste your daily train movement messages below to get a structured table.")

text_input = st.text_area("📥 Paste WhatsApp Messages Here:", height=300)

if st.button("🔍 Parse Message"):
    pattern = re.compile(
        r"(?P<line_num>\d+)\.\s*(?P<code1>[A-Z]+)?/?(?P<code2>[A-Z]+)?\s*"
        r"(?P<action>TO|S/D)?\s*(?P<time>\d{1,2}/\d{2})?\s*(AT\s+(?P<station>[A-Z]+))?"
        r"(?:\s+(?P<train_no>\d{4,5}))?", re.IGNORECASE
    )

    lines = text_input.splitlines()
    parsed_rows = []

    for line in lines:
        match = pattern.search(line)
        if match:
            parsed = match.groupdict()
            parsed_rows.append({
                "Line": parsed["line_num"],
                "From": parsed["code1"],
                "To": parsed["code2"],
                "Action": (parsed["action"] or "").upper(),
                "Time": parsed["time"],
                "Station": parsed["station"],
                "Train No": parsed["train_no"]
            })

    if parsed_rows:
        df = pd.DataFrame(parsed_rows)
        st.success("✅ Parsed Successfully!")
        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Download CSV", csv, "parsed_trains.csv", "text/csv")
    else:
        st.warning("❗ No valid lines found.")