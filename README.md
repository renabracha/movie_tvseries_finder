# Movie and TV Series Finder

## Acknowledgment
I would like to thank the following individuals and organisations that made this project possible. 
* Groq for providing me free access to their API key and thereby allowing me to gain hands-on experience in making API calls without having to constantly worry about token limits.
* OMDB API for allowing me to obtain information about films and TV series using their API free of charge.

## Abstract
I often remember the basic plot of a movie or TV series - or which actors starred in it — but struggle to recall the title. This program takes a vague description and returns three possible matches, using only prompt-based logic without complex backend logic or search indexing.

<br>

The application follows this sequence:
1. Accept a vague description of a movie or TV series from the user.
2. Use a prompt to extract likely titles, actors, genres, and the content type (movie or TV series).
3. Query the OMDb database using the predicted title and content type to retrieve the IMDb ID.
4. Fetch the full details of the matched titles using the IMDb ID.

## Development Notes
* This project showcases how effectively large language models (LLMs) can infer structured, searchable metadata - such as titles, actors, and genres - from ambiguous natural language input.
* It also solidified my comfort working with live APIs; in this case, querying the OMDb API using an API key.

## Installation
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

### Step 4. Run the script. 
1. In the Command Prompt window, run the Streamlit application. Type:<br>
	`streamlit run movie_tvseries_finder.py`
<br>
<br>
This will start a local web server and open the application in your browser. Press the Analyse button to view the results. 

## Web app in action
![Alt text for screen reader](https://github.com/renabracha/movie_tvseries_finder/blob/main/screenshot_1.JPG?raw=true)
![Alt text for screen reader](https://github.com/renabracha/movie_tvseries_finder/blob/main/screenshot_2.JPG?raw=true)