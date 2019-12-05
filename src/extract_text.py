from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage, PDFTextExtractionNotAllowed
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from io import StringIO
from tqdm import tqdm
import json
import argparse
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", type=str)
    parser.add_argument("--output", "-o", type=str, default="./")
    args = parser.parse_args()

    input_path = args.input
    file_name = os.path.basename(input_path)
    output_path = os.path.join(args.output, file_name.replace("pdf", "json"))

    password = "0000"
    laparams = LAParams()
    laparams.detect_vertical = True
    manager = PDFResourceManager()
    outfp = StringIO()
    device = TextConverter(manager, outfp=outfp, codec='utf-8', laparams=laparams)
    interpreter = PDFPageInterpreter(manager, device)

    str_dict = {}
    head_idx = 0

    with open(output_path, "w") as f_out:
        with open(input_path, "rb") as f_in:
            pdf_parser = PDFParser(f_in)
            document = PDFDocument(pdf_parser, password)
            if not document.is_extractable:
                raise PDFTextExtractionNotAllowed
            for i, page in enumerate(tqdm(PDFPage.create_pages(document))):
                interpreter.process_page(page)
                str_dict[i+575] = outfp.getvalue()[head_idx:]
                head_idx = len(outfp.getvalue())
        json.dump(str_dict, f_out)