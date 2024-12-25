import streamlit as st
import openai

def chatbot_page():
    # Set your OpenAI API key here
    def query_fine_tuned_chat_model(prompt, model="ft:gpt-3.5-turbo-0125:personal:kidney:9nRl67jC"):
        """ Send a prompt to the fine-tuned chat model and get the response """
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=[{"role": "user", "content": prompt}]
            )
            return response['choices'][0]['message']['content'].strip()
        except Exception as e:
            return f"An error occurred: {str(e)}"

    st.title('💬 Chatbot')
    st.markdown("Solve your confusion about anti-rejection medications here.")
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        msg = query_fine_tuned_chat_model(prompt)
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)