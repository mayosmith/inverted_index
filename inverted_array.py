from collections import defaultdict
import os
import re

# Initialize empty array for JavaScript output
js_array = []

def strip_html_tags(html):
    # Remove script and style elements
    html = re.sub(r'<script.*?</script>', '', html, flags=re.DOTALL)
    html = re.sub(r'<style.*?</style>', '', html, flags=re.DOTALL)
    
    # Extract alt text from img tags
    html = re.sub(r'<img[^>]*alt="([^"]*)"[^>]*>', r'\1', html)
    
    # Remove remaining HTML tags
    html = re.sub(r'<[^>]+>', ' ', html)
    
    # Remove extra whitespace
    text = ' '.join(html.split())
    
    return text

# Function to build documents from HTML files
def build_documents():
    documents = {}
    for i in range(1, 25):
        filename = f"rp-{i}.html"
        
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                html_content = file.read()
                text = strip_html_tags(html_content)
                documents[filename] = text  # Use filename as key and stripped text as value
                
        except FileNotFoundError:
            print(f"Warning: {filename} not found")
    
    return documents

# Replace hardcoded documents with the function call
documents = build_documents()

# Building the inverted index
inverted_index = defaultdict(list)
for doc_id, text in documents.items():
    for word in re.sub(r'[^\w\s]', '', text.lower()).split():
        if doc_id not in inverted_index[word]:
            inverted_index[word].append(doc_id)
            # Save inverted index to JS file
            with open('js/inverted_index.js', 'w', encoding='utf-8') as f:
                f.write('const invertedIndex = ' + str(dict(inverted_index)).replace("'", '"') + ';')

# Function to search for documents containing all words in query
def search(query, index):
    words = query.lower().split()
    result = set(index[words[0]])  # Start with the first word's document list
    for word in words[1:]:
        result.intersection_update(index[word])  # Intersect with next word's document list
    return result

# Example search query
query = input("Enter search terms: ")
print("Documents containing '{}':".format(query), search(query, inverted_index))

# Write JavaScript array to file
with open('js/rpfetch-inv.js', 'w', encoding='utf-8') as outfile:
    outfile.write('const rpFetch = [\n')
    
    # Write each row as [text, filename]
    for row in js_array:
        text = row[0].replace('"', '\\"')  # Escape quotes in text
        outfile.write(f'  ["{text}", "{row[1]}"],\n')
        
    outfile.write('];')
