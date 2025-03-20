from api import TikTokApi
from queryFormatter import QueryFormatter
from file_converter import FileConverter
#from fileHandler import FileHandler
#from tiktok_login import Login
from usageGui import Gui
from tkinter import Tk

def main():
    tiktok_api = TikTokApi()
    query_formatter = QueryFormatter()
    t1 = ("username", "izzyandmarysdad", "EQ")
    t2 = ("keyword", "Chicken", "EQ")
    args = [t1, t2]
    and_clause = query_formatter.query_AND_clause(args)
    print("Entire query body:")
    q = query_formatter.query_builder("20250101", "20250129", and_clause)
    vids = tiktok_api.get_videos_by_dynamic_query_body(q, "20250101", "20250129")
    print(vids)
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
    #ogin.login()
    #gui = Gui("ghj", "ghjk", "ghjkl")
    #gui.test_page()
    
    #Make login pop up, save the client secrets and stuff to pass into gui
    #
    
    
    #   1 - QueryFormatter takes input from GUI, gives to TikTok Api
    #   2 - TikTokApi takes query, fetches data from endpoint, sends to FileConverter
    #   3 - FileConverter converts json to csv, and provides json and csv files
    #   4 - (Optional) FileHandler creates PDF and/or excel sheet
    

if __name__ == "__main__":
    main()