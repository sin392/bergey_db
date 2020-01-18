import xml.etree.ElementTree as ET
from tqdm import tqdm

tree = ET.parse('../xml/test.xml')
root = tree.getroot()
print(root)

pages = []
microbe_list = []
bold_flag = False

for child in tqdm(root):
    table_flag = False
    page = ""
    # page
    for child_2 in child:
        # textbox, rect
        textbox = ""
        for child_3 in child_2:
            # textline
            textline = ""
            bold_word = ""
            count = 0
            bold_words = []
            for child_4 in child_3:
                # text, image, textgroup
                if type(child_4.text) == str: textline += child_4.text
                # 見出し判定
                if child_4.tag == "text":
                    if "font" not in child_4.attrib:
                        # space
                        if bold_word != "": bold_word += " "
                    elif "Bold" in child_4.attrib["font"]:
                        # 行の先頭のもののみ抜出
                        if bold_word == "" and count > 5:
                            continue
                        else:
                            bold_word += child_4.text
                    # space終わりの場合対策に条件文は分ける
                    else:
                        if bold_word != "" and bold_word[0].isupper():
                            bold_words.append(bold_word.strip())
                        bold_word = ""
                    if child_4 == child_3[-1] and bold_word != "" and bold_word[0].isupper():
                        bold_words.append(bold_word.strip())
                        bold_word = ""
                    count += 1

            for i in range(len(bold_words)):
                if bold_words[i].startswith("TABLE") or bold_words[i].startswith("FIGURE") or len(bold_words[i]) <= 3 \
                or bold_words[i].endswith("-") or bold_words[i].endswith(".") or "," in bold_words[i] or len(bold_words[i].split(" ")) >= 5 \
                or ";" in bold_words[i] or ":" in bold_words[i]:
                    bold_words[i] = ""
            bold_words = [x for x in bold_words if x != ""]
            if len(bold_words) > 0:
                print(bold_words)
                for x in bold_words:
                    microbe_list.append(x)

            if table_flag:
                if child_3.tag == "textline":
                    if child_3[0].tag == "text":
                        font_size = child_3[0].attrib["size"]
                        if float(font_size) >= 10:
                            table_flag = False
                        else:
                            continue
                    else:
                        continue
                else:
                    continue
            elif textline.startswith("TABLE"):
                table_flag = True
                break
            else:
                if len(textline.strip()) > 2:
                    if len(bold_words) > 0 and microbe_list[-1] in textline:
                        for x in bold_words:
                            textline = textline.replace(x, f"<{x}>")
                            bold_flag = True
                            print(textline)
                    if not textline.endswith(".\n"):
                        textline = textline.replace("\n", " ")
                    textbox += textline
        if textbox != "" and bold_flag:
            # for tail in [".\n", ". \n"]:
                # if textbox.endswith(tail):
                    # tail_word = textbox.replace(tail, "")[::-1].split()[0]
                    # if len(tail_word) > 1:
                    #     textbox = textbox.strip() + "<end>\n"
                    #     bold_flag = False
            textbox = "<end>\n" + textbox
            bold_flag = False

        page += textbox
    if child == root[-1]:
        page = page + "<end>\n"
    # print(page)
    pages.append(page.strip())
    # if child == root[3]:
    #     break

with open("../txt/microbes.txt", "w") as f:
    for x in microbe_list:
        # x = x.strip()
        # if x.startswith("TABLE") or x.startswith("FIGURE") or len(x) <= 3 \
        #     or x.endswith("-") or x.endswith(".") or "," in x or len(x.split()) >= 5 \
        #     or ";" in x or ":" in x:
        #     # ","などを含む見出しも存在するが、物質名ではないと考え除外
        #     continue
        # else:
        print(x, file=f)
with open("../txt/pages.txt", "w") as f_p:
    for page in pages:
        print(page, file=f_p)