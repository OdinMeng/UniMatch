import streamlit as st

def about_page():
    st.title("About Us")

    # Subheader About UniMatch
    st.subheader("**About UniMatch**")
    st.write("""
            UniMatch is a company created with the main goal of helping graduated students
            find suitable universities and/or areas of study, assisting their transition to higher
            education. It intends to achieve this goal by making the best use of LLMs and
            generative AI technologies to provide the users with a new level of personalization
            and to find information which would be hard to access.

            The platform provides information about a wide range of university courses and their
            subjects, and any requirements for applying. It also aids students discover
            international mobility opportunities, and applicable scholarships for any area of
            study. UniMatch is designed for a wide range of users, including high school
            graduates looking for undergraduate programs, undergraduates seeking Master’s
            degrees, and those interested in pursuing PhDs. By making the process simpler and
            more personalized, UniMatch ensures students can make better decisions for their
            education and future careers.
        """)

    # Mission Statement
    st.subheader("**MISSION STATEMENT**")
    st.write("""
            The mission of UniMatch is to enable students and aspiring academics by guiding
            them towards academic paths, whether the person is searching for a university, Master’s programmes,
            scholarship, Erasmus+ programmes, etc. By helping these people find the right fit in the academic world,
            UniMatch contributes to a smaller dropout rate and higher satisfaction in these programs,
            ensuring students are allocated in tailored programs to achieve their individual goals.
        """)

    # Vision Statement
    st.subheader("**VISION STATEMENT**")
    st.write("""
            UniMatch aims to become a viable and mainstream tool for those who need guidance
            choosing where and/or what to study. You can find more information in the Future Perspectives section below.
        """)

    # Company Values
    st.subheader("**COMPANY VALUES**")
    st.write("""
            UniMatch is committed to the following values:
            - **Inclusion:** Our solution helps every kind of student with guidance to have guaranteed access to
              university-related matters, i.e., finding scholarships programmes.
            - **Internationalization:** One of our features is to help students look for international opportunities or
              universities abroad.
            - **Education:** The main goal of UniMatch is to provide students with guidance in their higher education path.
            - **Innovation:** We achieve our goals through innovative technologies, namely LLMs and generative AI.
        """)

    # How was UniMatch born?
    st.subheader("**How was UniMatch born?**")
    st.write("""
            UniMatch is a startup born as a university project for the Capstone Project course (at NOVA IMS, Lisbon),
            driven by the desire to address a common challenge faced by students.

            The idea came from the creators seeing many of their peers struggle to choose a university,
            often feeling lost and unsure. UniMatch was created to make this process easier by providing personalized
            advice to help students pick the right university and program for their interests and goals.
        """)

    # Future Perspectives
    st.subheader("**Future Perspectives**")
    st.write("""
            UniMatch is a small startup focused on showcasing how generative AI can solve
            industry challenges, such as helping students make informed decisions about their
            education or streamlining administrative processes in universities.

            Currently, the internal database contains only basic information—such as the name,
            location, and main website—on about 0.21% of universities worldwide, and only 20%
            of these have detailed data on courses, prerequisites, scholarships, and other relevant
            details. As a result, UniMatch is still in the early stages of development.

            However, we love to believe that the potential is there: UniMatch could grow into a
            mainstream tool for students by providing personalized university recommendations
            based on their unique preferences, academic background, and career goals, offering
            detailed insights to help them make well-informed decisions about their future.

            In the future, we might expand our database to cover all universities in the European
            Union and add new features like multimedia support.
        """)

    # Team Section in Columns
    st.subheader("About the Team")
    col1, col2 = st.columns(2)

    with col1:
        st.write("### Dino Meng")
        st.write("""
                - Is a Italian exchange student from the University of Trieste,
                  pursuing a bachelor's degree in "Artificial Intelligence & Data Analytics".
                - Interests: pure mathematics, machine learning, coding, and generative AI technologies.
            """)

        st.write("### Lourenço Passeiro")
        st.write("""
                - Third-year student at NOVA IMS pursuing a degree in Data Science.
                - Passionate about machine learning, with aspirations to create impactful models for decision-making.
                - Experienced in regression, classification, clustering, and deep learning.
            """)

        st.write("### Miguel Marques")
        st.write("""
                - Third-year student at NOVA IMS pursuing a degree in Data Science.
                - Enthusiast in data science and databases, with a strong focus on insights extraction.
                - Extensive experience with SQL and database optimization.
            """)

    with col2:
        st.write("### Peter Lekszycki")
        st.write("""
                - Third-year student at NOVA IMS pursuing a degree in Data Science.
                - Passionate about entrepreneurship and using data for real-world innovation.
                - Aspires to create a data-centric startup leveraging AI technologies.
            """)

        st.write("### Tomás Gonçalves")
        st.write("""
                - Third-year student at NOVA IMS pursuing a degree in Data Science.
                - Focuses on data analytics and generating business insights for decision-making.
                - Experienced in data cleaning, EDA, and visualization using Python, SQL, and Power BI.
            """)

