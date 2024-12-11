import streamlit as st
from scrape import (
    scrape_website,
    split_dom_content,
    clean_body_content,
    extract_body_content,
)
from parse import parse_with_ollama

# Ensure session state includes 'dom_content' to persist between user actions
if "dom_content" not in st.session_state:
    st.session_state.dom_content = ""

# Streamlit app title
st.title("AI Web Scraper")
url = st.text_input("Enter a website URL:")

# Scrape the site when the button is clicked
if st.button("Scrape Site"):
    st.write("Scraping the website...")
    result = scrape_website(url)  # Scrape HTML from the provided URL
    body_content = extract_body_content(result)  # Extract the <body> content
    clean_content = clean_body_content(body_content)  # Clean content (remove scripts, styles)

    if not clean_content:
        st.warning("No DOM content extracted. Check the URL or try another website.")
    else:
        st.session_state.dom_content = clean_content

    # Allow users to view the cleaned content
    with st.expander("View DOM Content"):
        st.text_area("DOM Content", clean_content, height=300)

# If content is available, allow parsing
if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you want to parse?")

    if st.button("Parse Content"):
        if parse_description:
            st.write("Parsing the content")
            dom_chunks = split_dom_content(st.session_state.dom_content)  # Split into smaller chunks
            result = parse_with_ollama(dom_chunks, parse_description)  # AI parses chunks
            st.write(result)
