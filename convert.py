import os
import subprocess
import json
import argparse
from collections import OrderedDict
from transformers import PreTrainedTokenizerFast
from utils.locker import Locker

PATH_PARENT = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

parser = argparse.ArgumentParser()
parser.add_argument("--overwrite", action="store_true")
parser.add_argument("--start_index", type=int, default=0)
parser.add_argument("--end_index", type=int, default=10)
parser.add_argument(
    "--path_storage", type=str, default=os.path.join(PATH_PARENT, "ar5iv")
)
parser.add_argument("--url_to_html", action="store_true")
parser.add_argument("--html_to_md", action="store_true")
args = parser.parse_args()

assert (
    args.url_to_html or args.html_to_md
), "both `--url_to_html` and `--html_to_md` conversions not set, aborting..."

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

            filename_html = os.path.join(f"{id}.html")
            filename_md = os.path.join(f"{id}.md")

            dir_html = os.path.join(dir, filename_html)
            dir_md = os.path.join(dir, filename_md)

            if args.url_to_html and (
                args.overwrite or not os.path.exists(dir_html)
            ):
                # pandoc
                # arxiv number --> URL --> HTML
                command = [
                    "docker run --rm",
                    f'--volume "{dir}:/data"',
                    f'--volume "{os.path.join(dir, "assets")}:/assets"',
                    "--user $(id -u):$(id -g)",
                    "pandoc/latex",
                    f"-s -r html https://ar5iv.org/abs/{id}",
                    "--extract-media=assets",
                    "--mathml",
                    "-t html",
                    f"-o {filename_html}",
                ]
                subprocess.run(" ".join(command), shell=True)

            if args.html_to_md and (
                args.overwrite or not os.path.exists(dir_md)
            ):
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
                    f"{filename_html}",
                    "-t gfm-raw_html",
                    "--wrap=none",
                    "--filter=/filters/mk2.py",
                    f"-o {filename_md}",
                ]
                subprocess.run(" ".join(command), shell=True)

                # number of tokens of resulting markdown
                if os.path.exists(dir_md):
                    with open(dir_md, "r") as f:
                        converted = f.read()
                        id_to_num_tok[id] = len(tokenizer.tokenize(converted))
                else:
                    id_to_num_tok[id] = 0
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
