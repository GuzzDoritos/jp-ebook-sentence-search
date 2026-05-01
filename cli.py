from ebooklib import epub
from sudachipy import SplitMode
from ebook_extractor import get_sentences, create_index, tokenize, tokenizer_obj

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


if __name__ == "__main__":
    main()