import streamlit as st
import pandas as pd
import io
import os

from parser import extract_commands
from diff_engine import compare_commands

st.set_page_config(
    page_title="FCCA - Firmware Command Change Analyzer",
    layout="wide"
)

st.title("FCCA - Firmware Command Change Analyzer")

st.markdown(
    """
    Compare two firmware CLI XML repositories and identify:

    - Added Commands
    - Removed Commands
    - Modified Commands
    """
)

old_zip = st.file_uploader(
    "Upload Old XML Repository (e.g. 10300)",
    type=["zip"]
)

new_zip = st.file_uploader(
    "Upload New XML Repository (e.g. 10400)",
    type=["zip"]
)

if old_zip and new_zip:

    if st.button("Generate Report"):

        with st.spinner("Analyzing XML repositories..."):

            os.makedirs("input", exist_ok=True)

            old_zip_path = "input/old.zip"
            new_zip_path = "input/new.zip"

            with open(old_zip_path, "wb") as f:
                f.write(old_zip.read())

            with open(new_zip_path, "wb") as f:
                f.write(new_zip.read())

            old_cmds = extract_commands(
                old_zip_path
            )

            new_cmds = extract_commands(
                new_zip_path
            )

            added, removed, modified = compare_commands(
                old_cmds,
                new_cmds
            )

        st.success("Analysis Complete")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Added Commands",
            len(added)
        )

        col2.metric(
            "Removed Commands",
            len(removed)
        )

        col3.metric(
            "Modified Commands",
            len(modified)
        )

        added_df = pd.DataFrame(added)
        removed_df = pd.DataFrame(removed)
        modified_df = pd.DataFrame(modified)

        st.divider()

        st.subheader("Added Commands")

        if not added_df.empty:
            st.dataframe(
                added_df,
                use_container_width=True
            )
        else:
            st.info("No added commands found.")

        st.divider()

        st.subheader("Removed Commands")

        if not removed_df.empty:
            st.dataframe(
                removed_df,
                use_container_width=True
            )
        else:
            st.info("No removed commands found.")

        st.divider()

        st.subheader("Modified Commands")

        if not modified_df.empty:
            st.dataframe(
                modified_df,
                use_container_width=True
            )
        else:
            st.info("No modified commands found.")

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

        output.seek(0)

        st.download_button(
            label="Download FCCA Report",
            data=output,
            file_name="FCCA_Report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
