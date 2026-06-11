import streamlit as st
import pandas as pd
import io

from parser import extract_commands
from diff_engine import compare_commands

st.title("FCCA - Firmware Command Change Analyzer")

old_pdf = st.file_uploader(
    "Upload Old CLI Manual",
    type=["pdf"]
)

new_pdf = st.file_uploader(
    "Upload New CLI Manual",
    type=["pdf"]
)

if old_pdf and new_pdf:

    if st.button("Generate Report"):

        with open("input/old.pdf", "wb") as f:
            f.write(old_pdf.read())

        with open("input/new.pdf", "wb") as f:
            f.write(new_pdf.read())

        old_cmds = extract_commands("input/old.pdf")
        new_cmds = extract_commands("input/new.pdf")

        added, removed, modified = compare_commands(
            old_cmds,
            new_cmds
        )

        st.success("Analysis Complete")

        col1, col2, col3 = st.columns(3)

        col1.metric("Added Commands", len(added))
        col2.metric("Removed Commands", len(removed))
        col3.metric("Modified Commands", len(modified))

        added_df = pd.DataFrame(added)
        removed_df = pd.DataFrame(removed)
        modified_df = pd.DataFrame(modified)

        st.subheader("Added Commands")
        st.dataframe(added_df)

        st.subheader("Removed Commands")
        st.dataframe(removed_df)

        st.subheader("Modified Commands")
        st.dataframe(modified_df)

        output = io.BytesIO()

        with pd.ExcelWriter(
            output,
            engine="openpyxl"
        ) as writer:

            added_df.to_excel(
                writer,
                sheet_name="Added",
                index=False
            )

            removed_df.to_excel(
                writer,
                sheet_name="Removed",
                index=False
            )

            modified_df.to_excel(
                writer,
                sheet_name="Modified",
                index=False
            )

        st.download_button(
            "Download FCCA Report",
            output.getvalue(),
            "FCCA_Report.xlsx"
        )
