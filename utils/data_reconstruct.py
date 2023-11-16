# change ar5iv dataset structure
# from : ar5iv/yymm.iiiii/...
# to   : ar5iv/yymm/iiiii/...
import os

PATH_PARENT = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
DATA_DIR = os.path.join(PATH_PARENT, "ar5iv")

if __name__ == "__main__":
    for id in os.listdir(DATA_DIR):
        assert len(id.split(".")) == 2
        yymm, num = id.split(".")
        if not os.path.exists(os.path.join(DATA_DIR, yymm)):
            print(yymm)
            os.makedirs(os.path.join(DATA_DIR, yymm))
        os.rename(os.path.join(DATA_DIR, id), os.path.join(DATA_DIR, yymm, num))
