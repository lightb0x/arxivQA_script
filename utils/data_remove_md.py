# remove markdown files in dataset
import os

PATH_PARENT = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
DATA_DIR = os.path.join(PATH_PARENT, "ar5iv")

if __name__ == "__main__":
    yymm = os.listdir(DATA_DIR)
    for ym in yymm:
        papers_of_ym = os.listdir(os.path.join(DATA_DIR, ym))
        for paper in papers_of_ym:
            paper_dir = os.path.join(DATA_DIR, ym, paper)
            paper_id = f"{ym}.{paper}"
            md_dir = os.path.join(paper_dir, f"{paper_id}.md")
            if os.path.exists(md_dir):
                os.remove(md_dir)
