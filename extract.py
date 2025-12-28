from lxml import etree

def extract_footnotes(input_path, output_path):
    with etree.xmlfile(output_path, encoding="utf-8") as xf:
        xf.write_declaration()
        with xf.element("footnotes"):
            for _, elem in etree.iterparse(
                input_path,
                events=("end",),
                tag="{*}footnote"
            ):
                xf.write(elem)
                elem.clear()
                while elem.getprevious() is not None:
                    del elem.getparent()[0]
