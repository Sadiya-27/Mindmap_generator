# Smart Mind Map Generator from Paragraph

This is a Streamlit app that generates a visual mind map from any input paragraph. It extracts key topics and related points intelligently using NLP (spaCy) and displays an interactive graph using Graphviz.

---

## Features

- Extracts top keywords (nouns and proper nouns) from a paragraph.
- Finds concise key points or whole sentences related to each keyword.
- Dynamically creates a mind map visual with nodes for main topic, keywords, and their points.
- Supports downloading the mind map as a PNG image.
- User-friendly Streamlit interface.

---

## Requirements

- Python 3.8+
- [Streamlit](https://streamlit.io/)
- [spaCy](https://spacy.io/) (`en_core_web_sm` model)
- [Graphviz](https://graphviz.org/) (system package + Python binding)

---

## How It Works: Algorithm and Libraries

### Algorithm Overview

1. **Keyword Extraction**  
   The app processes the input paragraph using **spaCy’s** NLP pipeline to identify and extract the most important keywords.  
   - It selects **nouns and proper nouns** as keywords because these typically represent main topics or entities.  
   - Using simple **frequency counting (term frequency)**, it picks the top N keywords appearing most often.

2. **Key Points Extraction**  
   For each keyword:  
   - The app scans sentences containing that keyword.  
   - It tries to extract **concise noun chunks** (phrases) containing the keyword for clarity and brevity.  
   - If noun chunks aren’t available or meaningful, it falls back to including the **full sentence** containing the keyword to retain context.  
   - It limits the number of points per keyword to avoid clutter.

3. **Mind Map Visualization**  
   The app builds a **graph** using **Graphviz** where:  
   - The central node represents the **main topic**.  
   - Child nodes are the extracted **keywords**.  
   - Further child nodes represent the **key points or phrases** related to each keyword.  
   - The graph is rendered visually for interactive exploration and downloadable as a PNG image.

---

### Libraries Used

- **[spaCy](https://spacy.io/)**  
  A powerful and fast Python NLP library used here for:  
  - Tokenization (splitting text into words and sentences)  
  - Part-of-speech tagging (identifying nouns, verbs, etc.)  
  - Lemmatization (reducing words to base forms)  
  - Sentence segmentation and noun chunk extraction  
  It enables accurate identification of meaningful keywords and relevant phrases.

- **[Graphviz](https://graphviz.org/)**  
  A graph visualization software to create node-edge diagrams.  
  The Python binding (`graphviz` package) allows programmatic creation of mind maps where nodes and edges represent the main topic, keywords, and points.  
  Graphviz produces clear, visually appealing layouts that help in understanding the relationship between concepts.

- **[Streamlit](https://streamlit.io/)**  
  A framework for building interactive web apps quickly in Python.  
  It manages the UI elements like text input, buttons, displaying the generated graph, images, and file downloads with minimal code.

- **Standard Python Libraries**  
  - `collections.Counter` for frequency counting of keywords.  
  - `re` for regular expression matching to find keywords in sentences.  
  - `tempfile` and `os` for safe file handling of graph images.

---

### Summary

The app leverages simple yet effective NLP techniques combined with frequency analysis and phrase extraction to generate meaningful mind maps. It uses open-source libraries to handle language processing, graph visualization, and UI presentation, enabling a smart, interactive tool that helps users visually organize and explore textual information.

---

## Installation

1. Clone the repo:
   ```bash
   git clone https://github.com/Sadiya-27/Mindmap_generator.git
   cd Mindmap_generator
Create and activate a virtual environment:

```bash
python -m venv venv
```
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

Install dependencies:

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```
Make sure Graphviz is installed on your system:

Windows: Download and install from graphviz.org

Ubuntu/Debian: sudo apt-get install graphviz

MacOS: brew install graphviz

Usage
Run the Streamlit app:

```bash
streamlit run app.py
```
Paste or type your paragraph.

Click Generate Mind Map.

View the generated mind map graph.

Optionally download the mind map as a PNG.

Notes
The app intelligently extracts keywords and related points, showing whole sentences if needed for clarity.

The venv folder is ignored in this repo; dependencies are managed via requirements.txt.

