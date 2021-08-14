# China-Crawler

This is a web crawler and HTML parser that scrapes intellectual property infringement case data from the Shenzhen Customs Administration in China. The agency tracks information about detained export shipments with goods purported to have violated IP laws. It crawls landing pages with lists of case hyperlinks, downloads the linked pages locally, and parses top-level details about each case using regular expressions, which are written into a CSV file.

The output CSV contains the following fields about each IP infringement case:

* Name, address, Unified Social Credit Code, and legal representative of the offending company
* Infringed brand name(s)
* Local path to each saved HTML file
* Title and publication date of the notice

This program uses Firefox, geckodriver, and the Selenium and bs4 Python libraries.

You can download ZIP files of just the CSV & XLSX parser output as of Aug 2021 [here,](https://github.com/HernandezPatrick/China-Crawler/files/6987180/Parser_Output.zip)
or all crawl artifacts, including HTMLs, [here.](https://github.com/HernandezPatrick/China-Crawler/files/6987181/Aug_2021_Crawl_Artifacts.zip)

# Usage examples

Run the crawler and parser for all available case pages:

python chinaCrawler.py _yourFilepath_

Run the crawler from a specific starting page, then run the parser (useful for recrawling the site):

python chinaCrawler.py _yourFilepath_ 105

Run the parser by itself on any collected HTMLs:

python chinaCrawler.py _yourFilepath_ parse
