from bs4 import BeautifulSoup
import requests


class Data:
    """A class for reading and updating the csv file."""

    headers = {"user-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"}

    def __init__(self):
        """Initialize values."""
        self.MOVIE_FILE_NAME = "movies-data.csv"
        self.MOVIE_URL = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"

        self.ACTOR_FILE_NAME = "actors-data.csv"

    def get_single_movie_data_url(self, url):
        """Returns dictionary containing movie data from a given url."""

        imdb_response = requests.get(url, headers=Data.headers)
        imdb_soup = BeautifulSoup(imdb_response.content, "html.parser")

        imdb_soup.find("div", {"class" : "title_wrapper"}).h1.span.decompose()
        movie_name = imdb_soup.find("div", {"class" : "title_wrapper"}).h1.get_text().strip()

        sub_title_data = imdb_soup.find("div", {"class" : "subtext"}).get_text().split("|")

        try:
            age_restriction, duration, genre, release_date = sub_title_data

        except ValueError:
            age_restriction = "Approved"
            duration, genre, release_date = sub_title_data

        age_restriction = age_restriction.strip()
        duration = duration.strip()
        genre = genre.strip().split(", \n")
        release_date = release_date.strip()

        rating = imdb_soup.find("span", {"itemprop" : "ratingValue"}).get_text().strip()

        summary = imdb_soup.find("div", {"class" : "summary_text"}).get_text().strip()

        cast_page_url = f"{url}fullcredits/"
        cast_page_response = requests.get(cast_page_url, headers=Data.headers)
        cast_page_soup = BeautifulSoup(cast_page_response.content, "html.parser")

        credits_tables = cast_page_soup.find_all("table", {"class" : "simpleTable simpleCreditsTable"})

        director = credits_tables[0].find("td", {"class" : "name"}).get_text().strip()
        writers = credits_tables[1].find_all("td", {"class" : "name"})

        for index, writer in enumerate(writers):
            writers[index] = writer.get_text().strip()

        actors_data = cast_page_soup.find("table", {"class" : "cast_list"}).find_all("tr")[1:]

        for index, actor_row in enumerate(actors_data):

            # this is done to catch the empty line before the uncredited cast
            if len(actor_row.get_text().split("...")) < 2:
                # slicing is done to remove the uncredited actors
                actors_data = actors_data[:index]
                break

            else:
                actor, character = actor_row.get_text().split("...")
                actor, character = actor.strip(), character.strip().replace("\n", "").replace("\t", "").replace("       ", " ")
                actors_data[index] = (actor, character)

        movie_data = {
            "name" : movie_name,
            "age-appropriate" : age_restriction,
            "duration" : duration,
            "genre" : genre,
            "release-date" : release_date,
            "rating" : rating,
            "summary" : summary,
            "director" : director,
            "writers" : writers,
            "actors" : actors_data,
        }

        return movie_data

    def get_single_movie_data_file(self, movie_name):
        """Reads the file and returns a dictionary in the same form as get_single_movie_data_url()."""

        movie_name = movie_name.lower().strip()
        self.movie_file = open(self.MOVIE_FILE_NAME, "r")
        lines = self.movie_file.read().split("\n")[1:-1]

        for line in lines:
            line = line.replace('","', "_")
            line = line[1:-1]
            line = line.split("_")

            file_movie_name = line[0].lower().strip()

            if file_movie_name == movie_name:

                actors = line[9].split(",")
                for index, actor in enumerate(actors):
                    actor = actor.split(" : ")
                    actors[index] = actor

                movie_data = {
                    "name" : file_movie_name,
                    "age-appropriate" : line[5],
                    "duration" : line[4],
                    "genre" : line[3].split(","),
                    "release-date" : line[6],
                    "rating" : line[2],
                    "summary" : line[1],
                    "director" : line[7],
                    "writers" : line[8].split(","),
                    "actors" : actors,
                }

                self.movie_file.close()
                return movie_data

        self.movie_file.close()
        return None

    def write_single_movie_data(self, data):
        """Writes a single movie into the file."""

        line = f'\"{data["name"]}\",\"{data["summary"]}\",\"{data["rating"]}\",'

        line += '"'
        for genre in data["genre"]:
            line += f"{genre},"
        line = line[:-1]
        line += '",'

        line += f'\"{data["duration"]}\",'
        line += f'\"{data["age-appropriate"]}\",'
        line += f'\"{data["release-date"]}\",'
        line += f'\"{data["director"]}\",'

        line += '"'
        for writer in data["writers"]:
            line += f"{writer},"
        line = line[:-1]
        line += '",'

        line += '"'
        for actor in data["actors"]:
            line += f"{actor[0]} : {actor[1]},"
        line = line[:-1]
        line += '"\n'

        self.movie_file.write(line)

    def write_top_250_movies_data(self):
        """Writes the data of the top 250 movies into a csv file."""

        imdb_response = requests.get(self.MOVIE_URL, headers=Data.headers)
        imdb_soup = BeautifulSoup(imdb_response.content, "html.parser")

        imdb_table = imdb_soup.find("tbody", {"class" : "lister-list"})
        movie_rows = imdb_table.find_all("tr")

        self.movie_file = open(self.MOVIE_FILE_NAME, "w")
        self.movie_file.write("Movie,Summary,Rating,Genre,Duration,Age-Approriate,Rlease-Date,Director,Writers,Actors:Characters\n")

        for num, movie in enumerate(movie_rows[:10]):
            url = f'https://www.imdb.com{movie.find("td", {"class" : "titleColumn"}).a["href"].split("?")[0]}'
            data = self.get_single_movie_data_url(url)

            self.write_single_movie_data(data)
            print(f"Movie#{num+1}, \'{data['name']}\' is done.")

        self.movie_file.close()

    def write_new_movie_data(self, name):
        """Writes a new movie data into the csv file."""

        url = f"https://www.google.com/search?q=imdb+{name.replace(' ', '+')}"

        google_response = requests.get(url, headers=Data.headers)
        google_soup = BeautifulSoup(google_response.content, "html.parser")

        link = google_soup.find("div", {"class" : "r"}).a["href"]
        google_found_name = google_soup.find("h3", {"class" : "LC20lb DKV0Md"}).get_text().split("(")[0].strip()
        print(f"\nShowing results for {google_found_name}.")

        data = self.get_single_movie_data_url(link)

        self.movie_file = open(self.MOVIE_FILE_NAME, "a")
        self.write_single_movie_data(data)
        self.movie_file.close()

        return data

    def get_actor_data_name(self, actor_name):
        """Returns dictionary containing actor data from a name."""

        url = f"https://www.google.com/search?q=imdb+{actor_name.replace(' ', '+')}"

        google_response = requests.get(url, headers=Data.headers)
        google_soup = BeautifulSoup(google_response.content, "html.parser")

        link = google_soup.find("div", {"class" : "r"}).a["href"]

        imdb_response = requests.get(link, headers=Data.headers)
        imdb_soup = BeautifulSoup(imdb_response.content, "html.parser")

        birthdate = imdb_soup.find("time").get_text().replace("\n", "").split(",")
        birthdate = f"{birthdate[0].strip()}, {birthdate[1].strip()}"

        birthplace = imdb_soup.find("div", {"id" : "name-born-info"}).find_all("a")[-1].get_text().strip()

        famous_movies = imdb_soup.find_all("div", {"class" : "knownfor-title"})

        for index, movie in enumerate(famous_movies):
            movie_name = movie.find("div", {"class" : "knownfor-title-role"}).a.get_text().strip()
            character_played = movie.find("span", {"class" : "knownfor-ellipsis"}).get_text().strip()

            famous_movies[index] = (movie_name, character_played)

        movies_table = imdb_soup.find("div", {"class" : "filmo-category-section"})
        movie_table_rows = movies_table.find_all("div")

        movie_data = []

        for index, movie_row in enumerate(movie_table_rows):

            if movie_row.get("id") and not movie_row.get("style"):
                movie = movie_row.b.a.get_text().strip()
                movie_data.append(movie)

        data_dict = {
            "name" : actor_name.title(),
            "birthdate" : birthdate,
            "birthplace" : birthplace,
            "famous-movies/series" : famous_movies,
            "all-movies/series" : movie_data,
        }

        return data_dict

    def get_actor_data_file(self, actor_name):
        """Returns data if found else returns None."""

        actor_name = actor_name.lower().strip()

        self.actor_file = open(self.ACTOR_FILE_NAME, "r")
        lines = self.actor_file.read().split("\n")
        self.actor_file.close()

        for line in lines:
            line = line.replace('","', "_")
            line = line[1:-1]
            line = line.split("_")

            file_actor = line[0].lower().strip()

            if file_actor == actor_name:

                famous_movies = line[3].split(" , ")
                for index, movie in enumerate(famous_movies):
                    famous_movies[index] = movie.split(" : ")

                movies = line[4].split(" , ")

                data_dict = {
                    "name" : file_actor.title(),
                    "birthdate" : line[1],
                    "birthplace" : line[2],
                    "famous-movies/series" : famous_movies,
                    "all-movies/series" : movies,
                }

                return data_dict

        return None

    def write_new_actor_data(self, actor_data):
        """Writes the actor data in the actors-data.csv file."""

        line = f"\"{actor_data['name'].title()}\",\"{actor_data['birthdate']}\",\"{actor_data['birthplace']}\","

        line += '"'
        for famous_movie in actor_data["famous-movies/series"]:
            line += f'{famous_movie[0]} : {famous_movie[1]} , '
        line = line[:-2]
        line += '",'

        line += '"'
        for movie in actor_data["all-movies/series"]:
            line += f'{movie} , '
        line = line[:-2]
        line += '"\n'

        self.actor_file = open(self.ACTOR_FILE_NAME, "a")
        self.actor_file.write(line)
        self.actor_file.close()


if __name__ == "__main__":
    obj = Data()

    actor_data = obj.get_single_movie_data_file("the shawshank redemption")
    print(actor_data)
