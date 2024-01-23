import os
import asyncio
import glob
import json
from playwright.async_api import async_playwright
from fpdf import FPDF
from tedfulk_kb_pycrawler.models import WebPage, Knowledgebase, Config, NoSitemapError


async def crawl_websites(config: Config):
    """
    Crawl the specified websites and generate a knowledgebase.

    Args:
        config (Config): Configuration object containing the URLs and max pages to crawl.

    Raises:
        NoSitemapError: If no sitemap.xml is found for a given URL.

    Returns:
        Knowledgebase: The generated knowledgebase.
    """
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        page = await browser.new_page()
        knowledgebase = Knowledgebase(kb=[])
        for i, url in enumerate(config.urls):
            sitemap_url = url + "/sitemap.xml"
            response = await page.goto(sitemap_url)
            if response.status == 404:
                raise NoSitemapError(f"No sitemap.xml found for {url}")
            urls = await page.evaluate(
                '() => Array.from(document.querySelectorAll("loc")).map(e => e.textContent)'
            )
            for i, url in enumerate(urls):
                if (
                    config.max_pages_to_crawl is not None
                    and i >= config.max_pages_to_crawl
                ):
                    break
                await page.goto(url)
                body_content = await page.evaluate("() => document.body.textContent")
                web_page = WebPage(url=url, content=body_content)
                web_page.content = (
                    web_page.content.replace("\n", " ")
                    .replace("\t", " ")
                    .replace("\u2014", " ")
                    .replace("\u00b6", " ")
                    .replace("\u00a0", " ")
                    .replace("\u00ae", " ")
                    .replace("\u00b7", " ")
                    .replace("\u2026", " ")
                    .replace("\u2019", " ")
                    .replace("   ", " ")
                    .replace("    ", " ")
                    .replace("     ", " ")
                    .replace("       ", " ")
                )
                knowledgebase.kb.append(web_page)
        await browser.close()
        return knowledgebase


async def write_to_file(knowledgebase: Knowledgebase, config: Config):
    """
    Write the knowledgebase to the specified file.

    Args:
        knowledgebase (Knowledgebase): The knowledgebase to write.
        config (Config): Configuration object containing the output file name and type.

    Returns:
        None
    """
    for file_name in config.output_file_name:
        if not os.path.exists(f"knowledge/{file_name}"):
            os.makedirs(f"knowledge/{file_name}")

        for file_type in config.output_file_type:
            output_filename = get_output_filename(file_name, file_type)

            if file_type == "json":
                if not os.path.exists(f"knowledge/{file_name}/{output_filename}"):
                    with open(f"knowledge/{file_name}/{output_filename}", "w") as f:
                        json.dump(knowledgebase.model_dump(), f, indent=4)
            elif file_type == "txt":
                if not os.path.exists(f"knowledge/{file_name}/{output_filename}"):
                    with open(f"knowledge/{file_name}/{output_filename}", "w") as f:
                        for web_page in knowledgebase.kb:
                            f.write(web_page.content)
            elif file_type == "pdf":
                if not os.path.exists(f"knowledge/{file_name}/{output_filename}"):
                    string_to_pdf(
                        knowledgebase, f"knowledge/{file_name}/{output_filename}"
                    )

        print(f"Knowledgebase written to {file_name}")


def get_output_filename(file_name: str, file_type: str):
    _files = glob.glob(f"knowledge/{file_name}/{file_name}*.{file_type}")
    count = len(_files) + 1
    output_filename = f"{file_name}-{count}.{file_type}"
    return output_filename


def string_to_pdf(knowledgebase: Knowledgebase, file_name):
    """
    The function `string_to_pdf` converts the content of webpages in a knowledgebase to a PDF file,
    handling encoding issues.

    Args:
        knowledgebase (Knowledgebase): The `knowledgebase` parameter is an object of the `Knowledgebase`
    class. It likely contains a collection of webpages with their URLs and content.
        file_name: The `file_name` parameter is a string that represents the name of the PDF file that
    will be generated. It should include the file extension ".pdf". For example, if you want the PDF
    file to be named "knowledgebase.pdf", you would pass the string "knowledgebase.pdf" as the
    """
    pdf = FPDF()

    for webpage in knowledgebase.kb:
        try:
            # Try to convert the content string to ISO-8859-1
            content = webpage.content.encode("ISO-8859-1", "replace").decode(
                "ISO-8859-1"
            )
            pdf.set_font("Arial", size=6)
        except UnicodeEncodeError:
            # If conversion fails, use DejaVu font that supports UTF-8
            content = webpage.content
            pdf.set_font("DejaVu", "", 6)

        pdf.add_page()
        pdf.multi_cell(0, 6, f"URL: {webpage.url}\n{content}")

    pdf.output(file_name)


async def scrape_it(config: Config):
    try:
        knowledgebase = await crawl_websites(config)
        await write_to_file(knowledgebase, config)
    except NoSitemapError as e:
        print(str(e))
