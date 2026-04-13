import streamlit as st
import requests

st.title("Song Lyrics")
st.write("Welcome to the Song Lyrics app! Here you can find the lyrics to every song. Enjoy singing along!")

query = st.text_input("Song title:")
submit = st.button("Submit")

# Run search only when submit is clicked
if submit and query:
    url = "https://lrclib.net/api/search"
    params = {"q": query}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        results = response.json()
        if results:
            # Save results in session state so they persist
            st.session_state["results"] = results
        else:
            st.info("No results found. Try another song title.")
    else:
        st.error("Failed to fetch lyrics. Please try again.")

# Show dropdown if results exist in session state
if "results" in st.session_state and st.session_state["results"]:
    options = {
        f"{song.get('trackName', 'Unknown Title')} - {song.get('artistName', 'Unknown Artist')}": song
        for song in st.session_state["results"]
    }

    choice = st.selectbox("Select a song:", list(options.keys()))

    if choice:
        selected_song = options[choice]
        st.subheader(choice)
        lyrics = selected_song.get("syncedLyrics") or selected_song.get("plainLyrics")
        if lyrics:
            st.text(lyrics)
        else:
            st.warning("Lyrics not available for this track.")