from bs4 import BeautifulSoup
import datetime
import requests
import sys


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
        self.file.write("Name,Summary,IMDb Rating,Age Appropriate,Duration,Genre,Release Year,Director,Writers,Actor:Character\n")

        for i, self.row in enumerate(self.rows[:2]):

            name = self.row.find(class_="titleColumn").a.get_text().strip()
            link = f"https://www.imdb.com/{self.row.a['href']}".split("?")[0]
            rating = self.row.find(class_="ratingColumn imdbRating").get_text().strip()

            movie_response = requests.get(link, headers=self.headers)
            new_page_soup = BeautifulSoup(movie_response.content, "html.parser")

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

            desc = plot.find(class_="summary_text").get_text().strip()

            credit_box = plot.find_all(class_="credit_summary_item")
            director = credit_box[0].a.get_text()
            writers = credit_box[1].find_all("a")

            for index, writer in enumerate(writers):
                writers[index] = writer.get_text()

            cast_link = f"{link}fullcredits"
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

            self.file.write(line)
            # print(i + 1, name)
        self.file.close()
