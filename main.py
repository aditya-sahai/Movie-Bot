from Data import Data


def show_output(data_dict):
    """Prints the desired output."""
    key_word = input("What are you looking for?\n(complete movie data, summary, rating, age restriction, release year, director, writer, actors)\n>>>").lower().strip()

    if key_word == "complete movie data":
        for item in data_dict:
            print(item.title())
            item = data_dict[item].split(",")
            for var in item:
                print(f"\t{var}")

    elif key_word == "summary":
        print(f"Summary:\n\t{data_dict['desc']}")

    elif key_word == "rating":
        print(f"Rating:\n\t{data_dict['rating']}")

    elif key_word == "age restriction":
        print(f"Summary:\n\t{data_dict['age']}")

    elif key_word == "release year":
        print(f"Release Year:\n\t{data_dict['release-date']}")

    elif key_word == "director":
        print(f"Director:\n\t{data_dict['director']}")

    elif key_word == "writer":
        print(f"Writers:\n")
        for writer in data_dict["writers"]:
            print(f"\t{writer}")

    elif key_word == "actors":
        print(f"Actors:\n")
        print("\tActor Name : Character Name\n")
        for actor in data_dict["cast"]:
            name = actor.split(":")[0]
            character = actor.split(":")[1]
            print(f"\t{name} : {character}")

def chat_bot():
    """Contains if and else for understanding user need."""
    user_category = input("Enter category(actor, movie)\n>>>").lower().strip()

    if user_category == "movie":

        movie = input("Please enter the movie:\n>>>")
        data_dict = obj.get_movie_dict(movie)

        if data_dict != False:
            movie = input("Please enter precise movie name:\n>>>")
            show_output(data_dict)

        else:
            status = obj.get_data_line_from_google(movie)
            if not status:
                print("Please check your spelling and try again.")
                chat_bot()
            else:
                data_dict = obj.get_movie_dict(movie)
                show_output(data_dict)


obj = Data()
obj.restore_data()
# chat_bot()
