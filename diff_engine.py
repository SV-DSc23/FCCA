def compare_commands(
    old_cmds,
    new_cmds
):

    old_names = set(old_cmds.keys())
    new_names = set(new_cmds.keys())

    added = []

    for cmd in sorted(
        new_names - old_names
    ):

        added.append(
            {
                "Command": cmd,
                "Source File":
                    new_cmds[cmd]["file"]
            }
        )

    removed = []

    for cmd in sorted(
        old_names - new_names
    ):

        removed.append(
            {
                "Command": cmd,
                "Source File":
                    old_cmds[cmd]["file"]
            }
        )

    modified = []

    common = old_names.intersection(
        new_names
    )

    for cmd in sorted(common):

        old_data = old_cmds[cmd]
        new_data = new_cmds[cmd]

        changes = []

        if (
            old_data["help"]
            != new_data["help"]
        ):
            changes.append(
                "Help Text"
            )

        if (
            old_data["feature_id"]
            != new_data["feature_id"]
        ):
            changes.append(
                "Feature ID"
            )

        if changes:

            modified.append(
                {
                    "Command": cmd,
                    "Changed Fields":
                        ", ".join(changes),
                    "Old Help":
                        old_data["help"],
                    "New Help":
                        new_data["help"],
                    "Old Feature":
                        old_data["feature_id"],
                    "New Feature":
                        new_data["feature_id"]
                }
            )

    return (
        added,
        removed,
        modified
    )
