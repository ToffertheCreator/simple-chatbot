import asyncio
from typing import List
from loguru import logger
from urllib.parse import urlencode
from playwright.async_api import async_playwright

async def scrape_search(query: str, max_pages: int = 1) -> List[str]:
    """Scrape Bing search results using Playwright and return the top 5 URLs."""
    all_urls = []
    base_url = "https://www.bing.com/search"
    
    async with async_playwright() as playwright:
        # Launch browser with flags to disable WebGL and ignore SSL errors
        browser = await playwright.chromium.launch(
            headless=True, 
            args=[
                "--disable-webgl",                      # Disable WebGL
                "--ignore-certificate-errors",           # Ignore SSL certificate errors
                "--disable-features=MediaDecoding",      # Disable media decoding (FFmpeg errors)
                "--disable-gpu",                         # Disable GPU hardware acceleration
                "--no-sandbox",                          # For running in headless mode in some environments
                "--enable-unsafe-swiftshader"            # Enable software WebGL with lower security
            ]
        )
        page = await browser.new_page()

        for page_num in range(max_pages):
            params = {"q": query, "first": page_num * 10}
            url = f"{base_url}?{urlencode(params)}"
            logger.info(f"Scraping page {page_num + 1} for query: '{query}'")

            await page.goto(url)  # Go to the search results page
            await page.wait_for_selector("li.b_algo")  # Ensure the results are loaded

            # Extract the URLs from the search results
            urls = await page.eval_on_selector_all("li.b_algo h2 a", "elements => elements.map(el => el.href)")

            all_urls.extend(urls)

        await browser.close()

    top_5_urls = all_urls[:5]  # Return top 5 URLs
    logger.success(f"Scraped top 5 URLs: {top_5_urls}")
    return top_5_urls