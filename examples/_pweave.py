"""
Run all the example files and convert them to markdown files containing the output.

Uses `pweave`. It is not installed by default. To install:

    pip install pweave
"""

import pweave, datetime, glob, os


def publish_to_markdown(python_file: str, output_file: str):
    doc = pweave.Pweb(python_file, kernel="python3", doctype="markdown", output=output_file)

    doc.theme = "skeleton"  # The default option is skeleton , other options are pweave (the old theme), bootstrap , cerulean and journal. All look the same to me.

    doc.read()
    doc.run()
    doc.format()
    doc.formatted += f"\n---\nMarkdown generated automatically from [{python_file}]({python_file}) using [Pweave](http://mpastell.com/pweave) {pweave.__version__} on {datetime.date.today()}.\n"
    doc.write()


if __name__ == "__main__":
    for python_file in glob.glob("*.py"):
        print(python_file)
        if python_file != os.path.basename(__file__):
            output_file = python_file.replace(".py", ".md")
            publish_to_markdown(python_file, output_file)
    else:
        print(glob.glob("*.py"))
        
