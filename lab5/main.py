import copy
import string
import typing as tp
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog as fd
import nltk
from dataclasses import dataclass

ffont = "Helvetica 15 bold"
window = tk.Tk()
dictionary = dict()
help_dict = dictionary.items()
entry_template = tk.Entry()
entry_old_word = tk.Entry()
entry_new_word = tk.Entry()
entry_delete_word = tk.Entry()
entry_adding_word = tk.Entry()
entry_filepath = tk.Entry()
entry_filepath_new = tk.Entry()
entry_tag = tk.Entry()
entry_lemma = tk.Entry()


def check_string_is_word(string_: str) -> bool:
    for symbol in string_:
        if symbol in string.ascii_lowercase:
            return True

    return False


@dataclass
class DictItem:
    tags: tp.Dict[str, int]
    frequency: int
    initial_form: str


def get_and_split_text_into_dictionary() -> None:
    global dictionary
    global help_dict
    input_file_name = "dataset.txt"
    with open(input_file_name, "r") as input_file:
        text = input_file.read().lower()
    toktok = nltk.toktok.ToktokTokenizer()
    tokenized_text = toktok.tokenize(text)
    tagged_text = nltk.pos_tag(tokenized_text)
    d = dict()
    for word, tag in tagged_text:
        if check_string_is_word(word):
            d[word] = d.get(word, DictItem(tags=dict(), frequency=0,
                                           initial_form=nltk.WordNetLemmatizer().lemmatize(word)))
            d[word].tags[tag] = d[word].tags.get(tag, 0) + 1
            d[word].frequency += 1
    dictionary = d
    help_dict = copy.deepcopy(d).items()
    print_dictionary()


def print_dictionary() -> None:
    global window
    global dictionary
    global dict_
    global words_num
    words_num.config(
        text=f"Всего слов: {sum(item.frequency for word, item in help_dict):,}\nУникальных: {len(help_dict):,}")
    string_ = [""]
    for word, item in help_dict:
        string_ += f"word: {word}, tags: {set(item.tags.keys())}, frequency: {item.frequency}, initial form: {item.initial_form}\n"
    dict_.config(state=tk.NORMAL)
    dict_.delete("1.0", tk.END)
    dict_.insert(tk.END, ''.join(string_))
    dict_.config(state=tk.DISABLED)


def find_words_by_template() -> dict.items:
    global dictionary
    global entry_start
    global entry_end
    start = entry_start.get()
    end = entry_end.get()
    words = {word: item for word, item in dictionary.items() if
             word.startswith(start.lower()) and word.endswith(end.lower())}
    return words.items()


def get_template_sorted_by_words_asc() -> None:
    global dictionary
    global help_dict
    global window
    global dict_
    global words_num
    help_dict = sorted(find_words_by_template(), key=lambda x: x[0])

    print_dictionary()


def get_template_sorted_by_words_desc() -> None:
    global dictionary
    global help_dict
    global window
    global dict_
    global words_num
    help_dict = sorted(find_words_by_template(), key=lambda x: x[0], reverse=True)

    print_dictionary()


def get_template_sorted_by_frequencies_asc() -> None:
    global window
    global help_dict
    global dictionary
    global dict_
    global words_num
    help_dict = sorted(find_words_by_template(), key=lambda x: x[1].frequency)
    print_dictionary()


def get_template_sorted_by_frequencies_desc() -> None:
    global window
    global help_dict
    global dictionary
    global dict_
    global words_num
    help_dict = sorted(find_words_by_template(), key=lambda x: -x[1].frequency)
    print_dictionary()


def delete_word_from_dictionary() -> None:
    global dict_
    global dictionary
    global help_dict
    global entry_delete_word
    top = tk.Toplevel(window)
    top.title("Удаление")
    word_entry = tk.Entry(top, font=ffont)
    word_entry.pack()

    def delete_button():
        word = word_entry.get()
        response = messagebox.askyesno("Удаление", "Вы уверены?")
        dict_.config(state=tk.NORMAL)
        dict_.delete("1.0", tk.END)
        if response:
            res = dictionary.pop(word, "default")
            if res == "default":
                dict_.insert(tk.END, f"Слова {word} нет в словаре")
            else:
                dict_.insert(tk.END, f"Слово {word} удалено")

        else:
            dict_.insert(tk.END, f"Отменено")
        dict_.config(state=tk.DISABLED)

    tk.Button(top, text="Удалить", font=ffont, command=delete_button).pack(side=tk.LEFT)




