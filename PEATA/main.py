from tiktok_login import Login
from tkinter import Tk

def main():
    root = Tk()           
    app = Login(root)  
    root.attributes('-fullscreen', True)
    root.mainloop()
    
if __name__ == "__main__":
    main()