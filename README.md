# UniMatch

This is a complete description of the project *UniMatch* created for the *Capstone Project* at NOVA IMS Information Management School.

## 1. Project Overview 

- **Company Name**: UniMatch
- **Group 10**:
   - Dino Meng - 20241265
   - Lourenço Passeiro - 20221838
   - Miguel Marques - 20221839
   - Peter Lekszycki - 20221840
   - Tomás Gonçalves - 20221894
- **Description**:  
  UniMatch is an AI-powered platform to guide students in their higher education journey. It provides a personalized search engine for universities and customized recommendations on universities (called *matches*); moreover, it is also able to analyze external documents and answer specific questions about it. It interacts with users through a friendly chatbot who is able to query the universities database and provide tailored answers. The overall objective of UniMatch is to offer students a starting point for their path in higher education, enabling them to explore their options in a deeper manner leveraging AI.

<p align="center">
  <img src="images/UniMatch logotipo.png" />
</p>

---

## 2. Repository Structure: Deviations from the Template
We have used the project template for the Capstone Project course and modified it to accomodate our features. 

```python
UniMatch
├───images
└───UniMatch
    ├───chatbot
    │   ├───agents
    │   ├───chains
    │   ├───chatlogs
    │   ├───rag
    │   └───router
    ├───data
    │   ├───database
    │   ├───extracted_data
    │   ├───pdf
    │   └───user_files
    └───pages
        └───images        
```

