print("Initializing...")

from bs4 import BeautifulSoup
from ebooklib import epub
import ebooklib
from sudachipy import Dictionary, SplitMode
import re

tokenizer_obj = Dictionary().create()

def main():
    f = input("Type name of file: ")

    try:
        book = epub.read_epub(f)
    except FileNotFoundError:
        print(f"Error: File '{f}' was not found.")
        return
    except epub.EpubException as e:
        print(f"Epub Error: {e}. Possibly tried to load non-compatible file?")
        return

    sentences = get_sentences(book)

    print("Indexing file...")

    index = create_index(sentences)

    print("Found words:", len(index))

    search_loop(index)

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

def search_loop(index):
    word = input("Type a word: ")
    while word:
        tokens = tokenize(word)
        if not tokens:
            print("Could not tokenize input.")
            word = input("Type a word: ")
            continue
        w = tokens[0]
        if w in index:
            for s in index[w]:
                t_sentence = tokenizer_obj.tokenize(s, SplitMode.C)
                target_list = []
                for t in t_sentence:
                    if t.dictionary_form() == w:
                        target_list.append(t.surface())
                
                highlighted_text = s

                for tw in target_list:
                    highlighted_text = highlighted_text.replace(tw, f"{'\033[96m'}{tw}{'\033[0m'}")
                print(highlighted_text, '\n')
        else:
            print("Word not found.")
        word = input("Type a word: ")

def has_japanese(text):
    # This pattern covers Hiragana, Katakana, and the main Kanji block
    jp_pattern = re.compile(r'[\u3040-\u30ff\u4e00-\u9fff]')
    return bool(jp_pattern.search(text))

def tokenize(sentence):
    return [m.dictionary_form() for m in tokenizer_obj.tokenize(sentence, SplitMode.C)]

