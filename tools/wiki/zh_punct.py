"""Full-width punctuation for Simplified Chinese wiki pages, outside code and links.

    python3 tools/wiki/zh_punct.py docs/**/*.zh.md
"""
import re
import sys

CJK = r'[㐀-鿿　-〿＀-￯]'
SKIP = re.compile(r'(```.*?```|`[^`\n]*`|\]\([^)]*\)|<[^>\n]*>|\{[^}\n]*\}|https?://\S+)', re.S)


def fix(text):
    out = []
    for i, part in enumerate(SKIP.split(text)):
        if i % 2:
            out.append(part); continue
        part = re.sub(rf'(?<={CJK}),\s*', '，', part)
        part = re.sub(rf'(?<=[^\d\s]),(?={CJK})', '，', part)
        part = re.sub(rf'(?<={CJK});\s*', '；', part)
        part = re.sub(rf'(?<={CJK}):\s*', '：', part)
        part = re.sub(rf'(?<={CJK})\.(?=\s|$)', '。', part, flags=re.M)
        part = re.sub(rf'\(([^()\n]*{CJK}[^()\n]*)\)', r'（\1）', part)
        part = re.sub(rf'(?<={CJK})\s*\(([^()\n]*)\)', r'（\1）', part)
        part = re.sub(r'(?<=[）】」]),\s*', '，', part)
        out.append(part)
    return ''.join(out)


if __name__ == '__main__':
    for path in sys.argv[1:]:
        src = open(path, encoding='utf-8').read()
        dst = fix(src)
        if dst != src: open(path, 'w', encoding='utf-8').write(dst)
