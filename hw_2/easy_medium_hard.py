from pdflatex import PDFLaTeX
from generate_ast_package.generate_ast import plot_and_save_ast


def create_latex_document(body):
    first_line = r"\documentclass{article}" + "\n"
    graphics_lib = r"\usepackage{graphicx}" + "\n"
    second_line = r"\begin{document}" + "\n"
    end_line = r"\end{document}" + "\n"
    return first_line + graphics_lib + second_line + body + end_line


def generate_table_from_list(table: list[list]) -> str:
    n_columns = len(table[0])
    first_line = r"\begin{tabular}" + r"{ |" + "c|" * n_columns + r" }" + "\n" + "\hline \n"

    inside_table = f" \\\\ \n".join(list(map(lambda line: " & ".join(line), table))) + " \\\\ \n" + "\hline \n"

    last_line = r"\end{tabular}"
    return first_line + inside_table + last_line + "\n"


def generate_image(image_path):
    first_line = r"\begin{figure}[h]" + "\n"
    res = f"\\includegraphics[width=10cm, height=8cm]" + "{" + image_path + "}" + "\n"
    last_line = r"\end{figure}" + "\n"
    return first_line + res + last_line


def f(x):
    return x + 2


if __name__ == "__main__":
    table = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9'], ['10', '11', '12']]
    body = generate_table_from_list(table)

    image_path = "ast_new.jpg"
    plot_and_save_ast(f, image_path)

    body += generate_image(image_path)
    doc = create_latex_document(body)
    with open("table_image.tex", "w+") as tablefile:
        tablefile.write(doc)

    pdfl = PDFLaTeX.from_texfile('table_image.tex')
    pdf, log, completed_process = pdfl.create_pdf(keep_pdf_file=True, keep_log_file=False)
