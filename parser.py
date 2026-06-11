import pdfplumber
import re

def extract_commands(pdf_path):

    commands = {}

    print(f"\nOPENING PDF: {pdf_path}")

    with pdfplumber.open(pdf_path) as pdf:

        print(f"TOTAL PAGES = {len(pdf.pages)}")

        for page in pdf.pages:

            text = page.extract_text()

            if not text:
                continue

            lines = text.split("\n")

            for line in lines:

                line = line.strip()

                match = re.match(
                    r'^(\d+(?:\.\d+)+)\s+(.+)$',
                    line
                )

                if match:

                    section = match.group(1)
                    command = match.group(2).strip()

                    if (
                        len(command) > 3
                        and "Mode:" not in command
                        and "Privilege" not in command
                        and "Format:" not in command
                    ):

                        commands[command] = section

    print(
        f"COMMANDS FOUND = {len(commands)}"
    )

    return commands
