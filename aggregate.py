import os
import json

PATH_PARENT = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
DATA_DIR = os.path.join(PATH_PARENT, "ar5iv")

if __name__ == "__main__":
    aggregate = []
    for yymm in os.listdir(DATA_DIR):
        for num in os.listdir(os.path.join(DATA_DIR, yymm)):
            arxiv_id = ".".join([yymm, num, "json"])
            if os.path.exists(os.path.join(DATA_DIR, yymm, num, arxiv_id)):
                with open(
                    os.path.join(DATA_DIR, yymm, num, arxiv_id), "r"
                ) as f:
                    data = json.load(f)
                    aggregate.append(data)

    with open("arxivQA_v4.json", "w") as f:
        json.dump(aggregate, f, indent=4)
