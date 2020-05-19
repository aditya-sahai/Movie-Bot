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
                req_data = input("\nWhat are you looking for?(Age-Appropriate, Duration, Genre, Release-Date, Rating, Summary, Director, Writers, Actors)\n>>>")

                if movie == "q":
                    sys.exit()

                if movie_data != None:
                    self.show_movie_req_data(movie_data, req_data)

                else:
                    movie_data = self.write_new_movie_data(movie)

                    # write_new_movie_data does not return None or False as i am unable to check for validity of a movie
                    if movie_data:
                        self.show_movie_req_data(movie_data, req_data)

                    else:
                        pass
                        # when the movie does not exist

        elif category == "actor":
            pass

        else:
            pass
