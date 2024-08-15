from re import search, match
from pathlib import Path
from html import escape

# Bold text like this:
#
# *Text Here*                      ---renders-to--> <strong>Text here</strong>
#
def convert_strong(paragraph):
    while match := search(r"\*(.*?)\*", paragraph):
        raw_text = match.group(1)
        a = match.start(0)
        b = match.end(0)
        strong = f"<strong>{raw_text}</strong>"
        paragraph = paragraph[:a] + strong + paragraph[b:]
    return paragraph


# Links appear in a paragraph with the following formats:
#
# {Text Here}.                     ---renders-to--> <a href="Text_Here.html">Text Here</a>.
# {Text Here|https://example.com}. ---renders-to--> <a href="https://example.com">Text Here</a>.
def convert_links(paragraph):
    while match := search(r"{(.*?)}", paragraph):
        raw_link = match.group(1)
        if "|" in raw_link:
            text, url = raw_link.split("|")
        else:
            text = raw_link 
            url = raw_link.replace(" ", "_") + ".html"
        a = match.start(0)
        b = match.end(0)
        anchor = f"<a href='{url}'>{text}</a>"
        paragraph = paragraph[:a] + anchor + paragraph[b:]
    return paragraph


# Images appear in a paragraph with the following format:
#
# Any location in the paragraph, [FileNameGoesHere.png].
#
# Tag must end in ".png]"
#
def convert_images(paragraph):
    while match := search(r"\[(.*?.png)\]", paragraph):
        raw_link = match.group(1)
        a = match.start(0)
        b = match.end(0)
        img = f"<img src='{raw_link}'>"
        paragraph = paragraph[:a] + img + paragraph[b:]
    return paragraph

# Divs use the following format:
#
# [Any text here]
#
# or
#
# [class: Any text here]
#
def convert_divs(paragraph):
    while match := search(r"\[(.*?)\]", paragraph):
        raw_text = match.group(1)
        div_class = raw_text.split()[0]
        a = match.start(0)
        b = match.end(0)
        if div_class.endswith(":"):
            div_class = div_class[:-1]
            raw_text = raw_text.split(":",1)[1].strip()
        div = f"<div class='{div_class}'>{raw_text}</div>"
        paragraph = paragraph[:a] + div + paragraph[b:]
    return paragraph


# Include code from another PWML file as thus:
#
# <filename.mizu>
#
def convert_includes(domain, paragraph):
    while match := search(r"<(.*?\.mizu)>", paragraph):
        a = match.start(0)
        b = match.end(0)
        with Path(match.group(1)).open("r") as f:
            html = mizu(domain, f.read())
        paragraph = paragraph[:a] + html + paragraph[b:]
    return paragraph

# Don't do this if we already start with a tag, excluding anchors and images.
def wrap_paragraph_in_p_tag(paragraph):
    paragraph = paragraph.strip()
    if not paragraph.startswith("<") or paragraph.startswith("<a ") or paragraph.startswith("<img"):
        paragraph = f"<p>{paragraph}</p>"
    return paragraph


def mizu(domain, mizu_content, css=""):
    output = ""
    inul = False
    if "----" in mizu_content:
        beginning, width_spec, middle, end = mizu_content.split("----")
        first, rest = beginning.split("\n", 1)
        if not first.startswith("# "):
            print("Missing title. Please refer to documentation.")
            exit(1)
        if width_spec != "full-width" and not match("\d+em", width_spec):
            print("Missing width spec. Please refer to documentation.")
            exit(1)
        TITLE = first[2:]
        WIDTH_CSS = "100%" if width_spec == "full-width" else width_spec
        NAVIGATION = mizu(domain, rest)
        CONTENT = mizu(domain, middle)
        FOOTER = mizu(domain, end)
        with open("base.html", "r") as f:
            output = f.read()
            output = output.replace("TITLE", TITLE)
            output = output.replace("NAVIGATION", NAVIGATION)
            output = output.replace("WIDTH_CSS", WIDTH_CSS)
            output = output.replace("CSS", css)
            output = output.replace("CONTENT", CONTENT)
            output = output.replace("FOOTER", FOOTER)
            output = output.replace("DOMAIN", domain)
    else:
        paragraphs = mizu_content.split("\n\n")
        for paragraph in paragraphs:
            if paragraph.startswith("    "):
                paragraph = paragraph.strip()
                paragraph = escape(paragraph.replace("\n    ", "\n"))
                output += f"<pre>{paragraph}</pre>"
            else:
                paragraph = paragraph.strip()
                paragraph = paragraph.replace("\n", " ")
                if paragraph:
                    paragraph = convert_strong(paragraph)
                    paragraph = convert_links(paragraph)
                    paragraph = convert_images(paragraph)
                    paragraph = convert_includes(domain, paragraph)
                    paragraph = convert_divs(paragraph)
                    if paragraph.startswith("- "):
                        if not inul:
                            inul = True
                            output += "<ul>"
                        output += "<li>"
                        output += paragraph[2:]
                        output += "</li>"
                    else:
                        if inul:
                            inul = False
                            output += "</ul>"
                        paragraph = wrap_paragraph_in_p_tag(paragraph)
                        output += paragraph
    if inul:
        inul = False
        output += "</ul>"
    return output
