import os
import subprocess
import json
import argparse
from collections import OrderedDict
from transformers import PreTrainedTokenizerFast
from utils.locker import Locker

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

    tokenizer = PreTrainedTokenizerFast(tokenizer_file="phi-1_5.json")
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

            filename = os.path.join(dir, f"{id}.md")

            if not os.path.exists(filename):
                # pandoc
                # arxiv HTML --> markdown
                command = [
                    "docker run --rm",
                    f'--volume "{dir}:/data"',
                    f'--volume "{os.path.join(dir, "assets")}:/assets"',
                    f'--volume "{os.path.join(os.getcwd(), "filters")}:/filters"',
                    "--user $(id -u):$(id -g)",
                    "pandoc/panflute",
                    "-f html",
                    f"{id}.html",
                    "-t gfm-raw_html",
                    "--wrap=none",
                    "--filter=/filters/mk2.py",
                    f"-o {id}.md",
                ]
                subprocess.run(
                    " ".join(command),
                    shell=True,
                )
            # number of tokens of resulting markdown
            if os.path.exists(filename):
                with open(filename, "r") as f:
                    converted = f.read()
                    id_to_num_tok[id] = len(tokenizer.tokenize(converted))
            print("done!")

    with Locker():
        loaded = {}
        if os.path.exists(OUT_FILENAME):
            with open(OUT_FILENAME, "r") as f:
                loaded = json.load(f)

        def merge_two_dicts(orig, update):
            merged = orig.copy()
            merged.update(update)
            return merged

        id_to_num_tok = merge_two_dicts(loaded, id_to_num_tok)
        ordered = OrderedDict(sorted(id_to_num_tok.items()))
        with open(OUT_FILENAME, "w") as f:
            json.dump(ordered, f, indent=4)