In particular we have made the following changes:
+ We added `UniMatch/UniMatch/chatbot/chatlogs` to add chatlogs, which can be used to save and laod a user's chat conversation with the chatbot
+ We added `UniMatch/UniMatch/chatbot/agents` to add a folder to store the agent (used to manage user's personal information) and his tools
+ We added `UniMatch/UniMatch/data/extracted_data` containing raw Excel files to show which information we have extracted
+ We added `UniMatch/UniMatch/data/user_files` to allow users to upload their own PDF files for the chatbot to analyze
+ We added `UniMatch/images` to let us to load images in this README.md file
+ We added `UniMatch/pages/images` to let us load images in the website application 

---

## 3. How to Test the Chatbot 

### 3.1 Prerequisites

- **Python Version**: Python 3.12.7

- **Dependencies**: If you wish to run UniMatch without using any dedicated environments, you can manually install the following libraries:

**LangChain Ecosystem:**  
`langchain=0.3.13`, `langchain-openai=0.2.10`, `langchain-pinecone=0.2.0`, `langchain-community=0.3.4`

**Pinecone Integration:**  
`pinecone-client=5.0.1`

**OpenAI Integration:**  
`openai=1.55.3`

**Data Processing:**  
`pandas=2.2.3`, `openpyxl=3.1.3`

- **Environment Setup**: To set up the Anaconda environment, open the command line at the base folder (`./UniMatch`) and type the following commands:
  - `conda create -n UniMatch python=3.12.7`
  - `conda activate UniMatch`
  - `pip install -r requirements.txt`
  If any prompts come out, type `y` to proceed.
  
  If you wish to uninstall the environment, you can simply type `conda remove -n UniMatch --all` and type `y` to every prompt. Do not forget to de-activate your environment by typing `conda deactivate`!
  
### 3.2 How to Run the Chatbot

Assuming the environment set up has been done, the user can run the web-based app by simply typing `streamlit run app.py`.

Users can log-in into a dummy user with the following credentials:
- username: `Alice`
- password: `P@ssw0rd!`

However, let it be noted that it is not strictly necessary to log in to interact with the chatbot; it is possible use the chatbot in *Guest Mode*, meaning without being logged in. However this is meant to be as some sort of *"trial version"* of the product, as most of the crucial features involving personalization are unavailable.

Alternatively, if a more tech-savvy approach is preferred, you can run the CLI-based interface by typing `python app_cli.py`. However this type is interface is more limited and features involving user registration and personalization are unavailable.

## 4. Database Schema 

### 4.1 Database Overview and Schema Diagram

UniMatch uses the following database schema to store information about users and universities:

<p align="center">
  <img src="images/database_schema.svg" />
</p>

### 4.2 Table Descriptions
Here is a detailed description of the database schema given above.

**1. Users Table**
- _IDUser_ (`INTEGER`): Unique identifier for the user. This will be used as a key for the bot.
- _Username_ (`TEXT`): User's chosen username. This will be used as a unique identifier for the login and registration system.
- _Age_ (`INTEGER`): User's age.
- _Password_ (`TEXT`): User's password.
- _CountryCode_ (`TEXT`): Code referencing the user's country.
- _CountryOfArrival_ (`TEXT`): The country where the user is arriving or located.
- _MainArea_ (`INTEGER`): Foreign key referencing the main area of interest (linked to `Areas`).

**2. UserPreferences Table**
- _IDPreference_ (`INTEGER`): Unique identifier for the preference.
- _IDUser_ (`INTEGER`): Foreign key referencing the user.
- _Preferences_ (`TEXT`): Description of the user's preferences.
- _Weight_ (`INTEGER`): Priority or weight assigned to the preference. All weights for each user must sum to 100; this will be checked with back-end external functions.

**3. Universities Table**
- _IDUniversity_ (`INTEGER`): Unique identifier for the university.
- _CountryCode_ (`TEXT`): Code of the country where the university is located.
- _UniversityName_ (`TEXT`): Name of the university.
- _MainWebsite_ (`TEXT`): Main website of the university.

**4. Courses Table**
- _IDCourse_ (`INTEGER`): Unique identifier for the course.
- _IDUniversity_ (`INTEGER`): Foreign key referencing the university.
- _CourseName_ (`TEXT`): Name of the course.
- _CourseDescription_ (`TEXT`): Description of the course.
- _Duration_ (`INTEGER`): Duration of the course (in years).
- _Tuition_ (`INTEGER`): Tuition fees for the course.
- _AcceptsInternationals_ (`BOOLEAN`): Whether the course accepts international students or not.
- _Area_ (`INTEGER`): Foreign key referencing the area (linked to `Areas`).
- _Language_ (`TEXT`): Language of instruction for the course. Can be more than one language.
- Note: Most fields are optional, as information could not be available for us.

**5. Subjects Table**
- _IDSubject_ (`INTEGER`): Unique identifier for the subject.
- _IDCourse_ (`INTEGER`): Foreign key referencing the course.
- _SubjectName_ (`TEXT`): Name of the subject.
- _SubjectDescription_ (`TEXT`): Description of the subject.
- _ECTS_ (`REAL`): Number of European Credit Transfer and Accumulation System credits.
- _WeekHours_ (`REAL`): Weekly hours allocated for the subject.
- _Semester_ (`REAL`): The semester in which the subject is offered.
- Note: Most fields are optional, as information could not be available for us.

**6. Internationals Table**
- _IDInternational_ (`INTEGER`): Unique identifier for international data.
- _IDUniversity_ (`INTEGER`): Foreign key referencing the university.
- _Destination_ (`TEXT`): Destination country or university.

**7. Scholarships Table**
- _IDScholarship_ (`INTEGER`): Unique identifier for the scholarship.
- _IDUniversity_ (`INTEGER`): Foreign key referencing the university.
- _ScholarshipName_ (`TEXT`): Name of the scholarship.
- _MaxAmount_ (`REAL`): Maximum monetary amount covered.
- _MinAmount_ (`REAL`): Minimum monetary amount covered.
- _Benefits_ (`TEXT`): Description of the benefits offered.
- Note: if the scholarship offers a constant amount, we put _MaxAmount_ = _MinAmount_

**8. Requisites Table**
- _IDRequisite_ (`INTEGER`): Unique identifier for the requisite.
- _IDCourse_ (`INTEGER`): Foreign key referencing the course.
- _IDScholarship_ (`INTEGER`): Foreign key referencing the scholarship.
- _Requisites_ (`TEXT`): Requirements or prerequisites.
- Note: Usually a requisite references either a course or a scholarship. Therefore _IDCourse_ and _IDScholarship_ are both optional fields, but only one should be non-null.

**9. Areas Table**
- _IDArea_ (`INTEGER`): Unique identifier for the area.
- _AreaName_ (`TEXT`): Name of the area 

**10. Matches Table**
- _IDUser_ (`INTEGER`): Foreign key referencing the user.
- _IDScholarship_ (`INTEGER`): Foreign key referencing scholarships.


**11. Countries Table**
- _CountryCode_ (`TEXT`): Unique code for the country (e.g., ISO country code).
- _Country_ (`TEXT`): Name of the country.
- Note: this is a simple hash-table to convert country codes to countries.

---

## 5. User Intentions 

### 5.1 Implemented Intentions

UniMatch's chatbot is designed to handle the following user intentions:

- **Manage Personal Information**: User either requests to modify his personal information or asks the chatbot to describe himself, including user preferences.
- **Search Universities, Courses, Scholarships and International Opportunities**: User wants to search for universities, courses, scholarships or international opportunities available in the system's database and a brief description of it.
- **Make Matches**: User wants the chatbot to make matches for his universities, giving a good amount of possibilities and starting points.
- **Query Matches**: User wants to search the matches that the chatbot has previously done.
- **Upload External Files**: User wants to upload external files containing information about universities, courses or similarly related topics. 
- **Analyze External Files**: Having uploaded the external files, user wants to analyze the file by making some specific questions about it.
- **Get Company Information**: User wants to receive information about the company UniMatch and what it offers.
- **Chitchat**: User intends to simply make chatter with the chatbot. 

### 5.2 How to Test Each Intention

- **Manage Personal Information**
1. Who am I? -> The chatbot should provide a clear and concise profile of yourself.
2. Change my age to 25 -> The chatbot should successfully modify your age to 25 and communicate you such result.
3. I want to change my user preferences; now I prefer to live in a chill town and study in a natural campus -> The chabot should successfully change your user preferences and communicate such results.

- **Search Universities, Courses, Scholarships and International Opportunities**
1. Do you have universities with courses in Artificial Intelligence? -> The chatbot should successfully provide a tailored answer describing the Bachelor's degree course in "Artificial Intelligence and Data Analytics" at the University of Trieste. 
2. Do you have scholarships in Trieste? -> The chatbot successfully finds a scholarship and describes it
3. Give me universities with courses in magic -> The bot tells the user that no such university could be found and encourages the user to consider into looking other programmes

- **Make Matches**
Note: this is a lengthy operation and could take minutes for the chatbot to complete.

1. I want some matches for universities. Look for universities in Hungary -> The chatbot will return five possible matches, representing different courses in the Technical University of Budapest.
2. Make me matches, with universities in Draconia -> Error occurs due to the absurdity of the input and the chatbot will communicate such result
3. Make matches for universities, make it various universities -> The chatbot will successfully make matches with five universities, each being a different course of a different university.

- **Query Maches**
1. Query my previously-made matches. -> The chabot will successfully query your previously-made matches, the descriptions being almost identical 
2. Look at my previous matches and focus on explaining why they are a good fit for me -> Same as above, but the chatbot will explain the compatibility between your preferences and the university more clearly, all while recalling your user preferences.
3. Search my matches and find potential incompatibilities -> Same as above, but the chatbot tries to explain some potential incompatibilities with the user preferences

- **Upload External Files**
This is handled through user UI

- **Analyze External Files**
Note: Upload the following files to the chatbot for testing the below prompts
- *PDF*: https://sites.units.it/internationalia/moduli/Information%20sheet%20Trieste.pdf
- *Website Link*: https://www.ulisboa.pt/en/curso/mestrado/data-science

1. I have uploaded a PDF file. What are the main campuses? -> Bot successfully finds the answer, indicating relevant elements
2. I have uploaded a link to a website. What is the course about? -> Same as above, but with another type of content
3. I have uploaded a PDF file. What is 1+1? -> Bot says that he couldn't find the answer in the context

- **Get Company Information**
1. What is UniMatch? -> Bot successfully describes what is UniMatch
2. Is is true that UniMatch is expensive? -> Bot finds no context about the information as is it not indicated in any of the files.
3. Who founded UniMatch? -> Bot successfully describes what kind of people founded UniMatch

- **Chitchat**
1. Hi! Do you like skiing?
2. Who is Dirichlet?
3. When is summer holidays in San Francisco?

In each prompt the chatbot will tell that they are not specialized in such topics, while providing a friendly answer. In any way, the chatbot will attempt to redirect the user towards making more pertinent prompts related to universities, scholarships, et cetera...

---

## 6. Intention Router

### 6.1 Intention Router Implementation

- **Message Generation**:  

For each intention we synthetically generated 50 messages, through LLMs (see the script `UniMatch/chatbot/router/generate_intentions.ipynb`), with an additional of 25 irrelevant messages. Moreover, we created other fifty synthetic intentions for the "Manage Personal Information" intention, as by testing we felt that it was the most misclassified one.

We stored the synthetic messages in `UniMatch/chatbot/router/synthetic_intentions.json` and the manually-made ones in `UniMatch/chatbot/router/new_intentions.json` 

### 6.2 Semantic Router Training

- **Encoder Type**

We had mainly two choices for our router, regarding the choice of encoder. Either we could have used an encoder from HuggingFace, or from OpenAI. To determine which one was the best for our intentions, we decided to train two baseline semantic routers and evaluated their accuracy scores accordingly; the one which showed the least signs of overfitting was picked for hyperparamter tuning.

**Result**: OpenAI's encoder gave us an accuracy of 0.9855, while HuggingFace's encoder had a 0.9493 accuracy. OpenAI's encoder was chosen as it had the best performance, even if it takes longer to train.

- **Other Hyperparameters: Aggregation method and Top K**
To decide on the aggregation method, we decided to test each one of them and chose the one with the best result, as done similarly with encoders.

**Results** (tabular format):
| Aggregate | Train | Validate |
| --------- | ----- | -------- |
| mean      | 0.93  | 0.98     |
| max       | 0.93  | 0.98     |
| sum       | 0.94  | 0.98     |

We choose `aggregation=sum` as it had the best train and evaluation score.

Then to decide the `top_k` parameter, we decided to do the same as above with the following candidates of `top_k`: k=1 (low), k=5 (average), k=50 (high).

**Results**: No variations in scores, meaning that in our case `top_k` is not influential. We chose `top_k=5` as it represented a sort of mid point between the possible decisions.

**Note**: A better alternative to this approach would have to use a GridSearchCV-similar approach; however as this is deemed to be too computationally expensive, we opted for an "evolutionary" approach.

For further details about the evaluation see the notebook at `UniMatch/chatbot/router/train_evaluate_router.ipynb`.

---

## 7. Intention Router Accuracy Testing Results
As we fine-tuned our router classifier, we evaluated it with the test data, giving us this result (stored in `UniMatch/UniMatch/chatbot/rag/router/evaluation_results.xlsx`)

| Intentions                             | Total | Misclassified | Accuracy |
| -------------------------------------- | ----- | ------------- | -------- |
| Manage Personal Information            | 10    | 0             | 100%     |
| Search Scholarships and Internationals | 6     | 0             | 100%     |
| Search Universities                    | 6     | 1             | 83%      |
| Matchmaking                            | 5     | 0             | 100%     |
| Query Matches                          | 5     | 0             | 100%     |
| Leverage RAG (User-Uploaded Files)     | 5     | 0             | 100%     |
| Company Information                    | 6     | 0             | 100%     |
| None                                   | 3     | 2             | 33%      |
| All                                    | 46    | 3             | 85%      |