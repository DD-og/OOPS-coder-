import streamlit as st
import groq

# Set up the Groq API client
groq_api_key = "your key"  # Replace with your actual Groq API key
client = groq.Client(api_key=groq_api_key)

# Streamlit UI
st.title("OOP Concept Code Generator")
st.write("Ask for any OOP concept, and I'll provide the corresponding Python code!")

# User input
user_input = st.text_input("Enter an OOP concept (e.g., 'inheritance', 'encapsulation', 'polymorphism'):")

# Add a sidebar for additional options
with st.sidebar:
    st.header("Configuration")
    temperature = st.slider("Creativity Level", 0.0, 1.0, 0.3, 0.1, 
                          help="Higher values make the output more creative but less focused")
    max_tokens = st.slider("Maximum Response Length", 100, 1000, 500, 50,
                          help="Maximum length of the generated response")
    show_explanation = st.checkbox("Show Explanation", value=True,
                                 help="Toggle explanation visibility")

if user_input:
    # Generate a prompt for the Groq API
    prompt = f"""Provide a Python code example for the OOP concept: {user_input}.
    Make sure the code is well-commented and follows best practices.
    Include practical, real-world examples.
    Explain the code briefly and highlight key concepts."""

    # Call the Groq API
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=temperature,
        )

        # Display the response
        st.write("### Generated Code:")
        st.code(response.choices[0].message.content, language="python")

        if show_explanation:
            st.write("### Explanation:")
            st.write(response.choices[0].message.content)

        # Add copy button for the code
        if st.button("Copy Code to Clipboard"):
            st.write("Code copied to clipboard!")
            st.session_state.clipboard = response.choices[0].message.content

        # Add feedback mechanism
        st.write("### Was this helpful?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("👍 Yes"):
                st.success("Thanks for your feedback!")
        with col2:
            if st.button("👎 No"):
                feedback = st.text_area("Please let us know how we can improve:")
                if feedback:
                    st.success("Thank you for your feedback!")
    except Exception as e:
        st.error(f"An error occurred: {e}")
