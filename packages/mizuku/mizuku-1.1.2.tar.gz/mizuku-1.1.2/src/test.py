from mizuku.mizu import mizu

tests = {
    "- Bullet Point":
        "<ul><li>Bullet Point</li></ul>",

    "- Bullet Point\n\n- Second Bullet Point":
        "<ul><li>Bullet Point</li><li>Second Bullet Point</li></ul>",

    "Look at some *strong text here*; voila!":
        "<p>Look at some <strong>strong text here</strong>; voila!</p>",

    "Testing {Text Here}. Testing.":
        "<p>Testing <a href='Text_Here.html'>Text Here</a>. Testing.</p>",

    "Testing {Text Here|https://example.com}. Testing.":
        "<p>Testing <a href='https://example.com'>Text Here</a>. Testing.</p>",

    "Testing {Text Here|some_file.html}. Testing.":
        "<p>Testing <a href='some_file.html'>Text Here</a>. Testing.</p>",

    "At any location in a paragraph, just do this: [FileNameGoesHere.png].": 
        "<p>At any location in a paragraph, just do this: <img src='FileNameGoesHere.png'>.</p>",

    "[Any text here]": "<div class='Any'>Any text here</div>",
    "[center: Any text here]": "<div class='center'>Any text here</div>",
    "    <escaped code here>\n    <more>\n": "<pre>&lt;escaped code here&gt;\n&lt;more&gt;</pre>",
}

for key in tests:
    actual = mizu("example.com", key)
    expected = tests[key]
    key = key.replace("\n", "\\n")
    actual = actual.replace("\n", "\\n")
    expected = expected.replace("\n", "\\n")
    if actual != expected:
        print(f'[-] "{key}" failed, got {actual} instead of {expected}')
        exit(1)
    print(f'[+] "{key}" passed, got {actual}')

print("[+] All tests passed!")
