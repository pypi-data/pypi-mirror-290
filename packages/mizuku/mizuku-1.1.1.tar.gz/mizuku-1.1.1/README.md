# Mizuku = 水区 = Water District

This is a Python package that provides the CLI script `mizu`, meaning "water".

It converts .mizu files to .html files.

## Installation

    pip install mizuku

## Usage

    mizu

## Documentation

`mizu` is designed to produce output for any number of domain names.

This is useful for A/B testing domain names for your product or website.

The domains are listed one per line in the DOMAINS file.

---

Running `mizu` will look for all .mizu files in the current directory, and convert them to .html files.

So, for example, `Resume.mizu` will be converted to `./example.com/Resume.html`.

If a corresponding CSS file is present (e.g. Resume.css), it's contents will be automatically loaded into the resulting HTML.

---

To wrap some text in `<strong>` tags:

    Look at some *strong text here*; voila!

---

To link to a URL:

    {Text Here}.
    {Text Here|https://example.com}.
    {Text Here|some_file.html}.

The first one will automatically link to `Text_Here.html`.

---

To include an image:

    At any location in a paragraph, just do this: [FileNameGoesHere.png].

Only PNG format is supported and the `.png` extension must be provided.

---

To wrap some text in a `<div>` use the following format:

    [Any text here]
    [center: Any text here]

In the first case, the class of the div will be "Any", and you can style it in the related CSS file.

In the second case, the class of the div will be "center" and the text "center" will not be rendered.

---

To include another mizu file:

    <filename.mizu>

---

To wrap some text in a paragraph tag:

    Here is some text.

    Make sure this text is surrounded by two newlines, before and after, and it
    will get surrounded by P tags.

    Here is some more text.

---

HTML is parsed normally and as expected:

    Some left-aligned text.

    <center>
        Some centered aligned text.
    </center>

---

Bullet points are supported:

    - This is rendered as a bullet point. Make sure to include a space between
      this and the next bullet point, otherwise they're considered the same
      paragraph.

    - Here is the second bullet point!
