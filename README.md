# arxivQA_script
pre-process [ArXivQA](https://github.com/taesiri/ArXivQA) using [ar5iv](https://ar5iv.labs.arxiv.org/) and [pandoc](https://pandoc.org/index.html)

Current workflow is : ar5iv --> HTML --> gfm

You can download resulting tarball [here](https://1drv.ms/f/s!AuG8P2rNajS4uWSlSNtoIZNyHG4E?e=b9Ua10) (PW : `BLMPqh6mfLkekAQ3ufVDGj7M`)

md5 hash values
* `ar5iv_v4_textonly.tar.gz` : `5f01788d7e9e4d33b29279fa00574dac`
* `arxivQA_v4.json` : `e267227c3891eddea4c670f4fbf2102d`
* `arxivQA_v4_tex.json` : `1d5ff485b9603bc32d5b5f36a0a0bb3d`

## dataset card
### v4
merged article + Q&A to `json` (was only Q&A)

### v3
removed link, image, table, reference, appendix and redundant tail
* 4,602 papers
* 44,545,951 tokens for clean papers
* 11,425,548 tokens for Q&A
* 55,971,499 tokens total (clean papers + Q&A)

## build on your own
requires...
* docker for `pandoc`

### Default directory shape
```
* ArXivQA
* ar5iv
* arxivQA_script
  * convert.py
  * data_clean.py
  * ...
```

### how to run
```bash
# execute in order
python3 arxivqa_get_ids.py  # update `paper_ids.json`
python3 convert.py --start_index 0 --end_index 3 --url_to_html
python3 convert.py --start_index 0 --end_index 3 --html_to_md
python3 data_clean.py  # e.g., deduplication
python3 merge_qa.py  # add Q&A from ArXivQA, only for clean dataset
python3 aggregate.py  # aggregate to one large `json` file
```

## Output format
```
* ar5iv
  * (yymm)
    * (id)
      * assets
      * (yymm.id).html  # original
      * (yymm.id).md    # converted markdown
      * (yymm.id).json  # Q&A converted from ArXivQA (only for clean dataset)
    * ...
  * ...
```
