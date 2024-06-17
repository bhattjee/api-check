from flask import Flask, render_template, request
import freesound

# Replace with your Freesound Client ID and Secret
CLIENT_ID = "YOUR_FREESOUND_CLIENT_ID"
CLIENT_SECRET = "YOUR_FREESOUND_CLIENT_SECRET"

app = Flask(__name__)

@app.route('/')
def search_sounds():
  return render_template("search.html")

@app.route('/results', methods=['POST'])
def show_results():
  search_term = request.form['search_term']

  # Use OAuth to get an access token (replace with redirect URI)
  oauth = freesound.OAuth2(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri="	https://freesound.org/home/app_permissions/permission_granted/")
  access_token = oauth.token  # Replace with actual token retrieval process (see documentation)

  # Create a Freesound client with the access token
  client = freesound.Freesound(access_token=access_token)

  try:
    # Search for sounds using the search term
    sounds = client.search(query=search_term, filter="text", sort="downloads", duration="all")
  except freesound.FreesoundException as e:
    error_message = f"Error fetching sounds: {str(e)}"
    return render_template("results.html", error=error_message)

  return render_template("results.html", sounds=sounds)

if __name__ == '__main__':
  app.run(debug=True)
