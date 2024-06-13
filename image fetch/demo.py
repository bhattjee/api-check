from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Access key for Unsplash API
access_key = 'your access key'

def fetch_images_from_unsplash(query, per_page=5):
    url = f"https://api.unsplash.com/search/photos"
    
    params = {
        'query': query,
        'per_page': per_page,
        'client_id': access_key
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()['results']
    else:
        response.raise_for_status()

@app.route('/', methods=['GET', 'POST'])
def index():
    images = []
    if request.method == 'POST':
        query = request.form['query']
        images = fetch_images_from_unsplash(query)
    return render_template('show.html', images=images)

if __name__ == '__main__':
    app.run(debug=True)
