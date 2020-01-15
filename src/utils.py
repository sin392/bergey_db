import re

def color_word(string, word, color):
    idx = re.search(word, string)
    if color == "red":
        word_clr = f"<font color='{color}'><b>{word}</b></font>"
    else:
        word_clr = f"<font color='{color}'>{word}</font>"

    string = string[:idx.start()] + word_clr + string[idx.end():]

    return string

def make_html(string, keyword, keyword_idx, verbs, verbs_idx):
    with open("log.html", "a") as f:

        # highlight keyword

        string = color_word(string, keyword, color="red")

        # highlight verbs
        for verb in verbs:
            string = color_word(string, verb, color="blue")

        f.write("<p>")
        f.write(f"<b>keyword : {keyword}</b><br>")
        f.write(f"<b>used_verbs : {verbs}</b><br>")
        f.write(string)
        f.write("</p>")
