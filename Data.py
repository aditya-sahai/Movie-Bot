from bs4 import BeautifulSoup
import requests


class Data:
    """A class for reading and updating the csv file."""
    def __init__(self):
        """Initialize values."""
        self.file_name = "movies-data.csv"
        self.detailed_file_name = "movie-details.csv"
        self.URL = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"
        USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
        self.headers = {"user-agent" : USER_AGENT}

    def restore_data(self):
        """Updates the movies in the csv file and deletes old data."""
        response = requests.get(self.URL, headers=self.headers)
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

    def get_data_file_info(self, search_word):
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
                link = line[2][1:-1].strip()

                return {
                    "rank" : serial_num,
                    "release-year" : release_year,
                    "rating" : rating,
                    "link" : link,
                }

        return False

        self.file.close()

    def write_new_data(self, data_dict):
        """After getting the details from the web this function writes into a file 'movie-details.csv'"""

        self.detailed_file = open(self.detailed_file_name, "a")

        movie = data_dict["movie"].replace(",", "_")
        desc = data_dict["desc"].replace(",", "_")
        director = data_dict["dir"]
        writers = data_dict["writers"]
        actors = data_dict["actors"]

        line = f'"{movie.title()}","{desc}","{director}",'

        line += "\""
        for writer in writers:
            line += writer + '_'
        line = line[:-1]
        line += "\","

        line += "\""
        for actor in actors:
            line += actor + '_'
        line = line[:-1]
        line += "\"\n"

        self.detailed_file.write(line)
        self.detailed_file.close()

    def check_detailed_file(self, name):
        """Checks if the detailed file has a movie details."""

        self.detailed_file = open(self.detailed_file_name, "r")

        lines = self.detailed_file.readlines()
        self.detailed_file.close()

        name = name.lower().strip().replace(",", "_")
        for line in lines:

            line = line.split(",")
            line_movie = line[0].lower().strip().replace("\"", "")

            if name == line_movie:

                movie = line_movie.title()
                desc = line[1].replace("\"", "").replace("_", ",")
                director = line[2].replace("\"", "")
                writers = line[3].replace("\"", "").split("_")
                actors = line[4].replace("\"", "").split("_")

                return {
                    "movie" : movie,
                    "desc" : desc,
                    "dir" : director,
                    "writers" : writers,
                    "actors" : actors
                }
        return False

    def get_web_info(self, word):
        """Used when the user wants more information on a movie."""

        file_content = self.check_detailed_file(word)

        if file_content != False:
            return file_content

        url = self.get_data_file_info(word)
        if url != False:
            url = url["link"]
        else:
            return False

        response = requests.get(url, headers=self.headers)
        plot = BeautifulSoup(response.content, "html.parser").find(class_="plot_summary")

        desc = plot.find(class_="summary_text").get_text().strip()

        credit_box = plot.find_all(class_="credit_summary_item")
        director = credit_box[0].a.get_text()
        writers = credit_box[1].find_all("a")
        actors = credit_box[2].find_all("a")[:-1]

        for index, writer in enumerate(writers):
            writers[index] = writer.get_text()

        for index, actor in enumerate(actors):
            actors[index] = actor.get_text()


        data_dict = {
            "movie" : word,
            "desc" : desc,
            "dir" : director,
            "writers" : writers,
            "actors" : actors
        }

        self.write_new_data(data_dict)

        return data_dict


if __name__ == "__main__":
    obj = Data()

    # obj.restore_data()

    movie = input("Enter any movie: ")
    movie_info = obj.get_web_info(movie)

    if movie_info:

        print(movie_info["desc"])

        print(f"\nDirector:\n\t{movie_info['dir']}")

        print("Writers:")
        for writer in movie_info["writers"]:
            print(f"\t{writer.title()}")

        print("Actors:")
        for actor in movie_info["actors"]:
            print(f"\t{actor.title()}")

    else:
        print("Movie Not Found.")
