creates inverted index for html files and performs a query

How to run this experiment:

STEP 1: Copy 'inverted_array.py' into a root folder (example "mytestfolder")

STEP 2: Create two subdirectories: '/docs' and '/js'

STEP 3: Drop a bunch of .html files in the /docs sub-directory

STEP 4: run program in terminal (python3 inverted_array.py)

(You can see the newly created index in the /js directory)

================================================

To make this work with PDF files...

def build_documents():

    documents = {}

    for filename in os.listdir('docs'):
    
        if filename.endswith('.html') or filename.endswith('.pdf'):  # Check for PDF files
        
            try:
            
                if filename.endswith('.html'):
                
                    with open(os.path.join('docs', filename), 'r', encoding='utf-8') as file:
                    
                        html_content = file.read()
                   
                    text = strip_html_tags(html_content)
                
                elif filename.endswith('.pdf'):
                
                    from PyPDF2 import PdfReader  # Import PdfReader for PDF parsing
                    
                    with open(os.path.join('docs', filename), 'rb') as file:
                    
                        reader = PdfReader(file)
                        
                        text = ''
                        
                        for page in reader.pages:
                        
                            text += page.extract_text()  # Extract text from each page
                
                documents[filename] = text  # Use filename as key and stripped text as value
                
            except FileNotFoundError:
            
                print(f"Warning: {os.path.join('docs', filename)} not found")
    
    return documents
