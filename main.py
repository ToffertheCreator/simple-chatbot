import asyncio
import gradio as gr
from bing_scraper import scrape_search
from content_scraper import setup_browser, scrape_content
from summarizer import summarize_text
from weather_query import fetch_weather

# Async scraper function'
async def scraper(query: str):
    """Scrape and summarize web content based on a user query."""
    top_5_urls = await scrape_search(query, max_pages=1)

    if not top_5_urls:
        return {"summary": "No links found", "sources": []}

    # Scrape content from each link
    browser = setup_browser()
    combined_content = ""
    for idx, url in enumerate(top_5_urls, start=1):
        content = scrape_content(url, browser)
        combined_content += content + "\n\n"
        await asyncio.sleep(5)  # Add delay between requests

    browser.quit()

    # Summarize the combined content
    summary = summarize_text(combined_content, sentence_count=25)
    return {"summary": summary, "sources": top_5_urls}

# Weather query function
async def get_weather_info(location: str):
    """Fetch weather information asynchronously."""
    return await fetch_weather(location)

# Gradio chatbot logic
async def chatbot(input_text, chat_history):
    """Handle chatbot responses based on user input."""
    chat_history.append({"role": "user", "content": input_text})  # Add user input to chat history

    if input_text == "1":
        # Weather query
        response = "Please provide a location for the weather query."
        chat_history.append({"role": "assistant", "content": response})
        return "", chat_history

    elif input_text == "2":
        # General query
        response = "Please provide a query you'd like to search for."
        chat_history.append({"role": "assistant", "content": response})
        return "", chat_history

    elif chat_history[-2]["content"] == "Please provide a location for the weather query.":
        # Handle weather input
        try:
            weather_report = await get_weather_info(input_text)
            response = f"Weather information:\n{weather_report}"
        except Exception as e:
            response = f"Failed to fetch weather information. Error: {e}"
        chat_history.append({"role": "assistant", "content": response})
        return "", chat_history

    elif chat_history[-2]["content"] == "Please provide a query you'd like to search for.":
        # Handle general query input
        try:
            result = await scraper(input_text)
            response = f"{result['summary']}\n\nSources: {result['sources']}"
        except Exception as e:
            response = f"Failed to fetch results for your query. Error: {e}"
        chat_history.append({"role": "assistant", "content": response})
        return "", chat_history

    else:
        # Default response
        response = "I didn't quite understand. Please choose a valid option:\n(1) Weather Query\n(2) General Query"
        chat_history.append({"role": "assistant", "content": response})
        return "", chat_history

# Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown("## Simple Chatbot")
    chatbot_ui = gr.Chatbot(label="Chat History", type="messages")
    user_input = gr.Textbox(label="Type your message here...", placeholder="Enter '1' for weather or '2' for general query.")
    clear_button = gr.Button("Clear Chat")

    chat_history = gr.State([])  # Store chat history as a list of dictionaries

    # Update chatbot logic
    user_input.submit(chatbot, inputs=[user_input, chat_history], outputs=[user_input, chatbot_ui])
    clear_button.click(lambda: ([], []), inputs=[], outputs=[chat_history, chatbot_ui])

# Launch the Gradio app
if __name__ == "__main__":
    demo.launch()
