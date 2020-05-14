import requests
from bs4 import BeautifulSoup
import sys
from Data import Data


class ChatBot(Data):

    def show_movie_part(self, required_data, user_data, data_dict):
        """Displays the required part of the data."""

        if required_data == "writers":
            print("\nWriters:")
            for writer in data_dict[required_data]:
                print(f"\t{writer.title()}")

        elif required_data == "cast":
            print("\nActors:")
            print("\tActor : Character")
            for actor in data_dict[required_data]:
                actor_name, character = actor.split(":")
                print(f"\t{actor_name.title()} : {character.title()}")

        elif required_data == "age":
            print("\nAge Appropriate:")
            print(f"\t{data_dict[required_data]}")

        else:
            print(f"\n{required_data.title()}:")
            print(f"\t{data_dict[required_data]}")

    def show_movie_output(self, required_data, user_data, data_dict):
        """Displays the required output."""
        if required_data == "all":
            for item in data_dict:
                self.show_movie_part(item, user_data, data_dict)

        else:
            # output = data_dict[required_data]
            self.show_movie_part(required_data, user_data, data_dict)

    def show_actor_movie_num(self, actor, actor_data):
        """Prints the number of movies performed by the actor."""

        print(f"\nMovie Performed by {actor.title()}:\n\t{len(actor_data)}")

    def show_movies_performed(self, actor, actor_data):
        """Prints the movie : character played"""

        print("\nMovie : Character Played\n")
        for movie in actor_data:
            print(f"\t{movie['movie']} : {movie['character']}")

    def show_character_name(self, actor_data, search_movie, actor):
        """Prints the name of the character performed by the actor in a certain movie."""

        search_movie = search_movie.lower().strip()

        if search_movie == "q":
            sys.exit()

        for movie in actor_data:

            if movie["movie"].lower().strip() == search_movie:
                print(f"\n{search_movie.title()}:")
                print(f"\t{movie['character'].title()}")
                return None

        print(f"{actor.title()} has not performed any movie called {search_movie.title()}.")

    def chat(self, required_category, required_movie):
        """Gets input from user and shows output using show_output function."""

        if not required_category:
            category =  input("\nEnter the category(movie, actor):\n>>>").lower().strip()

            if category == "q":
                sys.exit()

            get_movie = True

        else:
            category = required_category
            get_movie = False

        if category == "movie":

            if get_movie:
                movie = input("\nEnter the movie name:\n>>>")

                if movie.lower().strip() == "q":
                    sys.exit()

            else:
                movie = required_movie

            # return dict if found else returns false
            data_dict = self.get_movie_dict_from_file(movie)

            if data_dict:
                user_data = input("\nWhat are you looking for?(all, summary, ratings, age appropriate, duration, genre, release date, director, writers, actors)\n>>>").lower().strip()

                if user_data == "q":
                    sys.exit()
                elif user_data == "all":
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

                self.show_movie_output(req_data, user_data, data_dict)

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

            if actor == "q":
                sys.exit()

            actor_data = self.load_actor_data(actor)

            user_data = input("\nWhat are you looking for?(all, character played in movie, movies performed, number of movies performed)\n>>>").lower().strip()

            if user_data == "q":
                sys.exit()

            elif user_data == "all":
                self.show_actor_movie_num(actor, actor_data)
                self.show_movies_performed(actor, actor_data)

            elif user_data == "character played in movie":
                search_movie = input("\nEnter the movie name:\n>>>")
                self.show_character_name(actor_data, search_movie, actor)

            elif user_data == "movies performed":
                self.show_movies_performed(actor, actor_data)

            elif user_data == "number of movies performed":
                self.show_actor_movie_num(actor, actor_data)

            else:
                print("Could Not Understand.\nPlease try again.")
                self.chat("actor", None)


        else:
            pass
