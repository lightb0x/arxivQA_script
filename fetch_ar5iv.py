import os
import subprocess
import json
import argparse

PATH_PARENT = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

parser = argparse.ArgumentParser()
parser.add_argument("--overwrite", action="store_true")
parser.add_argument("--start_index", type=int, default=0)
parser.add_argument("--end_index", type=int, default=10)
parser.add_argument(
    "--path_storage", type=str, default=os.path.join(PATH_PARENT, "ar5iv")
)
args = parser.parse_args()

IN_FILENAME = "paper_ids.json"

if __name__ == "__main__":
    start_index = args.start_index
    end_index = args.end_index

    with open(IN_FILENAME, "r") as f:
        ids = json.load(f)
        end_index = min(end_index, len(ids))
        for i, id in enumerate(ids[start_index:end_index]):
            print(
                f"{start_index + i} / {end_index} : {id}...", end="", flush=True
            )
            dir = os.path.join(args.path_storage, *id.split("."))

            if not os.path.exists(dir):
                os.makedirs(dir)

            filename = os.path.join(dir, f"{id}.html")

            if args.overwrite or not os.path.exists(filename):
                # pandoc
                # arxiv number --> URL --> HTML
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
            print("done!")
