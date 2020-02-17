import xml.etree.ElementTree as ET
from tqdm import tqdm

tree = ET.parse('../xml/test.xml')
root = tree.getroot()
print(root)

pages = []
order_list = []
family_list = []
genus_list = []
microbe_list = []

bold_flag = False
order_flag = False
family_flag = False
genus_flag = False

for child in tqdm(root):
    table_flag = False
    figure_flag = False
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
                # Order, Family, Genus, Spiecies判定
                if child_4.tag == "text":
                    if "font" not in child_4.attrib:
                        # space
                        if bold_word != "": bold_word += " "
                    elif "Bold" in child_4.attrib["font"]:
                        # 属名等はGenus ~ の後にBoldが来る
                        if not order_flag and textline.startswith("Order"):
                            order_flag = True
                        elif not family_flag and textline.startswith("Family"):
                            family_flag = True
                        elif not genus_flag and textline.startswith("Genus"):
                            genus_flag = True
                        # 行の先頭のもののみ抜出
                        if bold_word == "" and count > 5:
                            continue
                        else:
                            bold_word += child_4.text

                    # space終わりの場合対策に条件文は分ける
                    else:
                        if order_flag:
                            order_list.append(textline[:-2])
                            order_flag = False
                        elif family_flag:
                            family_list.append(textline[:-2])
                            family_flag = False
                        elif genus_flag:
                            genus_list.append(textline[:-2])
                            genus_flag = False
                        if bold_word != "" and (bold_word[0].isupper() or bold_word[0] == "“"):
                            bold_words.append(bold_word.strip())
                        bold_word = ""

                    if child_4 == child_3[-1] and bold_word != "" and (bold_word[0].isupper() or bold_word[0] == "“"):
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
                    microbe_list.append((order_list[-1], family_list[-1], genus_list[-1], x))

            for name, flag in [("TABLE", table_flag), ("FIGURE", figure_flag)]:
                if flag:
                    if child_3.tag == "textline":
                        if child_3[0].tag == "text":
                            font_size = child_3[0].attrib["size"]
                            if float(font_size) >= 10:
                                flag = False
                            else:
                                continue
                        else:
                            continue
                    else:
                        continue
                elif textline.startswith(name):
                    flag = True
                    break
                elif textline.startswith(name):
                    flag = True
                    break

            else:
                if len(textline.strip()) > 2:
                    if textline.split()[0].isdigit():
                        textline = ""
                        # pass
                    elif textline.split()[0] in ["Order", "Family", "Genus", "ORDER", "FAMILY", "GENUS"]:
                        textline = ""
                        # pass
                    elif not textline.endswith(".\n"):
                        textline = textline.replace("\n", " ")
                    if len(bold_words) > 0 and microbe_list[-1][-1] in textline:
                        for x in bold_words:
                            # 先頭の数字などはカット 
                            textline = textline[textline.find(x):]
                            textline = textline.replace(x+" ", f"<{x}>\n")
                            bold_flag = True
                            # print(textline)
                    textline = textline.replace("- ", "")
                    textbox += textline

        if textbox != "" and bold_flag:
            textbox = "<end>\n" + textbox
            bold_flag = False

        page += textbox
    if child == root[-1]:
        page = page + "\n<end>\n"
    pages.append(page.strip())

# 手作業による修正の反映
with open("../txt/microbes_mo.txt", "r") as f:
    microbes_mo = [x.strip() for x in f.readlines()]

with open("../csv/microbes.csv", "w") as f:
    for o, fa, g, s in microbe_list:
        # x = x.strip()
        # if x.startswith("TABLE") or x.startswith("FIGURE") or len(x) <= 3 \
        #     or x.endswith("-") or x.endswith(".") or "," in x or len(x.split()) >= 5 \
        #     or ";" in x or ":" in x:
        #     # ","などを含む見出しも存在するが、物質名ではないと考え除外
        #     continue
        # else:
        if s in microbes_mo:
            print(f"{o}, {fa}, {g}, {s}", file=f)
with open("../txt/pages.txt", "w") as f:
    for page in pages:
        print(page, file=f)