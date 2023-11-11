import streamlit as st
from pydub import AudioSegment
import numpy as np
import io

def get_loudest_moments(audio_segment, num_moments=15):
    # Break audio into 1-second chunks
    chunk_length_ms = 1000 # pydub calculates in millisec
    chunks = make_chunks(audio_segment, chunk_length_ms)
    
    # Calculate the loudness of each chunk
    loudness = [chunk.dBFS for chunk in chunks]

    # Find the indices of the 'num_moments' loudest chunks
    loudest_indices = np.argsort(loudness)[-num_moments:]

    # Calculate times (in seconds) of these chunks
    loudest_times = [i for i in loudest_indices]
    return sorted(loudest_times)

st.title('MP3 Loudness Analyzer')

uploaded_file = st.file_uploader("Upload an MP3 file", type=['mp3'])

if uploaded_file is not None:
    # Read the uploaded audio file
    audio_bytes = io.BytesIO(uploaded_file.read())
    audio = AudioSegment.from_file(audio_bytes, format="mp3")

    # Process the audio file
    loudest_moments = get_loudest_moments(audio, 15)

    # Display the results
    st.write("Loudest moments in the audio (in seconds):")
    for moment in loudest_moments:
        st.write(moment)
