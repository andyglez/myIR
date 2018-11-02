from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import io


def convert(file):
    text = ''
    if 'pdf' in file.name:
        text = convert_from_pdf(file)
    else:
        with io.open(file, 'r') as f:
            for line in f.readlines():
                text = text + line + ' '
    return text


def convert_from_pdf(file_path):
    manager = PDFResourceManager()
    output = io.StringIO()
    codec = 'utf-8'
    converter = TextConverter(manager, output, codec=codec, laparams=LAParams())

    interpreter = PDFPageInterpreter(manager, converter)
    pagenums = set()
    infile = open(file_path, 'rb')

    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)

    infile.close()
    converter.close()
    text = output.getvalue()
    output.close()

    assert isinstance(text, object)
    return str(text).replace('', '')
