from bs4 import BeautifulSoup
import requests


class Data:
    """A class for reading and updating the csv file."""
    def __init__(self):
        """Initialize values."""
        self.movie_file_name = "movies-data.csv"
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

        self.file = open(self.movie_file_name, "a")
        self.file.write(line)
        self.file.close()

        return True

    def load_actor_data(self, actor):
        """Returns a dictionary containing actor data."""

        data = []

        actor = actor.replace(" ", "+")
        google_page_url = f"https://www.google.com/search?q=imdb+{actor}"

        google_page_response = requests.get(google_page_url, headers=self.headers)
        google_soup = BeautifulSoup(google_page_response.content, "html.parser")

        link = google_soup.find(class_="r").a["href"]

        imdb_response = requests.get(link, headers=self.headers)
        imdb_soup = BeautifulSoup(imdb_response.content, "html.parser")

        imdb_soup.find(class_="see-more inline nobr-only").decompose()

        birthdate = imdb_soup.find("time").get_text()
        birthdate = birthdate.split(",")
        birthdate = f'{birthdate[0].strip()}, {birthdate[1].strip()}'

        movies_done_rows = imdb_soup.find(class_="filmo-category-section").find_all("div", {"class" : "filmo-row odd"})

        for movie_done_row in movies_done_rows:

            actor_code = movie_done_row.attrs["id"].replace("actor-", "")

            # the for and the if would remove the episode if the actor has performed a tv series
            for movie_done in movie_done_row.find_all(class_="filmo-episodes"):
                movie_done.decompose()

            if movie_done_row.find(id=f"more-episodes-{actor_code}-actor"):
                movie_done_row.find(id=f"more-episodes-{actor_code}-actor").decompose()

            movie_name = movie_done_row.b.a.get_text().strip()
            character_played = str(movie_done_row).split("br")[-1].replace("</div>", "").replace("/>", "").strip()

            single_movie_data = {"movie" : movie_name, "character" : character_played}
            data.append(single_movie_data)
            # print(single_movie_data)

        movies_done_rows = imdb_soup.find(class_="filmo-category-section").find_all("div", {"class" : "filmo-row even"})

        for movie_done_row in movies_done_rows:

            actor_code = movie_done_row.attrs["id"].replace("actor-", "")

            # the for and the if would remove the episode if the actor has performed a tv series
            for movie_done in movie_done_row.find_all(class_="filmo-episodes"):
                movie_done.decompose()

            if movie_done_row.find(id=f"more-episodes-{actor_code}-actor"):
                movie_done_row.find(id=f"more-episodes-{actor_code}-actor").decompose()

            movie_name = movie_done_row.b.a.get_text().strip()
            character_played = str(movie_done_row).split("br")[-1].replace("</div>", "").replace("/>", "").strip()

            single_movie_data = {"movie" : movie_name, "character" : character_played}
            data.append(single_movie_data)
            # print(single_movie_data)

        return data

    def restore_data(self):
        """Updates the movies in the csv file and deletes old data."""
        response = requests.get(self.URL, headers=self.headers)
        # print(response.status_code)

        self.table_soup = BeautifulSoup(response.content, "html.parser").find(class_="lister-list")
        self.rows = self.table_soup.find_all("tr")

        self.file = open(self.movie_file_name, "w")
        self.file.write("Name,Summary,IMDb Rating,Age Appropriate,Duration,Genre,Release Year,Director,Writers,Actor:Character\n")

        for i, self.row in enumerate(self.rows):

            link = f"https://www.imdb.com/{self.row.a['href']}".split("?")[0]
            name, line = self.get_movie_data(link)

            self.file.write(line)

            print(i + 1, name)

        self.file.close()

    def get_movie_dict_from_file(self, word):
        """Returns the a dictionary of the line containing word."""
        file = open(self.movie_file_name, "r")
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
