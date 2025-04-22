from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

# Secret token for authentication
SECRET_TOKEN = "K7cEjvvx4D"

# URL to scrape
BASE_URL = "https://www.timeanddate.com"
URL = f"{BASE_URL}/worldclock/?low=c&sort=1"

@app.route("/api/time", methods=["GET"])
def get_city_time():
    # Verify token
    token = request.headers.get("Authorization")
    if token != f"Bearer {SECRET_TOKEN}":
        return jsonify({"error": "Unauthorized"}), 401

    # Get city
    city = request.args.get("city", "").strip().lower()
    if not city:
        return jsonify({"error": "City parameter is required"}), 400

    # Scrape main page
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"class": "zebra fw tb-theme"})
    if not table:
        return jsonify({"error": "Could not locate city time table."}), 500

    # Search for city
    for row in table.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) >= 2:
            city_link = cells[0].find("a")
            if city_link and city in city_link.text.strip().lower():
                local_time = cells[1].text.strip()
                detail_url = BASE_URL + city_link["href"]

                # Get UTC offset
                utc_offset = "N/A"
                detail_response = requests.get(detail_url)
                detail_soup = BeautifulSoup(detail_response.text, "html.parser")
                offset_text = detail_soup.find(string=re.compile(r"UTC/GMT [+-]\d{1,2}(?::\d{2})? hour"))
                if offset_text:
                    match = re.search(r"UTC/GMT ([+-]\d{1,2}(?::\d{2})?) hour", offset_text)
                    if match:
                        utc_offset = f"UTC{match.group(1)}"

                return jsonify({
                    "city": city.title(),
                    "local_time": local_time,
                    "utc_offset": utc_offset
                })

    return jsonify({"error": f"City '{city}' not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)