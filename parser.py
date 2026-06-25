import zipfile
import xml.etree.ElementTree as ET
from io import BytesIO


def extract_commands(zip_path):

    commands = {}

    with zipfile.ZipFile(zip_path, "r") as zip_ref:

        xml_files = [
            f for f in zip_ref.namelist()
            if f.endswith(".xml")
        ]

        print(f"XML FILES FOUND = {len(xml_files)}")

        for xml_file in xml_files:

            try:

                xml_content = zip_ref.read(xml_file)

                root = ET.fromstring(xml_content)

                walk_commands(
                    root,
                    commands,
                    xml_file
                )

            except Exception as e:

                print(
                    f"ERROR parsing {xml_file}: {e}"
                )

    print(
        f"TOTAL COMMANDS FOUND = {len(commands)}"
    )

    return commands


def walk_commands(
    node,
    commands,
    source_file,
    parent_path=""
):

    tag = node.tag.split("}")[-1]

    if tag == "command":

        cmd_name = node.attrib.get("name", "")

        if cmd_name:

            full_path = (
                f"{parent_path} {cmd_name}"
            ).strip()

            commands[full_path] = {
                "file": source_file,
                "help": node.attrib.get(
                    "help",
                    ""
                ),
                "feature_id": node.attrib.get(
                    "feature_id",
                    ""
                )
            }

            parent_path = full_path

    for child in node:

        walk_commands(
            child,
            commands,
            source_file,
            parent_path
        )
