from api import TikTokApi
from queryFormatter import QueryFormatter
from file_converter import FileConverter
#from fileHandler import FileHandler
#from tiktok_login import Login
from usageGui import Gui

def main():
    tiktok_api = TikTokApi()
    query_formatter = QueryFormatter()
    file_converter = FileConverter()
    #file_handler = FileHandler()
    
    #In login, check if client secret stuff are valid by fetching access token
    #login = Login()
    gui = Gui("ghj", "ghjk", "ghjkl")
    gui.test_page()
    
    #Make login pop up, save the client secrets and stuff to pass into gui
    #login.login()
    
    
    #   1 - QueryFormatter takes input from GUI, gives to TikTok Api
    #   2 - TikTokApi takes query, fetches data from endpoint, sends to FileConverter
    #   3 - FileConverter converts json to csv, and provides json and csv files
    #   4 - (Optional) FileHandler creates PDF and/or excel sheet
    

if __name__ == "__main__":
    main()