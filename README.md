# arxivQA_script
pre-process [ArXivQA](https://github.com/taesiri/ArXivQA) using [ar5iv](https://ar5iv.labs.arxiv.org/) and [pandoc](https://pandoc.org/index.html)

Current workflow is : ar5iv --> HTML --> gfm

Requires...
* docker for `pandoc`

Default directory shape
```
* ArXivQA
* ar5iv
* arxivQA_script
  * arxivqa_get_ids.py
  * fetch_ar5iv.py
  * ...
```

## how to use
```bash
python3 arxivqa_get_ids.py  # update `paper_ids.json`
python3 fetch_ar5iv.py --start_index 0 --end_index 3  # update `ar5iv` and `paper_id_numchar.json`
```

Output format
```
* ar5iv
  * (arxiv-number)
    * assets
    * (arxiv-number).html
    * (arxiv-number).md
  * ...
```
