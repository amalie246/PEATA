from api import TikTokApi
from queryFormatter import QueryFormatter
from FileProcessor import FileProcessor
#from tiktok_login import Login
from gui import Gui
from tkinter import Tk

def main():
    #root = Tk()
    #login = Login(root)
    #root.mainloop()
    
    #if not login.access_token:
    #    print("Access token could not be obtained. Exiting program.")
    #    return
    
    gui = Gui("a", "b", "c", "d")
    gui.main_frame()
    
    """tiktok_api = TikTokApi()
    
    username = "izzyandmarysdad"
    keyword = "Chicken"
    start_date = "20250101"
    end_date = "20250129"

    
    
    videos = tiktok_api.get_videos(username, keyword, start_date, end_date)
    #Can check if a video query didnt go well by checking if not videos
    #Nothing to download, tell user that they need different arguments
    if not videos:
     print("Did not retrieve videos")
     return
 
    print(f"Fetched videos: {videos}")
    
    query_formatter = QueryFormatter()
    t1 = ("username", username, "EQ")
    t2 = ("keyword", keyword, "EQ")
    args = [t1, t2]
    and_clause = query_formatter.query_AND_clause(args)
    print(f"Formatted query: {and_clause}")
    
  
    file_processor = FileProcessor()
    file_processor.export_data("test", videos)
    #file_processor.save_any_json_data(videos, filename="tiktok_videos", file_format="json")
    #file_processor.save_any_json_data(videos, filename="tiktok_videos", file_format="csv")
    
    #data = file_processor.open_file()
    
    #if data is not None:
    #    file_processor.export_as_excel()
        
    #    file_processor.close_file()

    #videos = tiktok_api.get_videos("izzyandmarysdad", "keyword", "20250310", "20250318")
    #Can check if a video query didnt go well by checking if not videos
        #Nothing to download, tell user that they need different arguments
    # if not videos:
        # print("Did not retrieve videos")
    #query_formatter = QueryFormatter()"""
  
    
    #In login, check if client secret stuff are valid by fetching access token
    #root = Tk()
    #login = Login(root)
    #root.mainloop()
    #login.login()
    
    #Make login pop up, save the client secrets and stuff to pass into gui
    
if __name__ == "__main__":
    main()