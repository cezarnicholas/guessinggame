import os
import sys
import random
import tkinter
import tkinter.font


def resource_path(relative_path: str) -> str:
    base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base_path, relative_path)


with open(resource_path(".words"), encoding="utf-8") as f:
    word_list = [word.strip() for word in f]

word = ""
hint = ""
letter = ""
unique_chars = []
words_left = True
has_won = False


def pick_word():
    global word, hint, unique_chars, words_left

    # if not word_list:
    #     words_left = False
    #     return

    if not word_list:
        words_left = False
        return False

    temp = random.choice(word_list)
    word_list.remove(temp)
    word, hint = temp.split(" # ")
    unique_chars = [ch for ch in dict.fromkeys(word) if ch != ' ']
    words_left = bool(word_list)

    return words_left


pick_word()
frame = tkinter.Tk()
frame.geometry("620x550")
frame.minsize(620, 550)
frame.maxsize(620, 550)
frame.config(highlightthickness=4, highlightcolor="#FF0090")

f1 = tkinter.font.Font(family="Times New Roman", size=16)
f2 = tkinter.font.Font(family="Times New Roman", size=24, weight="bold")
f3 = tkinter.font.Font(family="Times New Roman", size=14)
f4 = tkinter.font.Font(family="Times New Roman", size=32)
f5 = tkinter.font.Font(family="Times New Roman", size=18, weight="bold")
f6 = tkinter.font.Font(family="Times New Roman", size=16, weight="bold")

hint_label = tkinter.Label(frame, text=hint, font=f1,
                           wraplength=455, justify="center")
hint_label.pack()
len_label = tkinter.Label(frame, text=str(len(word)) + " letters", font=f3)
len_label.pack()

mask = [" " if c == " " else "_" for c in word]
word_label = tkinter.Label(frame, text="".join(mask), font=f2)
word_label.pack()
win_label = tkinter.Label(frame,
                          text="ai castigat! esti cea mai tare",
                          font=f2,
                          fg="#FF69B4")
win_label.pack()
win_label.pack_forget()

ultimate_winner = tkinter.Label(frame,
                                text="ultimate winner!\nnici nu mai am cuvinte.\nprize: 10000 bunny kisses <3333",
                                font=f4,
                                fg="#FF0090",
                                wraplength=500)


def validate_guess(new_value: str) -> bool:
    if new_value == "":
        return True

    if len(new_value) > 1:
        return False

    return new_value.isalpha()


vcmd = (frame.register(validate_guess), "%P")
guess_var = tkinter.StringVar()
guess_entry = tkinter.Entry(frame,
                            textvariable=guess_var,
                            font=f6,
                            width=2,
                            justify="center",
                            validate="key",
                            validatecommand=vcmd,
                            bg="#FF69B4")
guess_entry.pack(pady=10)
guess_entry.focus_set()


def submit_guess(event=None):
    global mask, unique_chars
    g = guess_var.get().strip()
    guess_var.set("")

    g = g.lower()
    if any(c == g for c in word if c != " "):
        for i, c in enumerate(word):
            if c == g:
                mask[i] = c

        len_label.config(text=str(mask.count("_")) + " letters remaining")
        word_label.config(text="".join(mask))
        unique_chars = [ch for ch in unique_chars if ch != g]

    if "_" not in mask:
        on_win()
        return


guess_entry.bind("<Return>", submit_guess)

word_guess_var = tkinter.StringVar()
word_entry = tkinter.Entry(frame,
                           textvariable=word_guess_var,
                           font=f6,
                           width=29,
                           justify="center",
                           bg="#FF0090")
word_entry.pack(pady=5)


def submit_word_guess(event=None):
    global mask, unique_chars
    wg = word_guess_var.get().strip()
    word_guess_var.set("")
    if len(wg) > len(word):
        return

    wg = wg.lower()
    ul = list(dict.fromkeys(wg))
    for ch in ul:
        if any(c == ch for c in word if c != ' '):
            for i, c in enumerate(word):
                if c == ch:
                    mask[i] = c
            len_label.config(text=str(mask.count("_")) + " letters remaining")
            word_label.config(text="".join(mask))
            unique_chars = [uc for uc in unique_chars if uc != ch]

    if "_" not in mask:
        on_win()
        return


word_entry.bind("<Return>", submit_word_guess)
guess_entry.bind("<FocusIn>", lambda e: word_guess_var.set(""))
word_entry.bind("<FocusIn>", lambda e: guess_var.set(""))


def on_win():
    global has_won
    has_won = True
    win_label.pack()
    reveal_btn.config(state=tkinter.DISABLED)
    letter_btn.config(state=tkinter.DISABLED)
    guess_entry.config(state=tkinter.DISABLED)
    word_entry.config(state=tkinter.DISABLED)
    if has_won and not words_left:
        win_label.pack_forget()
        ultimate_winner.pack()


def reveal_word():
    global mask, unique_chars
    mask = list(word)
    unique_chars = []
    len_label.config(text="0 letters remaining")
    word_label.config(text=word)
    on_win()


def reveal_letter():
    global letter, unique_chars, mask
    if not unique_chars:
        return

    letter = random.choice(unique_chars)
    unique_chars.remove(letter)

    for i, c in enumerate(word):
        if c.lower() == letter.lower():
            mask[i] = letter

    len_label.config(text=str(mask.count("_")) + " letters remaining")
    word_label.config(text=str("".join(mask)))
    if "_" not in mask:
        on_win()


def change_word():
    global mask
    pick_word()

    mask = [" " if c == " " else "_" for c in word]
    hint_label.config(text=hint)
    len_label.config(text=str(len(word)) + " letters")
    word_label.config(text="".join(mask))
    win_label.pack_forget()
    reveal_btn.config(state=tkinter.NORMAL)
    letter_btn.config(state=tkinter.NORMAL)
    guess_entry.config(state=tkinter.NORMAL)
    guess_entry.focus_set()
    word_entry.config(state=tkinter.NORMAL)

    if not words_left:
        newgame_btn.config(state=tkinter.DISABLED)


reveal_btn = tkinter.Button(frame,
                            text="Reveal solution",
                            font=f1,
                            command=reveal_word)
letter_btn = tkinter.Button(frame,
                            text="Reveal letter",
                            font=f1,
                            command=reveal_letter)
newgame_btn = tkinter.Button(frame,
                             text="Get another word!",
                             font=f1,
                             command=change_word)

reveal_btn.pack()
letter_btn.pack()
newgame_btn.pack()

love = tkinter.Label(frame,
                     text="jsyk: cez loves lis <3",
                     fg="#FF69B4",
                     font=f5)
love.pack()

frame.mainloop()
