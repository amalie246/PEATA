from api import TikTokApi
from queryFormatter import QueryFormatter
from file_converter import FileConverter
#from fileHandler import FileHandler
from tiktok_login import Login
from gui import Gui
from tkinter import Tk

def main():
    #tiktok_api = TikTokApi()
    
    #root = Tk()
    #login = Login(root)
    #root.mainloop()
    
    #if not login.access_token:
    #    print("Access token could not be obtained. Exiting program.")
    #    return
    
    gui = Gui("a", "b", "c", "dfghjkl")
    gui.test_page()

    
    
    #videos = tiktok_api.get_videos("izzyandmarysdad", "keyword", "20250310", "20250318")
    #Can check if a video query didnt go well by checking if not videos
    #Nothing to download, tell user that they need different arguments
    #if not videos:
    #    print("Did not retrieve videos")
    #query_formatter = QueryFormatter()
    #t1 = ("username", "izzyandmarysdad", "EQ")
    #t2 = ("keyword", "Chicken", "EQ")
    #args = [t1]
    #and_clause = query_formatter.query_AND_clause(args)
    

    # videos = tiktok_api.get_videos("izzyandmarysdad", "keyword", "20250310", "20250318")
    #Can check if a video query didnt go well by checking if not videos
    #Nothing to download, tell user that they need different arguments
    # if not videos:
        # print("Did not retrieve videos")
    #query_formatter = QueryFormatter()
    #file_converter = FileConverter()
    #file_handler = FileHandler()
    
    #In login, check if client secret stuff are valid by fetching access token
    #root = Tk()
    #login = Login(root)
    #root.mainloop()
    #login.login()
    
    #Make login pop up, save the client secrets and stuff to pass into gui
    #
    
    
    #   1 - QueryFormatter takes input from GUI, gives to TikTok Api
    #   2 - TikTokApi takes query, fetches data from endpoint, sends to FileConverter
    #   3 - FileConverter converts json to csv, and provides json and csv files
    #   4 - (Optional) FileHandler creates PDF and/or excel sheet
    

if __name__ == "__main__":
    main()