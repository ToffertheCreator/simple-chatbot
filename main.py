import asyncio
import gradio as gr
from bing_scraper import scrape_search
from content_scraper import setup_browser, scrape_content
from summarizer import summarize_text
from weather_query import fetch_weather

# Async scraper function to search and summarize content based on user query
async def scraper(query: str):
    """Scrape and summarize web content based on a user query."""
    # Perform a search to get top 5 URLs
    top_5_urls = await scrape_search(query, max_pages=1)

    # If no URLs are found, return a default response
    if not top_5_urls:
        return {"summary": "No links found", "sources": []}

    # Initialize the browser for scraping
    browser = setup_browser()
    combined_content = ""  # Variable to store combined content from all scraped pages

    # Scrape content from each of the top 5 URLs
    for idx, url in enumerate(top_5_urls, start=1):
        content = scrape_content(url, browser)  # Get content from the URL
        combined_content += content + "\n\n"  # Append the content to combined_content
        await asyncio.sleep(5)  # Add a 5-second delay between requests to avoid overloading the server

    # Quit the browser after scraping
    browser.quit()

    # Summarize the combined content into a concise summary
    summary = summarize_text(combined_content, sentence_count=25)
    return {"summary": summary, "sources": top_5_urls}  # Return the summary and sources

# Fetch weather information for a given location asynchronously
async def get_weather_info(location: str):
    """Fetch weather information asynchronously."""
    return await fetch_weather(location)  # Use the fetch_weather function to get weather data

# Gradio chatbot logic to handle user input and responses
async def chatbot(input_text, chat_history):
    """Handle chatbot responses based on user input."""
    chat_history.append({"role": "user", "content": input_text})  # Add user input to chat history

    # Check if the user wants a weather query
    if input_text == "1":
        response = "Please provide a location for the weather query."
        chat_history.append({"role": "assistant", "content": response})  # Respond asking for location
        return "", chat_history  # Return empty string and updated chat history

    # Check if the user wants a general web query
    elif input_text == "2":
        response = "Please provide a query you'd like to search for."
        chat_history.append({"role": "assistant", "content": response})  # Ask for a specific query
        return "", chat_history

    # Handle the location input for the weather query
    elif chat_history[-2]["content"] == "Please provide a location for the weather query.":
        try:
            weather_report = await get_weather_info(input_text)  # Fetch the weather info
            response = f"Weather information:\n{weather_report}"
        except Exception as e:
            response = f"Failed to fetch weather information. Error: {e}"
        chat_history.append({"role": "assistant", "content": response})  # Add the weather response
        return "", chat_history

    # Handle the query input for a general search
    elif chat_history[-2]["content"] == "Please provide a query you'd like to search for.":
        try:
            result = await scraper(input_text)  # Scrape and summarize content based on the input query
            response = f"{result['summary']}\n\nSources: {result['sources']}"  # Return the summary and sources
        except Exception as e:
            response = f"Failed to fetch results for your query. Error: {e}"
        chat_history.append({"role": "assistant", "content": response})  # Add the result response
        return "", chat_history

    else:
        # Default response when input is not understood
        response = "I didn't quite understand. Please choose a valid option:\n(1) Weather Query\n(2) General Query"
        chat_history.append({"role": "assistant", "content": response})  # Provide guidance
        return "", chat_history

# Gradio Interface to build the chatbot UI
with gr.Blocks() as demo:
    gr.Markdown("## Simple Chatbot")  # Add a title to the interface
    chatbot_ui = gr.Chatbot(label="Chat History", type="messages")  # Create a chatbot display component
    user_input = gr.Textbox(label="Type your message here...", placeholder="Enter '1' for weather or '2' for general query.")  # Create a textbox for user input
    clear_button = gr.Button("Clear Chat")  # Button to clear the chat history

    chat_history = gr.State([])  # State to store chat history as a list of dictionaries

    # Define behavior for user input and clear button
    user_input.submit(chatbot, inputs=[user_input, chat_history], outputs=[user_input, chatbot_ui])  # Handle user input submission
    clear_button.click(lambda: ([], []), inputs=[], outputs=[chat_history, chatbot_ui])  # Clear the chat history when the button is clicked

# Launch the Gradio app
if __name__ == "__main__":
    demo.launch()  # Launch the Gradio app to interact with the chatbot
