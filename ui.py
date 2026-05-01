import streamlit as st
import tempfile
import os
from ebook_extractor import get_sentences, create_index, tokenize
from sudachipy import SplitMode
from sudachipy import Dictionary, SplitMode

st.set_page_config(page_title="文検索", page_icon="📖")
st.title("文検索")

@st.cache_resource
def get_tokenizer():
    return Dictionary().create()
tokenizer_obj = get_tokenizer()


@st.cache_resource
def build_index(file_bytes):
    # Write to a temp file since ebooklib needs a path
    with tempfile.NamedTemporaryFile(delete=False, suffix=".epub") as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name

    from ebooklib import epub
    book = epub.read_epub(tmp_path)


    os.unlink(tmp_path)

    sentences = get_sentences(book)
    index = create_index(sentences, tokenizer_obj)
    return index

uploaded_file = st.file_uploader("Upload an EPUB file", type="epub")

if uploaded_file:
    with st.spinner("Indexing..."):
        index = build_index(uploaded_file.read())
    st.success(f"Indexed {len(index)} unique words.")
    
    st.set_page_config(page_title=f"{uploaded_file.name.replace(".epub", "")} | 文検索", page_icon="📖")

    word = st.text_input("Search for a word:")

    if word:
        tokens = tokenize(word, tokenizer_obj)
        if not tokens:
            st.warning("Could not tokenize input.")
        else:
            w = tokens[0]
            if w in index:
                st.write(f"**{len(index[w])}** sentences found for **{w}**")
                for s in index[w]:
                    t_sentence = tokenizer_obj.tokenize(s, SplitMode.C)
                    target_list = []
                    for t in t_sentence:
                        if t.dictionary_form() == w:
                            target_list.append(t.surface())

                    highlighted = s
                    for tw in target_list:
                        highlighted = highlighted.replace(tw, f"<mark>{tw}</mark>")

                    st.markdown(highlighted, unsafe_allow_html=True)
                    st.divider()
            else:
                st.warning("Word not found.")
