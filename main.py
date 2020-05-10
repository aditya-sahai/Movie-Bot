from Data import Data


obj = Data()
# obj.restore_data()

movie = input("Enter any movie:\n>>>")
obj.get_data_line_from_google(movie)
