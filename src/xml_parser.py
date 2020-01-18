import xml.etree.ElementTree as ET
import re
import numpy as np
from tqdm import tqdm
from time import time

class XMLParser():
    def __init__(self):
        self.pages = []
        self.flatten_list = []
        self.replace_list = []
        self.ignore_flag = False
        self.microbes = []
        self.text = ""

    def _format_textline(self, tag_list):
        if not tag_list == []:
            string = "".join([x.text for x in tag_list])
        if len(string.strip()) <= 3:
            return []
        if self.ignore_flag:
            font_size_list = [float(x.attrib["size"]) if "size" in x.attrib else -1.0
                                for x in tag_list]
            for i, s in enumerate(font_size_list):
                if s >= 10:
                    tag_list = tag_list[:i]
                    self.ignore_flag = False
                    return tag_list
            return []
        elif string.startswith("TABLE") or string.startswith("FIGURE"):
            self.ignore_flag = True
            return []

        m = re.search(r"..?? ??\n", string)
        if m != None:
            start = m.start()
            tag_list = tag_list[:start]
            string = string[:start]

        tail = string[-2:]
        space_tag = ET.Element("text", attrib={})
        space_tag.text = " "
        if tail != ".\n" and tail[-1] == "\n":
            tag_list = tag_list[:-1] + [space_tag]
        if tail == " \n":
            tag_list = tag_list[:-1]
        if tail == "-\n":
            tag_list = tag_list[:-2]

        return tag_list
    
    def _flatten(self, tag_list:list) -> list:
        flatten_list = []
        parent = tag_list
        while type(parent[0]) == list:
            # print(type(parent[0]))
            for child in tqdm(parent):
                flatten_list.append(child)
            parent = flatten_list
        return flatten_list

    def _extract_microbes(self, textline):
        # 行頭5文字以内からはじまるものをチェック
        microbes = []
        N = len(textline)
        if N <= 5: return microbes
        for i in range(4):
            tag_att = textline[i].attrib
            font = tag_att["font"] if "font" in tag_att else "none"
            if "Bold" in font and textline[i].text.isupper():
                bold_word = ""
                for j in range(i, N):
                    tag_att_j = textline[j].attrib
                    if "font" not in tag_att_j or "Bold" in tag_att_j["font"]:
                        bold_word += textline[j].text
                    else:
                        break
                bold_word = bold_word.strip()
                if bold_word.endswith(".") or len(bold_word.split()) >= 5 or ";" in bold_word or ":" in bold_word \
                    or re.match(r".*\d+.*", bold_word) != None:
                    break
                else:
                    microbes.append(bold_word)
                    break
        return microbes


    def _get_text(self, tag_list=[]) -> str:
        N = len(tag_list)
        if N > 0 and N < 10000:
            flatten_list = self._flatten(tag_list)
        else:
            flatten_list = self.flatten_list
        charcter_list = [tag.text for tag in flatten_list]
        text = "".join(charcter_list)
        return text

    def parse(self, xml_path:str):
        tree = ET.parse(xml_path)
        root = tree.getroot()
        nl_tag = ET.Element("text", attrib={})
        nl_tag.text = "\n"
        for tag_page in tqdm(root):
            if tag_page.tag != "page": continue
            page = []
            for tag_textbox in tag_page:
                if tag_textbox.tag != "textbox": continue
                textbox = []
                for tag_textline in tag_textbox:
                    if tag_textline.tag != "textline": continue
                    textline = []
                    for tag_char in tag_textline:                        
                        if tag_char.tag != "text": continue
                        textline.append(tag_char)
                    textline = self._format_textline(textline)
                    self.microbes += self._extract_microbes(textline)
                    if textline != []:
                        textbox.append(textline)
                        for x in textline:
                            self.flatten_list.append(x)
                if textbox != []:
                    page.append(textbox)
        self.text = self._get_text(self.flatten_list)


if __name__ == "__main__":
    xml_path = '../xml/test.xml'
    doc_p = XMLParser()
    doc_p.parse(xml_path)
    print(doc_p.text)
    print(doc_p.microbes)

    with open("../txt/microbes.txt", "w") as f:
        for x in doc_p.microbes:
            print(x, file=f)
    with open("../txt/pages.txt", "w") as f:
        print(doc_p.text, file=f)