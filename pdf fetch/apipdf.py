from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Replace with your Google Books API key
api_key = 'your api here'

def fetch_pdfs_from_google_books(query, max_results=10):
    url = "https://www.googleapis.com/books/v1/volumes"
    params = {
        'q': query,
        'maxResults': max_results,
        'printType': 'books',
        'projection': 'full',
        'key': api_key
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        results = response.json().get('items', [])
        pdfs = []
        for item in results:
            access_info = item.get('accessInfo', {})
            if access_info.get('pdf', {}).get('isAvailable'):
                pdf_link = access_info.get('pdf', {}).get('downloadLink')
                if pdf_link:
                    pdf_data = {
                        'title': item['volumeInfo'].get('title', 'No Title'),
                        'authors': item['volumeInfo'].get('authors', []),
                        'pdf_link': pdf_link
                    }
                    pdfs.append(pdf_data)
        return pdfs
    else:
        response.raise_for_status()

@app.route('/', methods=['GET', 'POST'])
def index():
    pdfs = []
    if request.method == 'POST':
        query = request.form['query']
        pdfs = fetch_pdfs_from_google_books(query)
    return render_template('showpdf.html', pdfs=pdfs)

if __name__ == '__main__':
    app.run(debug=True)
