# 导入模块
import os
import platform
from .readlinux import read_docx, read_pdf, read_txt,convert_doc_to_docx,convert_doc_to_docx_win

# 导出函数
def parse_file(file_path, output_directory):
    _, file_extension = os.path.splitext(file_path)
    file_content = ""

    if file_extension.lower() == '.doc':
        docx_path = convert_doc_to_docx_win(file_path, output_directory) if platform.system() == 'Windows' else convert_doc_to_docx(file_path, output_directory)
        if docx_path:
            file_content = read_docx(docx_path)
            output_path = os.path.join(output_directory, f"{os.path.basename(file_path)[:-4]}.txt")
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
        output_path = os.path.join(output_directory, f"{os.path.basename(file_path)[:-4]}.txt")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(file_content)
        print(f"Output saved to {output_path}")
