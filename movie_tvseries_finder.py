import os
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
import json
import requests
from dotenv import load_dotenv
import streamlit as st
import contextlib
import io

# Set up the environment variables
load_dotenv()

# Access the API keys
os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')
os.environ["OMDB_API_KEY"] = os.getenv('OMDB_API_KEY')

# Initialise the language model
llm = ChatGroq(
    model = "llama-3.3-70b-versatile",
    temperature=0.7
)

# Define the search prompt
search_prompt = PromptTemplate(
    input_variables=["user_input"],
    template="""The user is describing a movie or a tv series they vaguely remember.

    Description:
    "{user_input}"

    Analyze if they are describing a TV series or a movie.

    Identify:
    - Suggested Titles
    - Probable Actors
    - Probable Genres
    - Content Type (movie or series)

    Output:

    Return it in JSON format like:
    {{
      "titles": [...],
      "actors": [...],
      "genres": [...],
      "type": "movie" or "series"
    }}
"""
)

# Extract a list of keywords necessary for OMDb search from the user's vague description
def extract_media_clues(user_input):
    """Get a vague description from the user then suggest top three movies or TV series that fit the description.

    Args:
        user_input (str): User's vague description about content they are looking for.

    Returns:
        dict: Structured information about the media.
    """
    response = (search_prompt | llm).invoke({"user_input": user_input}).content

    # Try to parse the response as JSON
    try:
        # Remove any markdown formatting that might be present
        if "```json" in response:
            response = response.split("```json")[1].split("```")[0].strip()
        elif "```" in response:
            response = response.split("```")[1].split("```")[0].strip()

        return json.loads(response)
    except json.JSONDecodeError:
        print("Error parsing JSON response. Raw response:")
        print(response)
        # Return a basic structure if parsing fails
        return {"titles": [], "actors": [], "genres": [], "type": "movie"}

# Search with the keywords
def search_omdb(query, content_type=None):
    OMDB_API_KEY = os.environ.get("OMDB_API_KEY")

    # Add type parameter if specified
    type_param = ""
    if content_type in ["movie", "series"]:
        type_param = f"&type={content_type}"

    url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&s={query}{type_param}"

    try:
        response = requests.get(url).json()
        if response.get("Response") == "False":
            print(f"No results found for query: {query}")
            return []
        return response.get("Search", [])
    except Exception as e:
        print(f"Error searching OMDB: {e}")
        return []

# Get detailed information about a movie or TV series using its IMDb ID
def get_media_details(imdb_id):
    OMDB_API_KEY = os.environ.get("OMDB_API_KEY")
    url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&i={imdb_id}&plot=short"

    try:
        return requests.get(url).json()
    except Exception as e:
        print(f"Error getting media details: {e}")
        return {}

# Display movie or TV series information in Streamlit
def display_media(media):
    if not media or media.get("Response") == "False":
        st.warning("No valid media data to display")
        return

    # Use a default image if poster is N/A
    poster = media.get('Poster', '')
    if poster == 'N/A' or not poster:
        poster = "https://via.placeholder.com/150x225?text=No+Poster"

    # Determine if it's a movie or series
    media_type = media.get('Type', 'Unknown')
    media_type_display = "TV Series" if media_type == "series" else "Movie"
    
    # Create a two-column layout
    col1, col2 = st.columns([1, 2])
    
    # Display poster in left column
    with col1:
        st.image(poster, width=150)
    
    # Display information in right column
    with col2:
        st.header(media.get('Title', 'Unknown Title'))
        st.subheader(f"{media.get('Year', 'Unknown Year')} • {media_type_display}")
        
        st.write(f"**Genre:** {media.get('Genre', 'Unknown')}")
        
        # Add seasons info if it's a series
        if media_type == "series" and media.get('totalSeasons'):
            st.write(f"**Seasons:** {media.get('totalSeasons')}")
        
        st.write(f"**IMDb Rating:** {media.get('imdbRating', 'N/A')}/10")
        st.write(f"**Cast:** {media.get('Actors', 'Unknown')}")
        
        st.write("**Plot:**")
        st.write(media.get('Plot', 'No plot available'))    

