from bs4 import BeautifulSoup
import requests


class Data:
    """A class for reading and updating the csv file."""

    headers = {"user-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"}

    def __init__(self):
        """Initialize values."""
        self.MOVIE_FILE_NAME = "movies-data.csv"
        self.MOVIE_URL = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"

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
        genre = genre.strip().split("\n")
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
                actor, character = actor.strip(), character.strip().replace(" \n  \n  \n  ", " ")
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

if __name__ == "__main__":
    obj = Data()
    movie_data = obj.get_single_movie_data_url("https://www.imdb.com/title/tt0111161/")
    print(movie_data)
