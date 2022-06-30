##parsecc Notes

``` read list of firm per .pdf file ```

- function parseHtmlXlsToDf(filename)

``` get page from the .pdf file ```

- function getPage(doc::Vector,page_n)
- function getPage(doc,page_n)

``` get contents of the .pdf file```

- function getPageContents(doc)

``` get from the content the first page number of the CCall firm by name or by Rpt number```
``` we use report number, since the firm can have several reports for a .pdf file ```

- function getFirmPageNumber(content,report_n::Int)

``` 1st type of CCall```

- function cutHeader(page,lastpage=false)
- function cutBottom(page)
- function cutDisclaimer(page)
- function IsTwoColumns(page)
- function getFirmCC_t1(doc,page_s,page_e)

``` end 1st type ```
``` 2nd type ```

- function fistPage_t2(page)
- function cutHeaderFooter_t2_1(page)
- function cutHeaderFooter_t2_2(page)

```given line, looking for a second column start ```

- function findColumn(line)
- function twoColumsToText(page,disclaimer=false)
- function getFirmCC_t2(doc,page_s,page_e) #type 2, Analyst==FDFN.COM
- function isFDFN(doc,page_n)

``` Parse file```

- function parseCalls(filename)

```parse all file from the current  ```

- function main()
getpage: get page from the document

``` Other comments ```

- Areas for improvement for the .jl script:
  - command line arguments (suffix)
  - turn it into python?