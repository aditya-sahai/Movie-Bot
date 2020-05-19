from Data import Data
import sys


class ChatBot(Data):

    def show_movie_req_data(self, movie_dict, req_data):
        """Shows only the required data."""

        # seperate print types for string and 1d and 2d lists
        if req_data == "genre" or req_data == "writers":
            print(f"\n{req_data.title()}:")
            for data in movie_dict[req_data]:
                print(f"\t{data}")

        elif req_data == "actors":
            print(f"\nActor Name : Character Name:")
            for person in movie_dict[req_data]:
                print(f"\t{person[0]} : {person[1]}")

        elif req_data == "age-appropriate" or req_data == "duration" or req_data == "release-date" or req_data == "rating" or req_data == "summary" or req_data == "director" or req_data == "director":
            print(f"\n{req_data.title()}:")
            print(f"\t{movie_dict[req_data]}")

        else:
            print("Could not understand.")

    def show_actor_req_data(self, actor_dict, req_data):
        """Displays the required part of the user data."""

        if req_data == "all-movies/series":
            print(f"\n{req_data.title()}:")
            for data in actor_dict[req_data]:
                print(f"\t{data}")

        elif req_data == "famous-movies/series":
            print(f"\nMovie Name : Character Name:")
            for data in actor_dict[req_data]:
                print(f"\t{data[0]} : {data[1]}")

        elif req_data == "birthplace" or req_data == "birthdate":
            print(f"\n{req_data.title()}:")
            print(f"\t{actor_dict[req_data]}")

        else:
            print("\nCould not understand.")

    def chat(self):
        """The main user interface."""

        category = input("\nEnter the category(movie, actor):\n>>>").lower().strip()

        if category == "q":
            sys.exit()

        elif category == "movie":
            movie = input("\nEnter the movie name:\n>>>").lower().strip()

            if movie == "q":
                sys.exit()

            else:

                movie_data = self.get_single_movie_data_file(movie)

                if movie == "q":
                    sys.exit()

                if movie_data != None:
                    req_data = input("\nWhat are you looking for?(Age-Appropriate, Duration, Genre, Release-Date, Rating, Summary, Director, Writers, Actors)\n>>>").lower().strip()
                    self.show_movie_req_data(movie_data, req_data)

                else:
                    movie_data = self.write_new_movie_data(movie)

                    # write_new_movie_data does not return None or False as i am unable to check for validity of a movie
                    if movie_data:
                        req_data = input("\nWhat are you looking for?(Age-Appropriate, Duration, Genre, Release-Date, Rating, Summary, Director, Writers, Actors)\n>>>").lower().strip()
                        self.show_movie_req_data(movie_data, req_data)

                    else:
                        # when the movie does not exist
                        pass

        elif category == "actor":

            actor = input("\nEnter the actor name:\n>>>").lower().strip()

            if category == "q":
                sys.exit()

            actor_data = self.get_actor_data_file(actor)

            if actor_data:
                req_data = input("\nWhat are you looking for?(Birthdate, Birthplace, Famous-Movies/Series, All-Movies/Series)\n>>>").lower().strip()

                if category == "q":
                    sys.exit()

                self.show_actor_req_data(actor_data, req_data)

            else:
                actor_data = self.get_actor_data_name(actor)

                # write_new_movie_data does not return None or False as i am unable to check for validity of a movie
                if actor_data:
                    req_data = input("\nWhat are you looking for?(Birthdate, Birthplace, Famous-Movies/Series, All-Movies/Series)\n>>>").lower().strip()
                    self.show_actor_req_data(actor_data, req_data)
                    self.write_new_actor_data(actor_data)

                else:
                    # when the actor does not exist
                    pass

        else:
            pass
