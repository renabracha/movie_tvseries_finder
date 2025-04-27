# Movie and TV Series Finder

## Acknowledgment
I would like to thank the following individuals and organisations that made this project possible. 
* Groq for providing me free access to their API key and thereby allowing me to gain hands-on experience in making API calls without having to constantly worry about token limits.
* OMDB API for allowing me to obtain information about films and TV series using their API free of charge.

## Abstract
I often remember the basic plot for many films and TV series or which actors starred in them, but find it difficult to recall their titles. The program takes a vague description of a movies or a TV series and suggests three possibilities, all only with prompts. 
<br>
The application follows the sequence below:
1. Ask for the description of a film or a TV series from the user, no matter how vague. 
2. Analyze the description and list possible titles, actors, genres, and content type (whether it is a movie or a TV series).
3. Search in the OMDB database by the title and content type to obtain the IMDb ID.
4. Get the movie/TV series details using the IMDb ID. 

# Installation
To run movie_tvseries_finder.py, do the following:

### Step 1. Place the files in a folder. 
1. Place the `.py` file in a local folder (e.g. `C:\temp\movie_tvseries_finder`).
2. Create a file called `.env` and place the GROQ API key in the following format:
	`GROQ_API_KEY = <groq_api_key>`
  `OMDB_API_KEY = <omdb_api_key>`
3. Place the `.env` file in the same local folder. 

### Step 2. Install Python. 
1. In Windows, open the Command Prompt window.
2. Make sure Python is installed. In the Command Prompt window, type:
	`python --version`
If you get an error or "Python is not recognized", you need to install Python:
	1. Go to `https://www.python.org/downloads/`.
	2. Download the latest Python installer for Windows
	3. Run the installer and make sure to check `Add Python to PATH` during installation

### Step 3. Set up a virtual environment. 
This keeps your project dependencies isolated:
1. In the Command Prompt window, go to the script folder. Type:<br>
	`cd C:\<path to your script folder>`
2. In the Command Prompt, create a Python virtual environment named `movie_tvseries_finder_env`.<br>
	`python -m venv movie_tvseries_finder_env`
3. In the Command Prompt, activate the Python virtual environment.<br>
	`movie_tvseries_finder_env\Scripts\activate`
4. Install the required dependencies.<br>
  `pip install -r requirements.txt`

### Step 4. Install the required packages. 
1. In the Command Prompt window, type:<br>
	`pip install python-dotenv groq langchain langchain_groq streamlit`

### Step 5. Run the script. 
1. In the Command Prompt window, run the Streamlit application. Type:<br>
	`streamlit run movie_tvseries_finder.py`
<br>
<br>
This will start a local web server and open the application in your browser. Press the Analyse button to view the results. 

## Web app in action
![Alt text for screen reader](https://github.com/renabracha/movie_tvseries_finder/blob/main/screenshot_1.JPG?raw=true)
![Alt text for screen reader](https://github.com/renabracha/movie_tvseries_finder/blob/main/screenshot_2.JPG?raw=true)