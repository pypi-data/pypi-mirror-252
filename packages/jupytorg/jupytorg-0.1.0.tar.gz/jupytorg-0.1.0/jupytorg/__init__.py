import json
import subprocess
import sys
import os
from pathlib import Path

import bs4

def usage() -> str:
    return ("Usage : jupytorg src=input_file_path (optional type=code_block_language dest=output_file_path)\n"
        + "    input_file_path : the path to input the file\n"
        + "    code_block_language : le language des blocks de code (default is C)\n"
        + "    output_file_path : the path to output the file (default is output_file.ipynb)")

def is_pandoc_installed() -> bool:
    try:
        subprocess.run(["pandoc", "--version"])
        return True
    except FileNotFoundError:
        return False

def main():
    nom_fichier_in: str
    nom_fichier_out = "output_file.ipynb"
    type_code = "C"
    fichier_in = None

    # analyse de l'entrée en commande
    if len(sys.argv) <= 1:
        print(usage())
        return
    else:
        for i in sys.argv:
            if i == "--help":
                print(usage())
                return
            arg = i.split("=")
            match arg[0]:
                case "src":
                    nom_fichier_in = arg[1].replace('~', str(Path.home()))
                case "type":
                    type_code = arg[1].replace('~', str(Path.home()))
                case "dest":
                    nom_fichier_out = arg[1].replace('~', str(Path.home()))
                case _:
                    SystemExit("unknown argument : " + i)
    if not is_pandoc_installed():
        raise SystemExit("Install pandoc to use this script")
    try:
        subprocess.run(["pandoc", nom_fichier_in, "-o", "out.html"])
    except FileNotFoundError:
        raise SystemExit("input file not found : " + nom_fichier_in)

    html = Path("out.html").read_text()
    # comment this line to keep the html file
    os.remove("out.html")

    document = bs4.BeautifulSoup(html, features="html.parser")

    cells = []
    flags = f""

    # Convert to ipynb
    for node in document.find_all(recursive=False):
        # si on trouve un block de code 
        if node.attrs.get("class", [""])[0] == "sourceCode":
            imports = ""
            encapslation_start = ""
            encapslation_end = ""
            flags = f""
            if node.attrs.get("data-results", [""]) == "file":
                # texte correspondant à une image en markdown
                texte = "!["+str(node.attrs.get("data-file", [""]))+"]("+str(node.attrs.get("data-file", [""]))+")"
                cells.append(
                    {
                        "cell_type": "code",
                        "source": [flags+node.get_text()],
                        "execution_count": 0,
                        "outputs": [],
                        "metadata": {
                            "vscode": {
                                "languageId": str(node.attrs.get("data-org-language", [""]))
                            }
                        }
                    }
                )
                cells.append({"cell_type": "markdown", "source": [texte], "metadata": {}})
            else:
                code_modified = node.get_text()
                if node.attrs.get("data-includes", [""]) != [''] and node.attrs.get("data-org-language", [""]) == 'C':
                    # imports déjà spécifiés
                    imports += "".join(list(map(lambda dep: "#include "+dep+"\n", (node.attrs.get("data-includes", [""])).split()))) + "\n"
                if node.attrs.get("data-org-language", [""]) == 'C':
                    # for example, to use OpenMP pragmas:
                    flags += "//%cflags:-fopenmp\n"
                    # prcq le prof c'est vrmt un connard d'utiliser emacs
                    imports += "#include <omp.h>\n#include <stdio.h>\n#include <stdlib.h>\n\n"
                    encapslation_start = "int main(int argc, char* argv[]){"
                    code_modified = '\t'.join(('\n'+code_modified.lstrip()).splitlines(True))
                    encapslation_end = "\n}"
                cells.append(
                    {
                        "cell_type": "code",
                        "source": [flags+imports+encapslation_start+code_modified+encapslation_end],
                        "execution_count": 0,
                        "outputs": [],
                        "metadata": {}
                    }
                )
        # si on trouve une image
        elif node.img:
            cells.append({"cell_type": "markdown", "source": [str(node.img)], "metadata": {}})
        # si on trouve un exemple (équivalent à un code)
        elif node.attrs.get("class", [""])[0] == "example":
            cells.append({"cell_type": "code", "source": [(node.get_text()).rstrip()], "metadata": {}})
        # si on trouve un plot, actuellement on prie pour une image déjà compilée
        elif node.attrs.get("class", [""])[0] == "gnuplot":
            texte = "!["+str(node.attrs.get("data-file", [""]))+"]("+str(node.attrs.get("data-file", [""]))+")"
            cells.append({"cell_type": "markdown", "source": [texte], "metadata": {}})
        # sinon c'est juste du texte
        else:
            cells.append({"cell_type": "markdown", "source": [str(node)], "metadata": {}})

    # écriture dans le fichier de sortie
    fichier_out = open(nom_fichier_out, "w")
    fichier_out.write(
        json.dumps(
            {
                "cells": cells,
                "metadata": {
                    "kernelspec": {
                        # C language kernelspec with OpenMP support
                        "display_name": "C",
                        "language": "c",
                        "name": "c",
                    },
                    "language_info": {
                        "file_extension": ".c",
                        "name": "c",
                        "mimetype": "text/plain",
                    },
                },
                "nbformat": 4,
                "nbformat_minor": 4,
            }
        )
    )

if __name__ == '__main__':
    main()
