import streamlit as st
from UniMatch.data.register import register, handle_registration
from UniMatch.data.user_info import modify_user_preferences
from UniMatch.data.database_auxiliars import get_areas, get_countries
import time

# Register Page
def register_page():
    countries = get_countries()
    # Add None to countries
    countries[None] = 'None'

    areas = get_areas()
    areas[None] = 'None'

    st.title("Register")
    with st.form("register_form"):
        # TO DO:
        # Add age
        # Add Country Selection
        # Add Education Level
        # Add Main Area Selection
        payload = {}

        st.header("Basic Information")
        st.markdown("Before proceeding to know about your detailed preferences, UniMatch needs to know about essential information about you.")
        username = st.text_input("Choose a Username \*")
        password = st.text_input("Choose a Password \*", type="password")
        age = st.number_input("Insert your age", min_value=1, max_value=120, step=1)
        country = st.selectbox(options=countries.keys(), label='Choose your country', format_func=(lambda code: countries[code]), index=151) # 151 defaults to none
        education_level = st.pills(options=["High School", "Bachelor's Degree", "Master's Degree", "PhD"], label="Choose your current education level")
        area = st.pills(options=areas.keys(), label = "Choose your main area", format_func=(lambda key: areas[key]), default=1)        

        payload['username'] = username
        payload['password'] = password
        payload['educationlevel'] = education_level
        payload['age'] = age
        payload['countrycode'] = country
        payload['mainarea'] = area

        st.header("User Preferences")
        st.markdown("""Now you can add your user preferences! You have three free fields, where you can insert any text onto it. Moreover, you can decide their importance by changing their weights!
                    
**Note:** Make sure that these weights sum to 100. If not, an error will occur.""")
        
        c1 = st.columns([4,1])
        c2 = st.columns(2)
        c3 = st.columns(2)

        p1 = c1[0].text_input("First Preference")
        w1 = c1[1].number_input("", min_value=0, max_value=100, value=33)

        c2 = st.columns([4,1])
        p2 = c2[0].text_input("Second Preference")
        w2 = c2[1].number_input(" ", min_value=0, max_value=100, value=33)

        c3 = st.columns([4,1])
        p3 = c3[0].text_input("Third Preference")
        w3 = c3[1].number_input("  ", min_value=0, max_value=100, value=33)
        
        # Create Preferences Payload
        preferences_payload = {}
        preferences_payload['preferences'] = [p1, p2, p3]
        preferences_payload['weights'] = [w1, w2, w3]

        register_button = st.form_submit_button("Register")
        st.write("*\* Obligatory field*")

    if st.button("Back"):
        st.session_state["show_register"] = False
        st.rerun()

    if register_button:
        # check weights before registering
        error_flag = False
        if w1 + w2 + w3 != 100:
            st.error("Invalid Preferences Weight")
            error_flag = True

        if not error_flag:
            result = register(**payload)

            if result > 0:
                st.session_state["logged_in"] = True
                st.session_state["current_user"] = username
                st.session_state["show_login"] = False
                st.session_state['user_id'] = result
                st.success(handle_registration(result))
                time.sleep(1)
                st.rerun()

            else:
                st.error(handle_registration(result))

            # Insert Preferences
            if secondary_result := modify_user_preferences(result, preferences_payload) != 0:
                st.error("Error in inserting user preferences")
            
            else:
                pass

            
