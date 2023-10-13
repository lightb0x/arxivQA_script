import os
import subprocess
import json
import argparse
from collections import OrderedDict

PATH_PARENT = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

parser = argparse.ArgumentParser()
parser.add_argument("--start_index", type=int, default=0)
parser.add_argument("--end_index", type=int, default=10)
parser.add_argument(
    "--path_storage", type=str, default=os.path.join(PATH_PARENT, "ar5iv")
)
args = parser.parse_args()

IN_FILENAME = "paper_ids.json"
OUT_FILENAME = "paper_id_numchar.json"

if __name__ == "__main__":
    start_index = args.start_index
    end_index = args.end_index

    id2numchar = {}
    if os.path.exists(OUT_FILENAME):
        with open(OUT_FILENAME, "r") as f:
            id2numchar = json.load(f)

    with open(IN_FILENAME, "r") as f:
        ids = json.load(f)
        for i, id in enumerate(ids[start_index:end_index]):
            print(
                f"{start_index + i} / {end_index} : {id}...", end="", flush=True
            )
            dir = os.path.join(args.path_storage, id)

            if not os.path.exists(dir):
                os.mkdir(dir)

            filename = os.path.join(dir, f"{id}.md")

            if not os.path.exists(filename):
                # pandoc
                # arxiv number --> URL --> HTML --> Markdown
                subprocess.run(
                    f"""docker run --rm \
                        --volume "{dir}:/data" \
                        --volume "{dir}/assets:/assets" \
                        --user $(id -u):$(id -g) \
                        pandoc/latex\
                        -s -r html https://ar5iv.org/abs/{id}\
                        --extract-media=assets\
                        --mathml\
                        -t html\
                        -o {id}.html
                        """,
                    shell=True,
                )
                subprocess.run(
                    f"""docker run --rm \
                        --volume "{dir}:/data" \
                        --volume "{dir}/assets:/assets" \
                        --user $(id -u):$(id -g) \
                        pandoc/latex\
                        -f html\
                        {id}.html\
                        -t gfm-raw_html\
                        --wrap=none\
                        -o {id}.md
                        """,
                    shell=True,
                )
                # TODO script to make markdown short
            # number of characters of markdown
            with open(filename, "r") as f:
                out = f.read()
                id2numchar[id] = len(out)
            print("done!")

    ordered = OrderedDict(sorted(id2numchar.items()))
    with open(OUT_FILENAME, "w") as f:
        json.dump(ordered, f, indent=4)
