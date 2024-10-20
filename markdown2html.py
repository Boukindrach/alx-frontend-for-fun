#!/usr/bin/env python3
import sys
import os
import re
import hashlib

def convert_markdown_to_html(markdown_content):
    # Convert headings
    for i in range(6, 0, -1):
        pattern = r'^{} (.+)$'.format('#' * i)
        replacement = r'<h{0}>\1</h{0}>'.format(i)
        markdown_content = re.sub(pattern, replacement, markdown_content, flags=re.MULTILINE)
    
    # Convert unordered lists
    unordered_list_pattern = r'((?:^- .+\n?)+)'
    markdown_content = re.sub(unordered_list_pattern, convert_unordered_list, markdown_content, flags=re.MULTILINE)
    
    # Convert ordered lists
    ordered_list_pattern = r'((?:^\* .+\n?)+)'
    markdown_content = re.sub(ordered_list_pattern, convert_ordered_list, markdown_content, flags=re.MULTILINE)
    
    # Convert paragraphs
    paragraph_pattern = r'(?:\A|\n\n)((?:.+\n?)+?)(?=\n\n|\Z)'
    markdown_content = re.sub(paragraph_pattern, convert_paragraph, markdown_content, flags=re.DOTALL)
    
    # Convert bold text
    bold_pattern = r'\*\*(.*?)\*\*'
    markdown_content = re.sub(bold_pattern, r'<b>\1</b>', markdown_content)
    
    # Convert emphasis (italic) text
    emphasis_pattern = r'__(.*?)__'
    markdown_content = re.sub(emphasis_pattern, r'<em>\1</em>', markdown_content)
    
    # Convert [[]] to MD5
    md5_pattern = r'\[\[(.*?)\]\]'
    markdown_content = re.sub(md5_pattern, convert_to_md5, markdown_content)
    
    # Convert (()) with character removal
    remove_c_pattern = r'\(\((.*?)\)\)'
    markdown_content = re.sub(remove_c_pattern, remove_c, markdown_content)
    
    return markdown_content

def convert_unordered_list(match):
    items = match.group(1).split('\n')
    html_items = ['<li>{}</li>'.format(item[2:].strip()) for item in items if item.strip()]
    return '<ul>\n    {}\n</ul>'.format('\n    '.join(html_items))

def convert_ordered_list(match):
    items = match.group(1).split('\n')
    html_items = ['<li>{}</li>'.format(item[2:].strip()) for item in items if item.strip()]
    return '<ol>\n    {}\n</ol>'.format('\n    '.join(html_items))

def convert_paragraph(match):
    lines = match.group(1).split('\n')
    formatted_lines = [lines[0]] + [f'    <br />\n{line}' for line in lines[1:]]
    return '<p>\n{}\n</p>'.format('\n'.join(formatted_lines))

def convert_to_md5(match):
    content = match.group(1)
    return hashlib.md5(content.encode()).hexdigest()

def remove_c(match):
    content = match.group(1)
    return re.sub(r'[cC]', '', content)

def main():
    # Check if the correct number of arguments is provided
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        sys.exit(1)

    # Get the input and output file names
    markdown_file = sys.argv[1]
    html_file = sys.argv[2]

    # Check if the Markdown file exists
    if not os.path.exists(markdown_file):
        sys.stderr.write(f"Missing {markdown_file}\n")
        sys.exit(1)

    # Read the content of the Markdown file
    with open(markdown_file, 'r') as f:
        markdown_content = f.read()

    # Convert Markdown to HTML
    html_content = convert_markdown_to_html(markdown_content)

    # Write the HTML content to the output file
    with open(html_file, 'w') as f:
        f.write(html_content)

    # Exit successfully
    sys.exit(0)

if __name__ == "__main__":
    main()
