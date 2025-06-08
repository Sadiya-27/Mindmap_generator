import streamlit as st
import spacy
from collections import defaultdict, Counter
import graphviz
import tempfile
import os
import re

# Load spaCy NLP model
nlp = spacy.load("en_core_web_sm")

# --- Extract keywords (noun-based) ---
def extract_keywords(text, num_keywords=5):
    doc = nlp(text.lower())
    nouns = [token.lemma_ for token in doc if token.is_alpha and not token.is_stop and token.pos_ in {"NOUN", "PROPN"}]
    freq = Counter(nouns)
    return [word for word, _ in freq.most_common(num_keywords)]

# --- Extract key points: noun chunks first, full sentences as fallback ---
def extract_key_points(text, keywords, max_points_per_kw=5):
    doc = nlp(text)
    sentence_map = defaultdict(list)
    used_texts = set()

    for sent in doc.sents:
        sent_text = sent.text.strip()
        sent_lower = sent_text.lower()

        for kw in keywords:
            if kw in sent_lower:
                # Try to use unique noun chunks
                chunks_added = 0
                for chunk in sent.noun_chunks:
                    chunk_text = chunk.text.strip()
                    if kw in chunk_text.lower() and chunk_text.lower() not in used_texts:
                        sentence_map[kw].append(chunk_text)
                        used_texts.add(chunk_text.lower())
                        chunks_added += 1
                        if len(sentence_map[kw]) >= max_points_per_kw:
                            break

                # Fallback to full sentence if not enough info
                if chunks_added == 0 and sent_lower not in used_texts:
                    sentence_map[kw].append(sent_text)
                    used_texts.add(sent_lower)

    return sentence_map

# --- Graphviz mind map rendering ---
def render_mindmap(main_topic, grouped_data):
    dot = graphviz.Digraph(format="png")
    dot.attr(rankdir="LR", splines="true")
    dot.node(main_topic, shape="box", style="filled", color="lightblue")

    for keyword, points in grouped_data.items():
        dot.node(keyword, shape="ellipse", style="filled", color="lightgreen")
        dot.edge(main_topic, keyword)

        for i, point in enumerate(points):
            label_id = f"{keyword}_pt{i+1}"
            label = point if len(point) <= 80 else point[:77] + "..."
            dot.node(label_id, label, shape="note", style="filled", color="orange")
            dot.edge(keyword, label_id)

    return dot

# --- Save rendered image to bytes ---
def save_mindmap(dot, filename="mindmap"):
    with tempfile.TemporaryDirectory() as tmpdirname:
        filepath = os.path.join(tmpdirname, filename)
        try:
            rendered_path = dot.render(filepath, cleanup=True)
            with open(rendered_path, "rb") as f:
                return f.read()
        except Exception as e:
            st.error(f"Error saving mindmap: {e}")
            return None

# --- Streamlit App UI ---
st.set_page_config(page_title="Smart Mind Map Generator", layout="centered")
st.title("🧠 Smart Mind Map Generator from Paragraph")

example = """Artificial Intelligence (AI) is a branch of computer science that aims to create intelligent machines. 
It has become an essential part of the technology industry. Research associated with artificial intelligence is highly technical and specialized. 
The core problems of AI include programming computers for certain traits such as knowledge, reasoning, problem solving, perception, learning, planning, and language processing.
Machine learning is a subset of AI that focuses on the ability of systems to learn from data. Natural language processing (NLP) helps machines understand human language."""

text_input = st.text_area("Paste your paragraph here:", value=example, height=300)

if st.button("Generate Mind Map"):
    if not text_input.strip():
        st.warning("Please provide a valid paragraph.")
    else:
        with st.spinner("Generating mind map..."):
            main_topic = "Artificial Intelligence"  # Can be made dynamic later
            keywords = extract_keywords(text_input, num_keywords=6)
            grouped_data = extract_key_points(text_input, keywords, max_points_per_kw=4)
            dot = render_mindmap(main_topic, grouped_data)
            st.graphviz_chart(dot)

            image_bytes = save_mindmap(dot)
            if image_bytes:
                st.image(image_bytes, caption="Mind Map", use_container_width=True)
                st.download_button("📥 Download as PNG", data=image_bytes, file_name="mindmap.png", mime="image/png")
