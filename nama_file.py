import requests

ACCESS_KEY = 'ygDEXtjNxxlLWToH51EHCslSQpLvLlAlU1HKH1n4rvY'

def search_unsplash(query, per_page=5):
    url = "https://api.unsplash.com/search/photos"
    headers = {
        "Authorization": f"Client-ID {ACCESS_KEY}"
    }
    params = {
        "query": query,
        "per_page": per_page
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        for i, photo in enumerate(data['results']):
            description = photo['description'] or photo['alt_description'] or "No description"
            image_url = photo['urls']['regular']
            photographer = photo['user']['name']

            print(f"{i+1}. {description}")
            print(f"   URL: {image_url}")
            print(f"   Photographer: {photographer}\n")

            # Simpan gambar otomatis
            download_image(image_url, f"image_{i+1}.jpg")
    else:
        print(f"Error: {response.status_code} - {response.text}")

def download_image(url, filename):
    img_data = requests.get(url).content
    with open(filename, 'wb') as handler:
        handler.write(img_data)
    print(f"[✓] Gambar tersimpan: {filename}")

if __name__ == "__main__":
    keyword = input("Search keyword: ")
    search_unsplash(keyword)

