print("Initializing...")

import streamlit as st
from bs4 import BeautifulSoup
import ebooklib
from sudachipy import SplitMode
import re


def get_sentences(book):
    sentences = []

    all_items = book.get_items()

    for item in all_items:
        if item.get_type() == ebooklib.ITEM_DOCUMENT:

            soup = BeautifulSoup(item.get_body_content().decode('utf-8'), "lxml")

            for element in soup(["script", "style", "ruby"]):
                element.decompose()

            for p in soup.find_all('p'):
                txt = p.text
                if has_japanese(txt):
                    sentences.append(txt)

    return sentences

def create_index(sentences):
    index = {} 
    for s in sentences:
        for token in tokenize(s):
            if (has_japanese(token)):
                if (token not in index):
                    index[token] = set()
                index[token].add(s)
    return index

def has_japanese(text):
    # This pattern covers Hiragana, Katakana, and the main Kanji block
    jp_pattern = re.compile(r'[\u3040-\u30ff\u4e00-\u9fff]')
    return bool(jp_pattern.search(text))

def tokenize(sentence):
    return [m.dictionary_form() for m in tokenizer_obj.tokenize(sentence, SplitMode.C)]

