import streamlit as st

from streamlit_event_hook import init

init()

st.title("Hahaha")

st.markdown('''
<style>
.my_link {
    word-break: break-word;
    margin-bottom: 0px;
}

.my_link:hover {
    text-decoration: none;
}

.my_link:active {
}

.my_link:visited {
}
</style>
''', unsafe_allow_html=True)


def p2():
    st.write("p2")


st.page_link(st.Page(p2), label="a_link")
