from tkinter import *
from tkinter import messagebox
import requests

class Login:
    def login():
        api_url = e1.get()
        client_id = e2.get()
        client_key = e3.get()
        client_secret = e4.get()

        if not api_url or not client_id or not client_key or not client_secret:
            messagebox.showwarning("Feil", "Du må fylle inn alle feltene")
            return

        success, message = test_connection(api_url, client_id, client_key, client_secret)

        if success:
            messagebox.showinfo("Innlogging vellykket", "Velkommen!")
            master.destroy()
            open_main_window()
        else:
            messagebox.showerror("Innlogging feilet", message)


    def test_connection(api_url, client_id, client_key, client_secret):
        endpoint = f"{api_url}/oauth/token/"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'client_id': client_id,
            'client_secret': client_secret,
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


    master = Tk()
    master.title("TikTok API Login")

    Label(master, text="API URL:").grid(row=0, column=0, sticky=W, padx=5, pady=5)
    Label(master, text="Client ID:").grid(row=1, column=0, sticky=W, padx=5, pady=5)
    Label(master, text="Client Key:").grid(row=2, column=0, sticky=W, padx=5, pady=5)
    Label(master, text="Client Secret:").grid(row=3, column=0, sticky=W, padx=5, pady=5)

    e1 = Entry(master)
    e2 = Entry(master)
    e3 = Entry(master)
    e4 = Entry(master, show="*")

    e1.grid(row=0, column=1, padx=5, pady=5)
    e2.grid(row=1, column=1, padx=5, pady=5)
    e3.grid(row=2, column=1, padx=5, pady=5)
    e4.grid(row=3, column=1, padx=5, pady=5)

    Button(master, text="Logg inn", command=login).grid(row=4, column=0, columnspan=2, pady=10)

    master.mainloop()
