# check if there is paper with more than 3 entries
# 2 entries = assets + html
# 3 entries = assets + html + markdown
import os

PATH_PARENT = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
DATA_DIR = os.path.join(PATH_PARENT, "ar5iv")

if __name__ == "__main__":
    yymm = os.listdir(DATA_DIR)
    for ym in yymm:
        papers_of_ym = os.listdir(os.path.join(DATA_DIR, ym))
        for paper in papers_of_ym:
            paper_dir = os.path.join(DATA_DIR, ym, paper)
            if len(os.listdir(paper_dir)) > 3:
                print(f"{ym}.{paper}")
