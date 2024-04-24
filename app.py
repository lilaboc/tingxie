import streamlit as st
import asyncio
from tingxie import edge, playsound
import random


async def _main(word):
    # start = time.time()
    st.write(f"Current word: {word}")
    if word.strip() != "":
        media = await edge(word.strip(), slow=False)
        playsound(media)
        print(random.randint(0, 10))


st.title("Word Reader")

# User input
user_input = st.text_input("Enter words, separated by commas")

# Check if 'user_input' is in session_state (i.e., this is not the first run)
if 'user_input' in st.session_state:
    # Check if the input has changed
    if st.session_state.user_input != user_input:
        # Update the session_state
        st.session_state.words = user_input.split(",")

# Store the current input in session_state for comparison in the next run
st.session_state.user_input = user_input

# Initialize session state
if "words" not in st.session_state:
    st.session_state.words = []
if "index" not in st.session_state:
    st.session_state.index = 0

# Create four columns for the buttons
col1, col2, col3 = st.columns(3)

# Next button
if col1.button("Next"):
    # Split the user input into a list of words
    # st.session_state.words = user_input.split(",")
    # If the words list is empty, read "听写完了，干得好"
    if st.session_state.index >= len(st.session_state.words):
        asyncio.run(_main("听写完了，干得好"))
    # Call the _main function with the next word
    elif st.session_state.index < len(st.session_state.words):
        # Increment the index for the next word
        print("index", st.session_state.index)
        print(f"I am reading {st.session_state.words[st.session_state.index]}")
        # Display the current word
        asyncio.run(_main(st.session_state.words[st.session_state.index]))
        st.session_state.index += 1
# Previous button
if col2.button("Previous"):
    # Call the _main function with the previous word
    if st.session_state.index > 1:
        st.session_state.index -= 1
        asyncio.run(_main(st.session_state.words[st.session_state.index - 1]))


# Replay button
if col3.button("Replay"):
    # Call the _main function with the current word
    if st.session_state.index > 0:
        asyncio.run(_main(st.session_state.words[st.session_state.index - 1]))

