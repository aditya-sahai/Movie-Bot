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
            print(f"{user_data.title()}:\n")
            print(f"\t{data_dict[required_data]}")

    def show_output(self, required_data, user_data, data_dict):
        """Displays the required output."""

        if required_data != "all":
            output = data_dict[required_data]

        if required_data == "all":
            for item in data_dict:
                self.show_part(item, user_data, data_dict)

        else:
            self.show_part(required_data, user_data, data_dict)

    def chat(self):
        """Gets input from user and shows output using show_output function."""

        category = input("Enter the category(movie, actor):\n>>>").lower().strip()

        if category == "movie":
            movie = input("Enter the movie name:\n>>>")

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
                pass

        elif category == "actor":
            pass

        else:
            pass
