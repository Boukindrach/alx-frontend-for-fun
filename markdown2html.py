#!/usr/bin/python3
""" A script markdown2html.py """


import sys
import os.path
import re
import hashlib

def convert_md5(line):
    md5 = re.findall(r'\[\[(.+?)\]\]', line)
    for match in md5:
        hashed = hashlib.md5(match.encode()).hexdigest()
        line = line.replace(f'[[{match}]]', hashed)
    return line

def remove_c(line):
    matches = re.findall(r'\(\((.+?)\)\)', line)
    for match in matches:
        removed_c = ''.join(c for c in match if c not in 'Cc')
        line = line.replace(f'(({match}))', removed_c)
    return line

def process_headings(line):
    heading_level = len(line) - len(line.lstrip('#'))
    if 1 <= heading_level <= 6:
        content = line.strip('#').strip()
        return f'<h{heading_level}>{content}</h{heading_level}>\n'
    return line

def process_lists(line, html, list_state):
    unordered = line.startswith('- ')
    ordered = line.startswith('* ')

    if unordered or ordered:
        tag = 'ul' if unordered else 'ol'
        if not list_state[tag]:
            html.write(f'<{tag}>\n')
            list_state[tag] = True
        content = line[2:].strip()
        html.write(f'<li>{content}</li>\n')
    elif list_state['ul'] or list_state['ol']:
        for tag in ['ul', 'ol']:
            if list_state[tag]:
                html.write(f'</{tag}>\n')
                list_state[tag] = False
    return list_state

def process_paragraph(line, html, in_paragraph):
    if line.strip():
        if not in_paragraph:
            html.write('<p>\n')
            in_paragraph = True
        elif in_paragraph:
            html.write('<br/>\n')
        html.write(line)
    elif in_paragraph:
        html.write('</p>\n')
        in_paragraph = False
    return in_paragraph

def convert_markdown_to_html(input_file, output_file):
    with open(input_file, 'r') as md_file, open(output_file, 'w') as html_file:
        list_state = {'ul': False, 'ol': False}
        in_paragraph = False

        for line in md_file:
            line = line.replace('**', '<b>', 1).replace('**', '</b>', 1)
            line = line.replace('__', '<em>', 1).replace('__', '</em>', 1)
            line = convert_md5(line)
            line = remove_c(line)
            line = process_headings(line)
            
            list_state = process_lists(line, html_file, list_state)
            
            if not any(list_state.values()):
                in_paragraph = process_paragraph(line, html_file, in_paragraph)

        # Close any open tags
        for tag in ['ul', 'ol']:
            if list_state[tag]:
                html_file.write(f'</{tag}>\n')
        if in_paragraph:
            html_file.write('</p>\n')

def main():
    if len(sys.argv) < 3:
        print('Usage: ./markdown2html.py README.md README.html', file=sys.stderr)
        sys.exit(1)

    input_file, output_file = sys.argv[1], sys.argv[2]

    if not os.path.isfile(input_file):
        print(f'Missing {input_file}', file=sys.stderr)
        sys.exit(1)

    convert_markdown_to_html(input_file, output_file)

if __name__ == '__main__':
    main()
