from tkinter import *
from tkinter import messagebox
import requests
from usageGui import Gui
import logging

class Login:
    def __init__(self,master):
        self.master = master
        master.title("Tiktok api login")
        
        Label(master, text="Client ID:").grid(row=1, column=0, sticky=W, padx=5, pady=5)
        Label(master, text="Client Key:").grid(row=2, column=0, sticky=W, padx=5, pady=5)
        Label(master, text="Client Secret:").grid(row=3, column=0, sticky=W, padx=5, pady=5)

        self.client_id_entry = Entry(master)
        self.client_key_entry = Entry(master)
        self.client_secret_entry = Entry(master, show="*")
        
        
        self.client_id_entry.grid(row=1, column=1, padx=5, pady=5)
        self.client_key_entry.grid(row=2, column=1, padx=5, pady=5)
        self.client_secret_entry.grid(row=3, column=1, padx=5, pady=5)

        
        Button(master, text="Logg inn", command=self.login).grid(row=4, column=0, columnspan=2, pady=10)
        
        
        self.access_token = None
        
    def login(self):
        self.client_id = self.client_id_entry.get()
        self.client_key = self.client_key_entry.get()
        self.client_secret = self.client_secret_entry.get()

        if not self.client_id or not self.client_key or not self.client_secret:
            messagebox.showwarning("Feil", "Du må fylle inn alle feltene")
            return

        success, message = self.test_connection(self.client_id, self.client_key, self.client_secret)

        if success:
            messagebox.showinfo("Login Successful welcome!", message)
            self.master.destroy()
            self.open_main_window()
        else:
            messagebox.showerror("Login Failed", message)
            
                 

    def test_connection(self, client_id, client_key, client_secret):
        endpoint = "https://open.tiktokapis.com/v2/oauth/token/"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'client_id': client_id,
            'client_secret': client_secret,
            'client_key': client_key,
            'grant_type': 'client_credentials'
        }

        try:
            response = requests.post(endpoint, headers=headers, data=data)
            
            if response.status_code == 200:
                try:
                    json_resp = response.json()
                    
                    if "error" in json_resp:
                        logging.error("Incorrect parameters")
                        return False, "Incorrect parameters"

                    if "access_token" in json_resp:
                        self.access_token = json_resp['access_token']
                        return True, "Access token successfully retrieved."
                    
                    logging.error("Unexpected response from TikTok API")
                    return False, "Unexpected response from TikTok API"
                
                except ValueError:
                    logging.error("Invalid JSON response")
                    return False, "Invalid JSON response"
            
            else:
                logging.error(f"Something went wrong: {response.status_code} - {response.text}")
                return False, f"Something went wrong: {response.status_code} - {response.text}"
            
        except requests.RequestException as e:
            logging.error(f"Connection error: {str(e)}")
            return False, f"Connection error: {str(e)}"

        
    def open_main_window(self):
        main_window = Toplevel(self.master)
        Label(main_window, text="Velkommen!").pack(pady=20)
        if self.access_token:
            gui = Gui(self.client_secret, self.client_id, self.client_key, self.access_token)
            gui.test_page()
        else:
            messagebox.showerror("Error", "No access token found. Please try again.")
        
        
if __name__ == "__main__":
    root = Tk()              
    app = Login(root)      
    root.mainloop()
            



