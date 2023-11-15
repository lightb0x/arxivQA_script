import os
import subprocess
import json
import argparse
from collections import OrderedDict
from transformers import PreTrainedTokenizerFast

PATH_PARENT = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

parser = argparse.ArgumentParser()
parser.add_argument("--start_index", type=int, default=0)
parser.add_argument("--end_index", type=int, default=10)
parser.add_argument(
    "--path_storage", type=str, default=os.path.join(PATH_PARENT, "ar5iv")
)
args = parser.parse_args()

IN_FILENAME = "paper_ids.json"
OUT_FILENAME = "paper_id_num_token.json"

if __name__ == "__main__":
    start_index = args.start_index
    end_index = args.end_index

    id_to_num_tok = {}
    if os.path.exists(OUT_FILENAME):
        with open(OUT_FILENAME, "r") as f:
            id_to_num_tok = json.load(f)

    with open(IN_FILENAME, "r") as f:
        ids = json.load(f)
        for i, id in enumerate(ids[start_index:end_index]):
            print(
                f"{start_index + i} / {end_index} : {id}...", end="", flush=True
            )
            dir = os.path.join(args.path_storage, *id.split("."))

            if not os.path.exists(dir):
                os.makedirs(dir)

            filename = os.path.join(dir, f"{id}.md")

            if not os.path.exists(filename):
                # pandoc
                # arxiv HTML --> markdown
                subprocess.run(
                    f"""docker run --rm \
                        --volume "{dir}:/data" \
                        --volume "{dir}/assets:/assets" \
                        --volume "{os.getcwd()}:/scripts" \
                        --user $(id -u):$(id -g) \
                        pandoc/panflute\
                        -f html\
                        {id}.html\
                        -t gfm-raw_html\
                        --wrap=none\
                        --filter=/scripts/markdown_filter.py\
                        -o {id}.md
                        """,
                    shell=True,
                )
            # number of tokens of resulting markdown
            with open(filename, "r") as f:
                converted = f.read()
                tknzr = PreTrainedTokenizerFast(tokenizer_file="phi-1_5.json")
                id_to_num_tok[id] = len(tknzr.tokenize(converted))
            print("done!")

    ordered = OrderedDict(sorted(id_to_num_tok.items()))
    with open(OUT_FILENAME, "w") as f:
        json.dump(ordered, f, indent=4)
