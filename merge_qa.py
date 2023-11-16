import os
import json
import re
from transformers import PreTrainedTokenizerFast

PATH_PARENT = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
DATA_DIR = os.path.join(PATH_PARENT, "ar5iv")
QA_DIR = os.path.join(PATH_PARENT, "ArXivQA", "papers")

CLEAN = "clean_dset.json"  # dedup id --> actual id
NUM_TOKENS = "paper_id_num_token.json"  # actual id --> num tokens


# QA markdown to json
def parse_qa(filename, tokenizer):
    paper = {}
    qas = []
    num_qa_tok = 0
    with open(filename, "r") as f_qa:
        qa = {}
        buffer = []
        for line in f_qa.readlines():
            if re.search(r"^#\s", line):
                sep_index = line.index("](https://")
                paper["title"] = line[3:sep_index].strip()
                paper["link"] = line[sep_index + 2 : -2].strip()
            elif re.search(r"^##\s", line):
                if "question" in qa:
                    qa["answer"] = "".join(buffer).strip()
                    num_qa_tok += len(tokenizer.tokenize(qa["answer"]))
                    qas.append(qa)
                    qa = {}
                qa["question"] = line[2:].strip()
                num_qa_tok += len(tokenizer.tokenize(qa["question"]))
                buffer = []
            else:
                buffer.append(line)
    paper["Q&A"] = qas

    return paper, num_qa_tok


if __name__ == "__main__":
    num_tokens = {}
    with open(NUM_TOKENS, "r") as f:
        num_tokens = json.load(f)
    clean_link = {}
    with open(CLEAN, "r") as f:
        clean_link = json.load(f)

    tokenizer = PreTrainedTokenizerFast(tokenizer_file="phi-1_5.json")
    total_num_tok = 0
    total_num_qa_tok = 0
    for id, actual in clean_link.items():
        print(id)
        ym, num = actual.split(".")
        paper_path = os.path.join(DATA_DIR, ym, num)

        qa_file = os.path.join(QA_DIR, f"{actual}.md")
        paper_qas, qa_num_tok = parse_qa(qa_file, tokenizer)
        total_num_qa_tok += qa_num_tok

        with open(os.path.join(paper_path, f"{actual}.json"), "w") as f_qa:
            json.dump(paper_qas, f_qa, indent=4)
        total_num_tok += num_tokens[actual]

    print(f"total {len(clean_link)} papers")
    print(f"total {total_num_qa_tok} tokens for Q&A")
    print(f"total {total_num_tok + total_num_qa_tok} tokens for paper + Q&A")
