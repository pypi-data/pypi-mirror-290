import os
import subprocess
import platform
from docx import Document
# from PyPDF2 import PdfFileReader
from langchain.document_loaders import PyPDFLoader
# Linux系统下将DOC转换为DOCX
def convert_doc_to_docx(doc_path, output_directory):
    # 获取文件名
    base_filename, _ = os.path.splitext(os.path.basename(doc_path))

    # 构建输出文件路径
    docx_path = os.path.join(output_directory, f"{base_filename}.docx")

    # 使用 libreoffice 命令行工具进行转换
    command = [
        'libreoffice',
        '--convert-to',
        'docx',
        '--headless',
        '--outdir',
        output_directory,
        doc_path
    ]

    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(result.stdout)
        print(f"Conversion successful: {docx_path}")
    except subprocess.CalledProcessError as e:
        print(f"Conversion failed: {e.stderr}")

    return docx_path

# 封装Windows特有代码
def convert_doc_to_docx_win(doc_path, output_directory):
    if platform.system() == 'Windows':
        try:
            from comtypes.client import CreateObject
            base_filename, _ = os.path.splitext(os.path.basename(doc_path))
            docx_path = os.path.join(output_directory, f"{base_filename}.docx")
            word = CreateObject('Word.Application')
            doc = word.Documents.Open(doc_path)
            doc.SaveAs(docx_path, FileFormat=16)  # 16 for docx
            doc.Close()
            word.Quit()
            return docx_path
        except ImportError:
            raise Exception("comtypes.client is not available on this platform.")
    else:
        return None

# 解析DOCX文件
def read_docx(docx_path):
    doc = Document(docx_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

# 解析PDF文件
def read_pdf(pdf_path):
    loader = PyPDFLoader(pdf_path)
    pages = loader.load_and_split()
    return ''.join([page.page_content for page in pages])



# 解析TXT文件
def read_txt(txt_path):
    with open(txt_path, 'r', encoding='utf-8') as f:
        return f.read()

# 主函数
def parse_file(file_path, output_directory):
    _, file_extension = os.path.splitext(file_path)
    file_content = ""

    if file_extension.lower() == '.doc':
        docx_path = convert_doc_to_docx_win(file_path, output_directory) if platform.system() == 'Windows' else convert_doc_to_docx(file_path, output_directory)
        if docx_path:
            file_content = read_docx(docx_path)
            base_filename, _ = os.path.splitext(os.path.basename(file_path))
            output_path = os.path.join(output_directory, f"{base_filename}.txt")
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(file_content)
            print(f"Output saved to {output_path}")
    elif file_extension.lower() in ['.docx', '.pdf', '.txt']:
        if file_extension.lower() == '.docx':
            file_content = read_docx(file_path)
        elif file_extension.lower() == '.pdf':
            file_content = read_pdf(file_path)
        elif file_extension.lower() == '.txt':
            file_content = read_txt(file_path)
        base_filename, _ = os.path.splitext(os.path.basename(file_path))
        output_path = os.path.join(output_directory, f"{base_filename}.txt")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(file_content)
        print(f"Output saved to {output_path}")

