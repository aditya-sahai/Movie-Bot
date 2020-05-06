from bs4 import BeautifulSoup
import requests


class Data:
    """A class for reading and updating the csv file."""
    def __init__(self):
        """Initialize values."""
        self.file_name = "movies-data.csv"
        self.URL = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"

    def restore_data(self):
        """Updates the movies in the csv file and deletes old data."""
        response = requests.get(self.URL)
        # print(response.status_code)

        self.table_soup = BeautifulSoup(response.content, "html.parser").find(class_="lister-list")
        self.rows = self.table_soup.find_all("tr")

        self.file = open(self.file_name, "w")

        for self.row in self.rows:
            serial_num = self.row.find(class_="titleColumn").get_text().split()[0][0:-1]
            name = self.row.find(class_="titleColumn").a.get_text().strip().replace(",", "_")
            link = f"https://www.imdb.com/{self.row.a['href']}"
            movie_release_year = self.row.find(class_="titleColumn").get_text().split()[-1][1:-1]
            rating = self.row.find(class_="ratingColumn imdbRating").get_text().strip()

            line = f'"{serial_num}","{name}","{link}","{movie_release_year}","{rating}"\n'
            self.file.write(line)

        self.file.close()

    def give_movie_info(self, search_word):
        """Reads the file and gives the user basic data."""
        self.file = open(self.file_name, "r")

        lines = self.file.readlines()

        for line in lines:
            line = line.split(",")
            name = line[1][1:-1].lower().strip()

            if search_word.lower().strip() == name:
                serial_num = line[0][1:-1].strip()
                release_year = line[3][1:-1].strip()
                rating = line[4][1:-2].strip()
                return serial_num, release_year, rating

        return False

        self.file.close()

if __name__ == "__main__":
    obj = Data()
    # obj.restore_data()

    movie = input("Enter any movie: ")
    info = obj.give_movie_info(movie)

    if info:
        print(f"Rank: {info[0]}")
        print(f"Movie Release Year : {info[1]}")
        print(f"Rating: {info[2]}")
