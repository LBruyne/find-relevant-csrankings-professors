# Find-Your-Relevant-CSRankings-Professor

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Description

This project aims to help CS students seeking PhD professors, by uncovering the relevance between their background and the professors at various universities. Students can discover professors and universities by searching for relevant fields on [CSRankings](https://csrankings.org). They can then filter for potential supervisors with related backgrounds by searching for interested keywords on academic websites (e.g., `Google Scholar`). The script provided here automates these steps.

The script offers the following functionalities:

- Filter and record the top-ranked schools and professors in your field, such as AI, HCI, and Database, by leveraging automated scraping of `CSRankings`.
- From the results of the previous step, search through the academic publications of each professor to identify the presence of your specified keywords of interest (e.g., LLM, Blockchain, spatial), and present their recent relevant works. This is achieved through automated retrieval from `Google Scholar`.
  
PRs are welcome!

## How to run

This project is powered by `selenium`, as websites like `Google Scholar` are challenging to scrape using libraries like `requests`. It can be run on a PC efficiently.

### Install

Since this project is driven by `selenium`, you need to first find the version of the `Chrome` browser on your machine and install the corresponding `chromedriver`.

Skip these if you are familiar with `selenium`.

- Find your Chrome version in your browser (in `About` of its tabbar).
- Download `chromedriver` with the same version [here](https://chromedriver.chromium.org/downloads).
- Make sure chromedriver is in your PATH (in MacOS you can move it into `/usr/local/bin`).

Install the required Python packages.

```
# add -i to switch to a mirror
pip install selenium BeautifulSoup4 prettytable
```

### Usage

First, execute `./csranking_top_professors.py` to retrieve the ranked universities and professors based on your interest areas. This script provides details about the professors, including their homepages and Google Scholar pages.

An example input:

```
python3 csranking_top_professors.py --fields sec,ai
```

Next, execute `./relevant_professors.py` to obtain the correlation between your selected keywords and the recent publications of these professors. This script allows filtering by institution and presents the latest and most cited works related to your keywords.

An example input:

```
python3 relevant_professors.py --filename examples/2020-2024-sec-ai.csv --keywords "LLM,privacy"
```

Example results can be found in the `examples` folder.

## License

This project is licensed under the [MIT License](LICENSE). See the LICENSE file for more details.
