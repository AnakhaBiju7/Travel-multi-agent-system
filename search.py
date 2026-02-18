import requests

def search_agent(city, memory, HOTEL_API_KEY):
    url = "https://api.hotels-api.com/v1/hotels/search"
    headers = {"X-API-KEY": HOTEL_API_KEY}
    params = {"city": city, "limit": 5}

    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    if not data.get("success"):
        print("API Error:", data)
        return []

    hotels = []
    for item in data.get("data", []):
        hotel = {
            "name": item.get("name", "Unknown"),
            "price": item.get("price", 0) or 0,
            "rating": item.get("rating", 0) or 0
        }
        if hotel["price"] == 0:
            hotel["price"] = memory["last_prices"].get(hotel["name"], int(100 + hotel["rating"]*80))
        hotels.append(hotel)
    return hotels
