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

    def get_movie_data(self, url):
        """Returns a line to be written in the movie-data.csv file from a given url."""
        movie_response = requests.get(url, headers=self.headers)
        new_page_soup = BeautifulSoup(movie_response.content, "html.parser")

        # this is done to remove the span which contained the year in the h1 containing title
        new_page_soup.find(id="titleYear").decompose()
        name = new_page_soup.find(class_="title_wrapper").h1.get_text().strip()

        # here we are looking for a span with attr 'itemprop' and value 'ratingValue'
        rating = new_page_soup.find("span", {"itemprop" : "ratingValue"}).get_text().strip()

        title_list = new_page_soup.find(class_="subtext").get_text().split("|")

        try:
            release_year = title_list[3].strip()
        except IndexError:
            release_year = title_list[2].strip()
            age_restriction = "Unknown"
            duration = title_list[0].strip()
            genre_list = title_list[1].strip().split(",")
            genre = ""
            for genre_var in genre_list:
                genre += f"{genre_var.strip()},"
            genre = genre[:-1]
        else:
            age_restriction = title_list[0].strip()
            duration = title_list[1].strip()
            genre_list = title_list[2].strip().split(",")
            genre = ""
            for genre_var in genre_list:
                genre += f"{genre_var.strip()},"
            genre = genre[:-1]

        plot = new_page_soup.find(class_="plot_summary")

        desc = plot.find(class_="summary_text").get_text().replace("\"", "'").strip()

        credit_box = plot.find_all(class_="credit_summary_item")
        director = credit_box[0].a.get_text()
        writers = credit_box[1].find_all("a")

        for index, writer in enumerate(writers):
            writers[index] = writer.get_text()

        cast_link = f"{url}fullcredits"
        cast_response = requests.get(cast_link, headers=self.headers)
        cast_table_rows = BeautifulSoup(cast_response.content, "html.parser").find(class_="cast_list").find_all("tr")[1:]
        line = f'"{name}","{desc}","{rating}","{age_restriction}","{duration}","{genre}","{release_year}","{director}"'

        line += ',"'
        for writer in writers:
            line += f"{writer},"
        line = line[:-1]
        line += '"'

        line += ',"'
        for cast_table_row in cast_table_rows:
            try:
                actor = cast_table_row.find_all("td")[1].a.text.strip()
                character = cast_table_row.find_all("td")[3].a.text.strip()
            except AttributeError:
                continue
            except IndexError:
                break
            else:
                line += f"{actor}:{character},"
        line = line[:-1]
        line += '"\n'
        return name, line

    def get_data_line_from_google(self, movie):
        """Gets the data from google and writes it into the csv file."""

        movie = movie.strip().replace(" ", "+")
        url = f'https://www.google.com/search?q=imdb+{movie}'

        google_page_response = requests.get(url, headers=self.headers)
        google_page_soup = BeautifulSoup(google_page_response.content, "html.parser")

        movie_page_url = google_page_soup.find(class_="r").a["href"]

        if "https://www.imdb.com/title/" not in movie_page_url:
            return False

        name, line = self.get_movie_data(movie_page_url)

        self.file = open(self.file_name, "a")
        self.file.write(line)
        self.file.close()

        return True


    def restore_data(self):
        """Updates the movies in the csv file and deletes old data."""
        response = requests.get(self.URL, headers=self.headers)
        # print(response.status_code)

        self.table_soup = BeautifulSoup(response.content, "html.parser").find(class_="lister-list")
        self.rows = self.table_soup.find_all("tr")

        self.file = open(self.file_name, "w")
        self.file.write("Name,Summary,IMDb Rating,Age Appropriate,Duration,Genre,Release Year,Director,Writers,Actor:Character\n")

        for i, self.row in enumerate(self.rows):

            link = f"https://www.imdb.com/{self.row.a['href']}".split("?")[0]
            name, line = self.get_movie_data(link)

            self.file.write(line)

            print(i + 1, name)

        self.file.close()

    def get_movie_dict_from_file(self, word):
        """Returns the a dictionary of the line containing word."""
        file = open(self.file_name, "r")
        lines = file.readlines()[1:]
        file.close()

        for line in lines:
            # following lines have been done to maintain the commas
            line = line[1:]
            line = line.replace('","', "_")
            line = line.split("_")

            for index, item in enumerate(line):
                if index != 3 and index != 4 and index != 6:
                    # this is because index 3 4 and 6 contain the age, duration, release

                    item = item.replace('"', "").lower().strip()
                    if word.lower().strip() == item:
                        data_dict = {
                            "name" : line[0],
                            "desc" : line[1],
                            "rating" : line[2],
                            "age" : line[3],
                            "duration" : line[4],
                            "genre" : line[5],
                            "release-date" : line[6],
                            "director" : line[7],
                            "writers" : line[8].split(","),
                            "cast" : line[9].replace('"', "").strip().split(","),
                        }
                        return data_dict
        return False
