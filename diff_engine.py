from rapidfuzz import fuzz

def compare_commands(old_cmds, new_cmds):

    old_names = set(old_cmds.keys())
    new_names = set(new_cmds.keys())

    added = []

    for cmd in sorted(new_names - old_names):

        added.append({
            "Section": new_cmds[cmd],
            "Command": cmd
        })

    removed = []

    for cmd in sorted(old_names - new_names):

        removed.append({
            "Section": old_cmds[cmd],
            "Command": cmd
        })

    modified = []

    for old_cmd in old_names:

        for new_cmd in new_names:

            score = fuzz.ratio(
                old_cmd,
                new_cmd
            )

            if 85 < score < 100:

                modified.append({
                    "Old Command": old_cmd,
                    "New Command": new_cmd,
                    "Similarity": round(score,2)
                })

    return added, removed, modified
