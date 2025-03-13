from tkinter import *
from tkinter import messagebox
import requests

class Login:
    def __init__(self,master):
        self.master = master
        master.title("Tiktok api login")
        
        #Label(master, text="API URL:").grid(row=0, column=0, sticky=W, padx=5, pady=5)
        Label(master, text="Client ID:").grid(row=1, column=0, sticky=W, padx=5, pady=5)
        Label(master, text="Client Key:").grid(row=2, column=0, sticky=W, padx=5, pady=5)
        Label(master, text="Client Secret:").grid(row=3, column=0, sticky=W, padx=5, pady=5)

        self.e1 = Entry(master)
        self.e2 = Entry(master)
        self.e3 = Entry(master)
        self.e4 = Entry(master, show="*")

        #self.e1.grid(row=0, column=1, padx=5, pady=5)
        self.e2.grid(row=1, column=1, padx=5, pady=5)
        self.e3.grid(row=2, column=1, padx=5, pady=5)
        self.e4.grid(row=3, column=1, padx=5, pady=5)
        
        Button(master, text="Logg inn", command=self.login).grid(row=4, column=0, columnspan=2, pady=10)
        
        
        
        
        
    def login(self):
        #api_url = self.e1.get()
        client_id = self.e2.get()
        client_key = self.e3.get()
        client_secret = self.e4.get()

        if not client_id or not client_key or not client_secret:
            messagebox.showwarning("Feil", "Du må fylle inn alle feltene")
            return

        success, message = self.test_connection(client_id, client_key, client_secret)

        if success:
            messagebox.showinfo("Innlogging vellykket", "Velkommen!")
            self.master.destroy()
            self.open_main_window()
        else:
            messagebox.showerror("Innlogging feilet", message)


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
                return True, "API-tilkobling vellykket!"
            else:
                return False, f"Feil: {response.status_code} - {response.text}"
        except requests.exceptions.RequestException as e:
            return False, f"Tilkoblingsfeil: {e}"
        
        
    def open_main_window(self):
        main_window = Toplevel(self.master)
        Label(main_window, text="Velkommen!").pack(pady=20)
        
if __name__ == "__main__":
    root = Tk()              
    app = Login(root)      
    root.mainloop()
            



