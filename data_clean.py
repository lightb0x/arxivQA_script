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
    skipped = 0
    total_num_tok = 0
    clean = {}
    dirty = {}

    num_tokens = {}
    with open(IN_FILENAME, "r") as f:
        num_tokens = json.load(f)

    for id, num_tok in num_tokens:
        ym, num = id.split(".")
        num = num.split("v")[0]
        dedup_id = ".".join([ym, num])

        if num_tok < 256:
            # skip ar5iv failure
            skipped += 1
            dirty[id] = "ar5iv/pandoc"
        elif dedup_id in clean:
            # skip duplicates
            skipped += 1
            dirty[id] = "duplicate"
        else:
            clean[dedup_id] = id  # actual link
            total_num_tok += num_tok

    print(f"skipped {skipped} out of {len(num_tokens)} papers")
    print(f"total {total_num_tok} tokens")

    print("saving...")
    with open(CLEAN, "w") as f:
        json.dump(clean, f, indent=4)
    with open(DIRTY, "w") as f:
        json.dump(dirty, f, indent=4)
    print("done!")