def insert_word_into_dictionary() -> None:
    global dict_
    global dictionary
    global entry_adding_word
    global entry_tag
    global entry_lemma

    top = tk.Toplevel(window)
    top.title("Добавление")
    frame1 = tk.Frame(top)
    tk.Label(frame1, text="Слово", font=ffont).pack(side=tk.LEFT)
    word_entry = tk.Entry(frame1, font=ffont)
    word_entry.pack(side=tk.LEFT)
    frame1.pack()
    frame2 = tk.Frame(top)
    tk.Label(frame2, text="Код", font=ffont).pack(side=tk.LEFT)
    tag_entry = tk.Entry(frame2, font=ffont)
    tag_entry.pack(side=tk.LEFT)
    frame2.pack()
    frame3 = tk.Frame(top)
    tk.Label(frame3, text="Лемма", font=ffont).pack(side=tk.LEFT)
    lemma_entry = tk.Entry(frame3, font=ffont)
    lemma_entry.pack(side=tk.LEFT)
    frame3.pack()

    def add_button():
        word = word_entry.get()
        tag = tag_entry.get()
        lemma = lemma_entry.get()
        dict_.config(state=tk.NORMAL)
        dict_.delete("1.0", tk.END)
        if word not in dictionary:
            dictionary[word] = DictItem(tags={tag: 0}, initial_form=lemma, frequency=0)
            dict_.insert(tk.END, f"Слово {word} добавлено в словарь")
        else:
            dict_.insert(tk.END, f"Слово {word} уже есть в словаре")
        dict_.config(state=tk.DISABLED)

    tk.Button(top, text="Добавить", font=ffont, command=add_button).pack(side=tk.LEFT)




def correct_word() -> None:
    global dictionary
    global entry_old_word
    global entry_new_word
    global dict_

    top = tk.Toplevel(window)
    top.title("Исправление")
    frame1 = tk.Frame(top)
    tk.Label(frame1, text="Старое значение", font=ffont).pack(side=tk.LEFT)
    word_entry = tk.Entry(frame1, font=ffont)
    word_entry.pack(side=tk.LEFT)
    frame1.pack()
    frame2 = tk.Frame(top)
    tk.Label(frame2, text="Новое значение", font=ffont).pack(side=tk.LEFT)
    new_word_entry = tk.Entry(frame2, font=ffont)
    new_word_entry.pack(side=tk.LEFT)
    frame2.pack()

    def correct_button():
        word_to_correct = word_entry.get()
        swap = new_word_entry.get()
        old_dict_item = dictionary.get(word_to_correct)
        if old_dict_item is None:
            dict_.config(state=tk.NORMAL)
            dict_.delete("1.0", tk.END)
            dict_.insert(tk.END, "Нет таких слов в словаре")
            dict_.config(state=tk.DISABLED)
            return None

        dictionary[swap] = dictionary.get(swap, DictItem(frequency=0, tags=dict(), initial_form=''))
        dictionary[swap].frequency += old_dict_item.frequency
        dictionary[swap].initial_form = old_dict_item.initial_form
        for tag, freq in old_dict_item.tags:
            dictionary[swap].tags[tag] = dictionary[swap].tags.get(tag, 0) + freq
        text = ""
        with open("dataset.txt", "r") as file:
            text = file.read()

        with open("dataset.txt", "w") as file:
            print(text.replace(word_to_correct, swap), file=file)

        dict_.config(state=tk.NORMAL)
        dict_.delete("1.0", tk.END)
        dict_.insert(tk.END, "Corrected")
        dict_.config(state=tk.DISABLED)

    tk.Button(top, text="Исправить", font=ffont, command=correct_button).pack(side=tk.LEFT)




def save_dictionary() -> None:
    global dictionary
    global dict_
    global entry_filepath

    f = fd.asksaveasfile(mode='w', defaultextension=".txt")
    if f is None:
        return

    with open(f.name, "w") as output_file:
        for word, frequency in dictionary.items():
            print(f"word: {word}, frequency: {frequency}", file=output_file)

    dict_.config(state=tk.NORMAL)
    dict_.delete("1.0", tk.END)
    dict_.insert(tk.END, "Dictionary is saved")
    dict_.config(state=tk.DISABLED)


def add_text() -> None:
    global entry_filepath_new
    global dictionary
    global dict_
    text = ""
    dict_.config(state=tk.NORMAL)
    dict_.delete("1.0", tk.END)

    filetypes = (
        ('text files', '*.txt'),
        ('All files', '*.*')
    )
    f = fd.askopenfile(filetypes=filetypes)

    with open(f.name, "r") as rfile:
        with open("dataset.txt", "a") as afile:
            afile.write("\n")
            afile.write(rfile.read())

    get_and_split_text_into_dictionary()
    dict_.insert(tk.END, "Added new text")
    dict_.config(state=tk.DISABLED)
    return None


