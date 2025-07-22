import os
import re
from bs4 import BeautifulSoup

def extract_comments_from_html(file_path):
    """Extract all comment texts from HTML file with the pattern:
    <span data-v-aed4aacc="" class="note-text"><span>COMMENT_TEXT</span></span>
    """
    # Read the HTML file
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
    except UnicodeDecodeError:
        # Try alternative encoding if UTF-8 fails
        with open(file_path, 'r', encoding='gbk') as file:
            html_content = file.read()
    
    # Method 1: Using BeautifulSoup (more robust)
    soup = BeautifulSoup(html_content, 'html.parser')
    comments = []
    
    # Find all spans with class="note-text"
    note_spans = soup.find_all('span', class_='note-text')
    for note_span in note_spans:
        # Find the inner span and get its text
        inner_span = note_span.find('span')
        if inner_span:
            comment_text = inner_span.get_text().strip()
            comments.append(comment_text)
    
    # Method 2: Using regex (faster but less robust)
    if not comments:  # If BeautifulSoup didn't find anything, try regex
        pattern = r'<span data-v-[^>]*? class="note-text"><span>(.*?)</span></span>'
        comments = re.findall(pattern, html_content)
    
    # Output results
    print(f"Found {len(comments)} comments:")
    for i, comment in enumerate(comments, 1):
        print(f"{i}. {comment}")
    
    # Save to output file
    with open(os.path.join(current_dir + "//md", "red_note_comments2.md"), "w", encoding="utf-8") as f:
        for i, comment in enumerate(comments, 1):
            f.write(f"{i}. {comment}" + '\n')
    
    return comments

if __name__ == "__main__":
    current_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_path)
 
    html_file = os.path.join(current_dir, "temp.html")
    extract_comments_from_html(html_file)
