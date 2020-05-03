from bs4 import BeautifulSoup
import requests


class Data:
    """A class for reading and updating the csv file."""
    def __init__(self):
        """Initialize values."""
        self.file_name = "movies-data.csv"
        self.file = open(self.file_name, "a+")
        self.URL = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"

    def update_data(self):
        """Updates the movies in the csv file."""
        response = requests.get(self.URL)
        # print(response.status_code)

        self.table_soup = BeautifulSoup(response.content, "html.parser").find(class_="lister-list")
        self.rows = self.table_soup.find_all("tr")
        self.file.truncate()

        for self.row in self.rows:
            serial_num = self.row.find(class_="titleColumn").get_text().split()[0][0:-1]
            name = self.row.find(class_="titleColumn").a.get_text().strip()
            link = f"https://www.imdb.com/{self.row.a['href']}"
            movie_release_year = self.row.find(class_="titleColumn").get_text().split()[-1][1:-1]
            rating = self.row.find(class_="ratingColumn imdbRating").get_text().strip()

            line = f'"{serial_num}","{name}","{link}","{movie_release_year}","{rating}"\n'
            self.file.write(line)

    def close_file(self):
        """Close the csv file and saves the data."""
        self.file.close()


if __name__ == "__main__":
    obj = Data()
    obj.update_data()
    obj.close_file()
