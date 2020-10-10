import SessionState
import streamlit as st
import io

st.beta_set_page_config(
    page_icon=":shark:",
    layout="wide",

)

def pageZero(sesh):
    st.title('This is page zero! welcome')
    st.write('some text for zeroth page. Welcome to the app. Follow the nav buttons above to move forward and backwards one page')
    st.write('You won\'t be able to proceed until you complete all the tasks on this page\n')
    st.write('For example, try clicking Next with the box unchecked.')

def pageOne(sesh):
    st.title('page ONE')
    st.write('two')

def pageTwo(sesh):
    st.title('TWO')
    st.write('three')

sesh = SessionState.get(curr_page = 0)
PAGES = [pageZero, pageOne, pageTwo]
    
def main():
    ####SIDEBAR STUFF
    st.sidebar.title("this is an app:")

    st.sidebar.markdown('Might be easier to import the pageOne/pageTwo/pageThree from a separate file to make the code cleaner')

    #####MAIN PAGE NAV BAR:
    st.markdown(' ## Navigation')
    st.markdown('Click Next to go to the next page')
    if st.button('Back:'):
        sesh.curr_page = max(0, sesh.curr_page-1)
    if st.button('Next page:'):
        sesh.curr_page = min(len(PAGES)-1, sesh.curr_page+1)
    st.markdown('----------------------------------')


    #####MAIN PAGE APP:
    st.write('PAGE NUMBER:', sesh.curr_page)
    page_turning_function = PAGES[sesh.curr_page]
    st.write(sesh.curr_page)
    page_turning_function(sesh)

if __name__=='__main__':
    main()
