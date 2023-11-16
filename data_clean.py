# remove following:
# * failed to render on ar5iv
# * failed to convert to markdown
# * duplicated (papers with versions)
import os
import json

PATH_PARENT = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
DATA_DIR = os.path.join(PATH_PARENT, "ar5iv")

IN_FILENAME = "paper_id_num_token.json"
CLEAN = "clean_dset.json"  # dedup id --> actual id
DIRTY = "dirty_dset.json"  # actual id --> reason

if __name__ == "__main__":
    skip_conversion = 0
    skip_duplicate = 0
    total_num_tok = 0
    clean = {}
    dirty = {}

    num_tokens = {}
    with open(IN_FILENAME, "r") as f:
        num_tokens = json.load(f)

    for id, num_tok in num_tokens.items():
        ym, num = id.split(".")
        num = num.split("v")[0]
        dedup_id = ".".join([ym, num])

        if num_tok < 256:
            # skip ar5iv failure
            skip_conversion += 1
            dirty[id] = "ar5iv/pandoc"
        elif dedup_id in clean:
            # skip duplicates
            skip_duplicate += 1
            dirty[id] = "duplicate"
        else:
            clean[dedup_id] = id  # actual link
            total_num_tok += num_tok

    print(f"skipped {skip_conversion} papers for conversion")
    print(f"skipped {skip_duplicate} papers for duplicate")
    print(f"out of {len(num_tokens)} papers")
    print(
        f"(skip {(skip_conversion + skip_duplicate) / len(num_tokens) * 100} %)"
    )
    print(f"total {total_num_tok} clean tokens")

    with open(CLEAN, "w") as f:
        json.dump(clean, f, indent=4)
    with open(DIRTY, "w") as f:
        json.dump(dirty, f, indent=4)
    print("done!")
