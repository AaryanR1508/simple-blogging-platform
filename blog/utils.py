import markdown
from markdown.treeprocessors import Treeprocessor
from markdown.extensions import Extension
from html.parser import HTMLParser
import xml.etree.ElementTree as etree 

class ParagraphExtractor(Treeprocessor):
    def run(self, root):
        new_root = etree.Element("div")
        for element in root:
            if element.tag == 'p':
                new_root.append(element)
        return new_root

class ParagraphOnlyExtension(Extension):
    def extendMarkdown(self, md):
        md.treeprocessors.register(ParagraphExtractor(md), 'paragraph_extractor', 100)

class HTMLTextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.data = []
        self.in_p = False

    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            self.in_p = True

    def handle_endtag(self, tag):
        if tag == 'p':
            self.in_p = False

    def handle_data(self, data):
        if self.in_p:
            self.data.append(data)

    def get_text(self):
        return ''.join(self.data)


def get_markdown_paragraph_preview(markdown_text, length=300):
    if not markdown_text:
        return ""

    md_html_only_paragraphs = markdown.markdown(markdown_text, extensions=[ParagraphOnlyExtension()])

    parser = HTMLTextExtractor()
    parser.feed(md_html_only_paragraphs)
    plain_text_paragraphs = parser.get_text()

    if len(plain_text_paragraphs) > length:
        truncated = plain_text_paragraphs[:length]
        last_space = truncated.rfind(' ')
        if last_space != -1:
            return truncated[:last_space] + '...'
        else:
            return truncated + '...'
    return plain_text_paragraphs