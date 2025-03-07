from api import TikTokApi
from queryFormatter import QueryFormatter
from file_converter import FileConverter
from fileHandler import FileHandler

def main():
    tiktok_api = TikTokApi();
    query_formatter = QueryFormatter();
    file_converter = FileConverter();
    file_handler = FileHandler();
    
    tiktok_api.get_video_comments("7463699433146961194");
    

if __name__ == "__main__":
    main()