def print_help() -> None:
    global dictionary
    global window
    global dict_
    with open('tags.txt', 'r') as tags_file:
        string_ = tags_file.read()
    dict_.config(state=tk.NORMAL)
    dict_.delete("1.0", tk.END)
    dict_.insert(tk.END, ''.join(string_))
    dict_.config(state=tk.DISABLED)


def print_pairs_word_tag_stat() -> None:
    global dictionary
    global dict_
    string_ = ""
    for word, item in dictionary.items():
        for tag, frequency in sorted(item.tags.items(), key=lambda x: -x[1]):
            string_ += f"word: {word}, tag: {tag}, frequency: {frequency}\n"
    dict_.config(state=tk.NORMAL)
    dict_.delete("1.0", tk.END)
    dict_.insert(tk.END, string_)
    dict_.config(state=tk.DISABLED)


def new_dict() -> None:
    open("dataset.txt", "w").close()
    get_and_split_text_into_dictionary()


def main() -> None:
    global window
    global dictionary
    global entry_template
    global dict_

    menubar = tk.Menu(window)

    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="Добавить", command=lambda: add_text())
    filemenu.add_command(label="Сохранить", command=lambda: save_dictionary())
    filemenu.add_command(label="Новый словарь", command=lambda: new_dict())
    filemenu.add_separator()
    filemenu.add_command(label="Выход", command=window.quit)
    menubar.add_cascade(label="Файл", menu=filemenu)

    menubar.add_command(label="Помощь", command=lambda: print_help())

    window.config(menu=menubar)

    frame1 = tk.Frame(window)
    global words_num
    words_num = tk.Label(frame1, font=ffont)
    words_num.pack(side=tk.LEFT)
    words_num.config(
        text=f"Всего слов: \nУникальных: ")
    frame1.pack()

    frame2 = tk.Frame(window)
    tk.Label(frame2, text="Начало", font=ffont).pack(side=tk.LEFT)
    global entry_start
    entry_start = tk.Entry(frame2, font=ffont)
    entry_start.pack(side=tk.LEFT)
    tk.Label(frame2, text="Конец", font=ffont).pack(side=tk.LEFT)
    global entry_end
    entry_end = tk.Entry(frame2, font=ffont)
    entry_end.pack(side=tk.LEFT)
    frame2.pack()

    frame3 = tk.Frame(window)
    button_sort_template_by_alphabet_ascending = tk.Button(frame3, text="Слово (возрастание)",
                                                           command=get_template_sorted_by_words_asc)
    button_sort_template_by_alphabet_ascending.pack(side=tk.LEFT)

    button_sort_template_by_alphabet_descending = tk.Button(frame3, text="Слово (убывание)",
                                                            command=get_template_sorted_by_words_desc)
    button_sort_template_by_alphabet_descending.pack(side=tk.LEFT)

    button_sort_template_by_frequency_ascending = tk.Button(frame3, text="Частота (возрастание)",
                                                            command=get_template_sorted_by_frequencies_asc)
    button_sort_template_by_frequency_ascending.pack(side=tk.LEFT)

    button_sort_template_by_frequency_descending = tk.Button(frame3, text="Частота (убывание)",
                                                             command=get_template_sorted_by_frequencies_desc)
    button_sort_template_by_frequency_descending.pack(side=tk.LEFT)
    frame3.pack()

    frame4 = tk.Frame(window)
    global dict_
    dict_ = tk.Text(frame4)
    dict_.pack()
    frame4.pack()

    frame5 = tk.Frame(window)
    tk.Button(frame5, text="Удалить", font=ffont, command=lambda: delete_word_from_dictionary()).pack(side=tk.LEFT)
    tk.Button(frame5, text="Исправить", font=ffont, command=lambda: correct_word()).pack(side=tk.LEFT)
    tk.Button(frame5, text="Добавить", font=ffont, command=lambda: insert_word_into_dictionary()).pack(side=tk.LEFT)
    frame5.pack()

    button_print_pairs_word_tag = tk.Button(window, text="Количество кодов слова", font=ffont,
                                            command=print_pairs_word_tag_stat)
    button_print_pairs_word_tag.pack()
    window.title("Dictionary")
    print_dictionary()
    window.mainloop()


if __name__ == "__main__":
    main()
