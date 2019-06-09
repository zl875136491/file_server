import sys
import os
import comtypes.client


def d2p(doc_name, pdf_name):
    in_file = doc_name
    out_file = pdf_name
    word = comtypes.client.CreateObject('Word.Application')
    doc = word.Documents.Open(in_file)
    doc.SaveAs(out_file, FileFormat=17)
    doc.Close()
    word.Quit()


file_path = "D:\\project\\server\\media\\"
file_list = os.listdir(file_path)
for word_path in file_list:
    doc_name = file_path + word_path
    pdf_name = file_path + word_path.split(".")[0] + ".pdf"

    if not os.path.exists(pdf_name):
        d2p(doc_name, pdf_name)
