import requests
from bs4 import BeautifulSoup

class DoubanTopMovies:
    def __init__(self):
        self.base_url = 'https://movie.douban.com/top250?start={}&filter='
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
        }

    def fetch_movies(self, start_index, end_index):
        movies_data = []

        for i in range(start_index, end_index + 1):
            url = self.base_url.format(i * 25)
            response = requests.get(url, headers=self.headers)
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

#if __name__ == "__main__":
#    fetcher = DoubanTopMovies()
#    top_movies = fetcher.fetch_movies(0, 1)  
#    print(top_movies)