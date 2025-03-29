# Login functionality (User Input Validation, Window Transition on Successful Login)
import sys
import os
from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.uic import loadUi
import requests
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'gui')))

from gui.ui.loginUi import Ui_LoginWindow  

#from app.main_app import MainApp



# Inherite Ui_LoginWindow class from login.py
class LoginApp(QMainWindow, Ui_LoginWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.login_button.clicked.connect(self.handle_login)
        
    def handle_login(self):
        client_id = self.client_id_input.text()
        client_key = self.client_key_input.text()
        client_secret = self.client_secret_input.text()
        
        if self.test_connection(client_id, client_key, client_secret):
            self.accept_login()
        else: 
            self.show_error_message("Invalied credentials, please try agian.")
        
        # if client_id and client_key and client_secret:
        #     print(f"Client ID: {client_id}")
        #     print(f"Client key: {client_key}")
        #     print(f"Client Secret: {client_secret")
            
        #     # add actual login logic here
            
        # else: 
        #     print("Please input all the fields.")

    def test_connection(self, client_id, client_key, client_secret):
        # Actual login API call here
        # use requests library, send API call
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

    def accept_login(self):      
        QMessageBox.information(self, "Login Success", "Welcome to PEATA!")
        # Add logic for showing the mainApp after login success.
        
    def show_error_message(self,message):
        QMessageBox(self, "Login Failed", message)
        
if __name__ == "__main__":
    app = QApplication(sys.argv) # Initialize PyQt
    window = LoginApp()
    window.show() # show the window with UI
    sys.exit(app.exec())

    