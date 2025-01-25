import asyncio
from typing import List
from loguru import logger  # Used for logging information
from urllib.parse import urlencode  # For URL parameter encoding
from playwright.async_api import async_playwright  # For web scraping using Playwright

# Function to scrape Bing search results and return the top 5 URLs
async def scrape_search(query: str, max_pages: int = 1) -> List[str]:
    """Scrape Bing search results using Playwright and return the top 5 URLs."""
    all_urls = []  # List to store all scraped URLs
    base_url = "https://www.bing.com/search"  # Bing search base URL
    
    async with async_playwright() as playwright:
        # Launch the browser in headless mode with specific flags for scraping
        browser = await playwright.chromium.launch(
            headless=True,  # Run in headless mode (no UI)
            args=[
                "--disable-webgl",                      # Disable WebGL to avoid potential errors
                "--ignore-certificate-errors",           # Ignore SSL certificate errors
                "--disable-features=MediaDecoding",      # Disable media decoding (e.g., FFmpeg errors)
                "--disable-gpu",                         # Disable GPU hardware acceleration
                "--no-sandbox",                          # For running in headless mode in some environments
                "--enable-unsafe-swiftshader"            # Enable software WebGL with lower security
            ]
        )
        page = await browser.new_page()  # Create a new page (browser tab)

        # Loop through pages of search results based on `max_pages` input
        for page_num in range(max_pages):
            # Encode the search query parameters for the URL
            params = {"q": query, "first": page_num * 10}  # 'first' determines the starting result
            url = f"{base_url}?{urlencode(params)}"  # Build the full URL for the search query
            logger.info(f"Scraping page {page_num + 1} for query: '{query}'")  # Log the scraping process

            await page.goto(url)  # Navigate to the search results page
            await page.wait_for_selector("li.b_algo")  # Wait for the results to load by checking for a selector

            # Extract URLs from the search results (specifically from <a> tags within <h2> tags)
            urls = await page.eval_on_selector_all("li.b_algo h2 a", "elements => elements.map(el => el.href)")

            all_urls.extend(urls)  # Add the scraped URLs to the `all_urls` list

        await browser.close()  # Close the browser after scraping is done

    top_5_urls = all_urls[:5]  # Return only the top 5 URLs from the list
    logger.success(f"Scraped top 5 URLs: {top_5_urls}")  # Log the top 5 URLs found
    return top_5_urls  # Return the top 5 URLs as a list
