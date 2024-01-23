# Python Web Scraper

This script utilizes the **Playwright library** for scraping websites and generating a knowledgebase. It is capable of outputting the scraped data in multiple formats, including JSON, plain text, and PDF.

## Main Functions

### `scrape_it(config: Config)`

#### Parameters

- `config`: An object containing URLs to scrape, output file names, file types, and a limit on pages to crawl.

#### Workflow

1. **Launch Chromium Browser**: Uses Playwright to start a new browser instance.
2. **URL Iteration**: For each URL in the `Config` object:
   - **Sitemap Processing**:
     - Navigate to `sitemap.xml`.
     - Raise `NoSitemapError` if not found, else extract URLs.
   - **Page Processing**: For each URL in the sitemap:
     - Stop if `max_pages_to_crawl` is reached.
     - Navigate to the URL and extract the page content.
     - Create a `WebPage` object with URL and content.
     - Clean content and add to `Knowledgebase` object.
3. **Output Generation**:
   - Calls `write_to_file(knowledgebase: Knowledgebase, config: Config)` to generate outputs.
   - Supports multiple output formats as specified in `config` (JSON, TXT, PDF).

### `write_to_file(knowledgebase: Knowledgebase, config: Config)`

#### Purpose

Writes the scraped data from `Knowledgebase` to files in the specified formats.

#### Functionality

- **Directory Creation**: Ensures the directory for storing files exists.
- **File Generation**:
  - **JSON Output**: Stores the `Knowledgebase` object in a JSON file.
  - **Text Output**: Creates a text file with all the page contents.
  - **PDF Output**: Generates a PDF file with the content of each webpage.

#### Unique Filenames

- Uses `get_output_filename(file_name: str, file_type: str)` to ensure unique file names for each output file.

### `string_to_pdf(knowledgebase: Knowledgebase, file_name)`

#### Purpose

Converts the content of webpages in a `Knowledgebase` to a PDF file.

#### Functionality

- Handles UTF-8 encoding and falls back to DejaVu font if necessary.
- Generates a PDF with each page's URL and content.

## Error Handling

- The script raises a `NoSitemapError` if a sitemap.xml file is not found for a given URL.
- Errors and statuses are printed to the console for debugging and monitoring.

## Requirements

- Playwright for Python
- FPDF library for PDF generation
- Pydantic for data model validation

## Usage

```bash
poetry add tedfulk-kb-pycrawler
```

```bash
playwright install
```

```python
import asyncio
from tedfulk_kb_pycrawler import scrape_it, Config


config = Config(
    urls=[
        "https://jxnl.github.io/instructor/",
    ],
    output_file_name=["instructor"],
    output_file_type=["pdf"],
    max_pages_to_crawl=100,
)
asyncio.run(scrape_it(config))

```

Activate your virtual environment:

```python
poetry shell
```

Run the script:

```python
python main.py
```
