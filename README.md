# arxivQA_script
pre-process [ArXivQA](https://github.com/taesiri/ArXivQA) using [ar5iv](https://ar5iv.labs.arxiv.org/) and [pandoc](https://pandoc.org/index.html)

Current workflow is : ar5iv --> HTML --> gfm

You can download resulting tarball [here](https://1drv.ms/u/s!AuG8P2rNajS4guE8Fq1yXJNI0wXyTA?e=2jX9gQ) (PW : `BLMPqh6mfLkekAQ3ufVDGj7M`)

## dataset card
### v3
removed link, image, table, reference, appendix and redundant tail
* 4,602 papers
* 44,545,951 tokens for clean papers
* 11,425,548 tokens for Q&A
* 55,971,499 tokens total (clean papers + Q&A)

## Requires...
* docker for `pandoc`

## Default directory shape
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
# execute in order
python3 arxivqa_get_ids.py  # update `paper_ids.json`
python3 convert.py --start_index 0 --end_index 3 --url_to_html
python3 convert.py --start_index 0 --end_index 3 --html_to_md
python3 data_clean.py  # e.g., deduplication
python3 merge_qa.py
```

## Output format
```
* ar5iv
  * (yymm)
    * (arxiv id)
      * assets
      * (arxiv-number).html
      * (arxiv-number).md
    * ...
  * ...
```
