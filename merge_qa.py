import os
import json
import re

PATH_PARENT = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
DATA_DIR = os.path.join(PATH_PARENT, "ar5iv")
QA_DIR = os.path.join(PATH_PARENT, "ArXivQA", "papers")

CLEAN = "clean_dset.json"


# QA markdown to json
def parse_qa(filename):
    paper = {}
    qas = []
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
                    qas.append(qa)
                    qa = {}
                qa["question"] = line[2:].strip()
                buffer = []
            else:
                buffer.append(line)
    paper["Q&A"] = qas

    return paper


if __name__ == "__main__":
    clean_link = {}
    with open(CLEAN, "r") as f:
        ids = json.load(f)

    for id, actual in ids:
        ym, num = actual.split(".")
        paper_path = os.path.join(DATA_DIR, ym, num)
        qa_file = os.path.join(QA_DIR, f"{actual}.md")

        paper_qas = parse_qa(qa_file)

        with open(os.path.join(paper_path, f"{actual}.json"), "w") as f_qa:
            json.dump(paper_qas, f_qa, indent=4)
