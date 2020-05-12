import requests
from bs4 import BeautifulSoup
from Data import Data


class ChatBot(Data):

    def show_part(self, required_data, user_data, data_dict):
        """Displays the required part of the data."""

        if required_data == "writers":
            print("Writers:\n")
            for writer in data_dict[required_data]:
                print(f"\t{writer.title()}")

        elif required_data == "cast":
            print("Actors:\n")
            print("\tActor : Character")
            for actor in data_dict[required_data]:
                actor_name, character = actor.split(":")
                print(f"\t{actor_name.title()} : {character.title()}")

        elif required_data == "age":
            print("Age Appropriate:\n")
            print(f"\t{data_dict[required_data]}")

        else:
            print(f"{required_data.title()}:\n")
            print(f"\t{data_dict[required_data]}")

    def show_output(self, required_data, user_data, data_dict):
        """Displays the required output."""

        if required_data != "all":
            output = data_dict[required_data]

        elif required_data == "all":
            for item in data_dict:
                self.show_part(item, user_data, data_dict)

        else:
            self.show_part(required_data, user_data, data_dict)

    def chat(self, required_category, required_movie):
        """Gets input from user and shows output using show_output function."""

        if not required_category:
            category = input("\nEnter the category(movie, actor):\n>>>").lower().strip()
            get_movie = True

        else:
            category = required_category
            get_movie = False

        if category == "movie":

            if get_movie:
                movie = input("\nEnter the movie name:\n>>>")

            else:
                movie = required_movie

            # return dict if found else returns false
            data_dict = self.get_movie_dict_from_file(movie)

            if data_dict:
                user_data = input("What are you looking for?(all, summary, ratings, age appropriate, duration, genre, release date, director, writers, actors)\n>>>").lower().strip()

                if user_data == "all":
                    req_data = "all"
                elif user_data == "summary":
                    req_data = 'desc'
                elif user_data == "ratings":
                    req_data = "rating"
                elif user_data == "age appropriate":
                    req_data = "age"
                elif user_data == "duration":
                    req_data = "duration"
                elif user_data == "genre":
                    req_data = "genre"
                elif user_data == "release date":
                    req_data = "release-date"
                elif user_data == "director":
                    req_data = "director"
                elif user_data == "writers":
                    req_data = "writers"
                elif user_data == "actors":
                    req_data = "cast"

                self.show_output(req_data, user_data, data_dict)

            else:

                # the following has been done to get a precise name
                movie = movie.strip().replace(" ", "+")
                url = f'https://www.google.com/search?q=imdb+{movie}'
                response = requests.get(url, headers=self.headers)

                title = BeautifulSoup(response.content, "html.parser").find(class_="LC20lb DKV0Md").get_text().replace(" - IMDb", "").strip()[:-7]
                print(f'Getting results for {title}.')

                # this is done so that the name written in the file and the name being searched are same
                movie = title

                if not self.get_movie_dict_from_file(movie):

                    # this is needed so as to write a line of the movie in the file else it is not needed
                    data_dict = self.get_data_line_from_google(movie)

                self.chat(category, movie)

        elif category == "actor":

            actor = input("\nEnter the actor name:\n>>>").lower().strip()

            actor_dict = self.load_actor_data(actor)
            print(actor_dict)

        else:
            pass
