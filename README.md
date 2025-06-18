# PEATA
Packaged Easier Access To API's


## Introduction
This project is meant to retrieve data from the TikTok Research API, targeted at researchers with access to the TikTok Research API. This version has a simple and straightforward GUI, you can see the more advanced GUI-version here: https://github.com/ElinEunjung/peata_ver2

This version can fetch video data with all fields available from the TikTok Research API (https://developers.tiktok.com/doc/research-api-specs-query-videos?enter_method=left_navigation), comment information from a video ID (https://developers.tiktok.com/doc/research-api-specs-query-video-comments?enter_method=left_navigation) and user info by username (https://developers.tiktok.com/doc/research-api-specs-query-user-info?enter_method=left_navigation). Other available endpoints are descriptive on the TikTok Developer page.

For video queries, we have chosen for this version to keep the field operation to be “EQ” on every field. Other field operations can be LT, LTE, GT, GTE and IN, but due to the time limit of this project, we kept it to EQ. We have also for now chosen to only have 1 string as input, so if you want a list of e.g. hashtag values, you can simply add another row of hashtag values. More about usage later down the page.

We recommend that you keep queries simple when using the GUI, but if you are extending our code, feel free to do whatever you wish to.

See the codebook here: https://developers.tiktok.com/doc/research-api-codebook?enter_method=left_navigation

## How-To Download
### Windows
If you have a Windows machine, please check if this is a 64-bit machine in your system settings. If so, the easiest installation will be to just download the executable file. If you wish to alter the source code, take a look at the other installation guides instead.

Navigate to the “Releases” section, and choose the newest that fits your machine. Download this zip-file, and unzip this file in a location that is easy for you to remember. Navigate into this unzipped file, and click on the file called “main”. The main file might be in a directory, also called main. If you are given a message that says you cannot run this program, try running it as administrator or give yourself permission to read and execute this under the files properties.

Double click the file called "main", this will immediately start the program. You can overlook the “_internal” folder, but take a note of the “data” folder next to the main.exe, as this is where your csv or excel files will be found later.

If you run into any problems using the main.exe file for Windows 64-bit, please contact Amalie. You can also download the entire source code and run it in an IDE.

If you wish to download the source code, please install Python from the official website. You also need an IDE to run this with, and we recommend to use Spyder. Navigate to the green button that says "<>Code", and download it as a zip file (or clone the repository: https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository). You need to unzip this .zip file, and place the unzipped folder in a place you can easily remember it (e.g. your Desktop). 

Open Spyder, and in the menu bar (on the top), find "Projects". Then choose "Open Project", and navigate to the folder inside your unzipped folder. There are two folders called "PEATA", and the top folder is the one you should open. Click the ">" symbol on the sub-folder also called "PEATA", and it should open multiple files. Press the file called "main.py", so it opens. Now you can run the file, with the green arrow located under "Debug" in the menu bar. This should run the program.

You will also have to install some packages, do this in the Spyder-terminal that is located to be bottom right (if this is your first time running the program, it should say "In [1]: ". Here, you must type these things, including the "!", and press enter:
- !pip install requests
- !pip install pandas
- !pip install openpyxl
- !pip install Pillow

Now, your program should be ready to run. See "Usage" for a guide on how to properly use our program.


### Mac
If you have a mac with apple M1/M2 chip, this version is for you! You can head over to the releases section in github and download the zip file called MacOs.zip. Make sure to save it somewhere easy to remember on your computer, such as your Desktop. Once the download is complete, double-click the zip file to unzip it. This will create a folder named main. Inside the main folder, you’ll find a file also named main. Try double-clicking this file to launch the program. Due to recent macOS security updates, you're likely to see a warning that says: "Apple could not verify ‘main’ is free of malware that may harm your Mac or compromise your privacy". This happens because the app is not signed by an Apple-registered developer. It’s safe to ignore this warning if you trust the source. When the warning appears, click the “?” icon in the dialog box. This will explain how you can fix the problem. You can go to settings into "privacy and security". Then scroll towards the bottom where it says "security". You’ll see a message saying the app was blocked. There will be an option to press a button that says "open anyway" for the main file. Try launching the file again and it should now open without the warning.

### Here is how to do that
If double-clicking the main file doesn’t work, you can try launching it through the Terminal instead. To do this, first open the Terminal application on your Mac. You can find the terminal app by searching terminal on your mac through spotlight. This will open a small black window with white text. This is the terminal. Then you can navigate to the location where you saved and unzipped the file. For example, if you saved it on your Desktop, you can type the following command: cd Desktop/main.  When you use pyInstaller on mac you have to make the file executable with the command "chmod +x main". When you have done that you will be able to launch the program by writing the following command "./main". The program takes some time to open, so you might have to wait for a while. Due to recent macOS security updates, you're likely to see a warning that says: "Apple could not verify ‘main’ is free of malware that may harm your Mac or compromise your privacy". This happens because the app is not signed by an Apple-registered developer. It’s safe to ignore this warning if you trust the source. When the warning appears, click the “?” icon in the dialog box. This will explain how you can fix the problem. You can go to settings into "privacy and security". Then scroll towards the bottom where it says "security". You’ll see a message saying the app was blocked. There will be an option to press a button that says "open anyway" for the main file. Try launching the file again and it should now open without the warning.


If you run into any problems using the main.exe file for Mac M1/M2 chip, please contact Oda. You can also download the entire source code and run it in an IDE.


## Usage
When you first start the program, either from a runnable file or from your IDE, the login page should appear immediately (or at least after a few seconds). 

You will first appear on a login page, where you have to enter your client credentials. This will test if your credentials are valid. If they aren’t, make sure you have entered the correct parameters. This is case sensitive, so we recommend copy-pasting, and do not include any special characters like “”. These client credentials are secret, and we do not save your client credentials in any way, they are only being used for the API-calls. If your credentials are valid, you will be passed on to the main interface where you can retrieve the data you want. You can find your client credentials from the TikTok Developer page. This page also lets you retry if you enter the wrong client credentials.

You will now be sent to the main page if the client credentials created a valid access token. Here, you can press <Escape> to exit the program at any time, and you will be prompted if you are sure. If you do, please remember to save your data as Excel or CSV file first, otherwise the data will be terminated with the program and you will have to redo the query.

On the top rectangle, you can choose which endpoint you want to fetch your data from. You will be able to fetch videos with your own filters, comments from a given video, and user info for a specific user.

For videos, you must enter a startdate and enddate, in the format YYYYMMDD. The enddate cannot be more than 30 days after the startdate. By default, username AND keyword filters are showing. However, you can change the AND-operation to NOT/OR, and change the field to whatever is available on the list. In the input field, you can enter what you like. You can also click “Add row” to add another filter, or “-” on the right side of the row to remove a filter. When you are ready, you can press “Submit”.

The progress bar will indicate when the computer is processing, and as long as it runs you are ensured that the program has not freezed. When the fetching is complete, you will be able to see a JSON-format output in the textbox. This can look messy, and it is not supposed to be readable, and is just an indicator to you that the contents were fetched from the endpoint. You can then press “Download as CSV” or “Download as Excel”, to download the data in your preferred format. 

For the comment queries, you must enter a video-id, which can be found in the search-bar of a video from tiktok.com. Example: www.tiktok.com/@stryketreneren/video/123456789. Copy and paste the numbers into the input-field, then download when the fetching has completed.


## Contributions
Amalie Nilsen, Oda Nøstdahl, Elin Eunjung Park, Ibrahim Khan.

## Licensing
Free to use