# Search for media by actor name
def search_by_actor(actor_name, content_type=None):
    results = search_omdb(actor_name, content_type)
    return results

# Main function to execute the media search process
def search_media(user_input):
    # Extract keywords from user's vague description that could help in our search
    print("🔍 Analyzing your description...")
    media_clues = extract_media_clues(user_input)

    # Get the keyword (either "movie" or "TV series")
    content_type = media_clues.get("type", "").lower()
    if content_type not in ["movie", "series"]:
        content_type = None  # Search for both if not specified

    print(f"🎬 Looking for {'TV series' if content_type == 'series' else 'movies' if content_type == 'movie' else 'content'} matching: {media_clues['titles']}")

    found_media = set()  # To avoid duplicates
    media_count = 0

    # First search by titles
    for title in media_clues.get("titles", []):
        search_results = search_omdb(title, content_type)
        for result in search_results[:3]:  # Limit to top 3 per title
            if result["imdbID"] not in found_media and media_count < 3:
                found_media.add(result["imdbID"])
                details = get_media_details(result["imdbID"])
                display_media(details)
                media_count += 1
                if media_count >= 3:
                    break

    # If we haven't found 3 results yet, try searching by actors
    if media_count < 3:
        for actor in media_clues.get("actors", []):
            if media_count >= 3:
                break
            search_results = search_by_actor(actor, content_type)
            for result in search_results[:3]:
                if result["imdbID"] not in found_media and media_count < 3:
                    found_media.add(result["imdbID"])
                    details = get_media_details(result["imdbID"])
                    display_media(details)
                    media_count += 1
                    if media_count >= 3:
                        break

    if not found_media:
        print("Sorry, no matching movies or TV shows found. Try providing more details or different keywords.")

# print() helper function to display the captured output of print statements in streamlit
def capture_print_output(func, *args, **kwargs):
    # Redirect stdout to a string buffer
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        result = func(*args, **kwargs)
    
    # Display the captured output in Streamlit
    output_str = output.getvalue()
    if output_str:
        st.text(output_str)
    
    return result

# Streamlit UI
st.title('Movie and TV Series Finder')

# Welcome message
st.markdown("""
Hey there! 👋 I’m your Movie & TV Series Finder.
Give me as much information as you can about the movie or TV series you are looking for, no matter how vague:
about the plot, the actors' names, the location, the setting, some words in the title,...etc.
I will then give you top three matches that fit your description.
""")

# Create session state to store variables
if 'current_step' not in st.session_state:
    st.session_state.current_step = 'vague_description'
if 'vague_description' not in st.session_state:
    st.session_state.vague_description = None
if 'media_clues' not in st.session_state:
    st.session_state.media_clues = None

# Step 1: Get a vague description of a movie from the user
if st.session_state.current_step == 'vague_description':
    vague_description_input = st.text_input("Describe it to me: ", key="vague_description_input")
    if st.button("Search", key="description_button"):
        if vague_description_input:
            st.session_state.vague_description = vague_description_input
            st.spinner(f'Description: {vague_description_input}')
            st.session_state.current_step = 'process'
            st.rerun()

# Step 2: Process user input and produce results
elif st.session_state.current_step == 'process':

    # Validate that we have all required data
    if not (st.session_state.vague_description):
        st.session_state.current_step = 'vague_description'
        st.rerun()
    try:
        # Fetch book information
        with st.spinner('🔍 Analyzing your description...'):
            st.session_state.media_clues = capture_print_output(
                search_media,
                st.session_state.vague_description
            )
            st.success('Successfully received book details')        
   
        # Reset button
        if st.button("Start over", key="reset_button"):
            for key in st.session_state.keys():
                del st.session_state[key]
            st.session_state.current_step = 'vague_description'  # Set initial step explicitly
            st.rerun()
            
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        if st.button("Try again", key="error_button"):
            for key in st.session_state.keys():
                del st.session_state[key]
            st.rerun()