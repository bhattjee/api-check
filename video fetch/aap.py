from flask import Flask, render_template, request
import requests  # Library for making API requests

# Replace with your YouTube Data API key
api_key = 'AIzaSyAwrPvQKBXuJmq9NgKOLjCBYhpyxeOcnK8'

app = Flask(__name__)


def fetch_videos_from_youtube(query, api_key):
  """Fetches videos from YouTube using the Data API.

  Args:
      query: Search query for videos.
      api_key: Your YouTube Data API key.

  Returns:
      A list of dictionaries containing video information (title, thumbnail, etc.)
      or None if there's an error.
  """
  base_url = "https://www.googleapis.com/youtube/v3/search"
  params = {
      "part": "snippet",
      "q": query,
      "maxResults": 12,  # You can adjust the number of results
      "key": api_key
  }

  try:
    response = requests.get(base_url, params=params)
    response.raise_for_status()  # Raise exception for non-200 status codes

    data = response.json()
    videos = []
    for item in data["items"]:
      video_id = item["id"]["videoId"]
      title = item["snippet"]["title"]
      thumbnail_url = item["snippet"]["thumbnails"]["default"]["url"]
      videos.append({"title": title, "thumbnail": thumbnail_url, "video_id": video_id})
    return videos

  except requests.exceptions.RequestException as e:
    print(f"Error fetching videos: {e}")
    return None


@app.route('/', methods=['GET', 'POST'])
def index():
  videos = []
  if request.method == 'POST':
    query = request.form['query']
    videos = fetch_videos_from_youtube(query, api_key)

  return render_template('showvideos.html', videos=videos)


if __name__ == '__main__':
  app.run(debug=True)
