# China-Crawler

This is a web crawler and HTML parser that scrapes intellectual property infringement case data from the Shenzhen Customs Administration in China. It crawls landing pages with lists of case hyperlinks, downloads the linked pages locally, and parses top-level details about each case using regular expressions, which are written into a CSV file.

The output CSV contains the following fields about each IP infringement case:

* Name, address, Unified Social Credit Code, and legal representative of the offending company
* Infringed brand name(s)
* Local path to each saved HTML file
* Title and publication date of the notice

This program uses Firefox, geckodriver, and the Selenium and bs4 Python libraries.

[See here for an example of the output from Aug 2021.](https://github.com/HernandezPatrick/China-Crawler/files/6978722/Aug_2021_Crawl_Artifacts.zip)
