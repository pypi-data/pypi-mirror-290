import requests
from bs4 import BeautifulSoup

def fetch_douban_top_movies(start_index, end_index):
    base_url = 'https://movie.douban.com/top250?start={}&filter='
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
    }
    movies_data = []

    for i in range(start_index, end_index + 1):
        url = base_url.format(i * 25)
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        movie_items = soup.find_all('div', class_='item')
        for item in movie_items:
            title = item.find('span', class_='title').text.strip()
            rating = item.find('span', class_='rating_num').text.strip()
            rating_num = item.find('div', class_='star').find_all('span')[-1].text.strip('人评价').strip()
            movies_data.append({
                'title': title,
                'rating': rating,
                'rating_num': rating_num
            })

    return movies_data


top_movies = fetch_douban_top_movies(0, 9)

for movie in top_movies[:5]:
    print(movie)