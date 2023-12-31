import os
import json
import argparse

PATH_PARENT = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

parser = argparse.ArgumentParser()
parser.add_argument(
    "--path_arxivQA", type=str, default=os.path.join(PATH_PARENT, "ArXivQA")
)
args = parser.parse_args()

OUT_FILENAME = "paper_ids.json"
PATH = os.path.join(args.path_arxivQA, "papers")

if __name__ == "__main__":
    l = sorted([os.path.splitext(filename)[0] for filename in os.listdir(PATH)])
    print(f"{len(l)} papers")

    with open(OUT_FILENAME, "w") as f:
        json.dump(l, f, indent=4)
