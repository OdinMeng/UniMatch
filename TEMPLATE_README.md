# CompanyName

This README.md template is designed to provide a clear and structured guide for documenting your chatbot project. It outlines the essential sections that should be included in your repository to ensure that anyone reviewing or contributing to the project can easily understand its functionality, setup process, and testing methodology. By following this template, you'll ensure that your project is well-documented, making it easier for team members and future contributors to maintain and extend the chatbot.

## 1. Project Overview

- **Company Name**: [Company Name]
- **Group X**: [List of contributors]
- **Description**:  
  Provide a concise overview of the company and the chatbot's purpose. Outline its core functionality and the intended use cases it addresses, including how it interacts with users, the types of queries it handles, and its overall objective.

---

## 2. How to Test the Chatbot

### 2.1 Prerequisites

- **Python Version**: [Specify required version of Python]
- **Dependencies**:  
  List all the required libraries and frameworks.
- **Environment Setup**:  
  Instructions for setting up the environment, such as creating a virtual environment or conda environment.

### 2.2 How to Run the Chatbot

Provide a clear, step-by-step guide on how to launch and interact with the chatbot. Include any necessary commands, parameters, or configurations. Groups should provide information of an existing user so i can test the chatbot using information of that user, i will also test the registration process.

## 3. Database Schema

### 3.1 Database Overview and Schema Diagram

Provide an overview of the database used by the chatbot system. Include a diagram of the database schema to visually represent the structure of tables, their relationships, and data flow. (with image)

### 3.2 Table Descriptions

Describe each table in the database schema, including its columns and their purpose.

---

## 4. User Intentions

### 4.1 Implemented Intentions

List and briefly describe the user intentions that the chatbot is designed to handle. For example:

- **Product Information**: User requests details about a specific product or product category.
- **Order Status**: User queries the status of an existing order based on an order ID.
- **Create Order**: User intends to create a new order, and the chatbot processes the order request.

### 4.2 How to Test Each Intention

For each intention, provide 3 examples of test messages that users can use to verify the chatbot's functionality. Include both typical and edge-case inputs to ensure the chatbot handles various scenarios.

#### Product Information

**Test Messages:**

1. "Tell me about the latest phone models."
2. "Give me more details about the tablet in your store."
3. "What products do you offer in the electronics section?"

**Expected Behavior:**  
The chatbot should retrieve and present information about the specific product or category the user is inquiring about.

---

## 5. Intention Router

### 5.1 Intention Router Implementation

- **Message Generation**:  
  Describe how you generated messages for each user intention. Did you create the messages manually, use synthetic data, or leverage a dataset? Specify the method used and tools/scripts for generating the data.  
  Where are the generated messages stored (e.g., in a file, database, or another format)?

### 5.2 Semantic Router Training

- **Hyperparameters**:  
  Report which encoder was used in the semantic router.  
  Report the aggregation method and the `top_k` parameter used for selecting the most relevant results.

### 5.3 Post-Processing for Accuracy Improvement

- **Post-Processing Techniques**:  
  If you applied any post-processing techniques to enhance the router's accuracy, describe them here.  
  For example, did you use a Large Language Model (LLM) for additional refinement?  
  Explain how these techniques were integrated into the pipeline and any custom code or algorithms used.

---

## 6. Intention Router Accuracy Testing Results

### Methodology

1. **Message Creation**:

   - Generate at least 50 messages per intention, totaling 400 messages. These can be either synthetic or human-generated.
   - Additionally, generate at least 25 small-talk messages related to your company and 25 off-topic messages unrelated to the company, labeled as "None."

2. **Data Splitting**:

   - Split the dataset into training and testing sets (90/10), ensuring a balanced distribution of each intention across both sets.

3. **Training the Semantic Router**:

   - Use the training split to train the semantic router. Report the accuracy on both the training and testing splits.

4. **Post-Processing with LLM**:

   - If applicable, apply post-processing using an LLM to improve the accuracy of the router. Report accuracy on both the training and testing splits after post-processing.

5. **Reporting Results**:
   - Report the accuracy for each intention, as well as the overall accuracy. Accuracy should be calculated as the percentage of correct responses out of the total inputs for each intention.

### Results

Present the accuracy results in a table format:

| Intention            | Test Inputs | Correct | Incorrect | Accuracy (%) |
| -------------------- | ----------- | ------- | --------- | ------------ |
| Product Information  | 10          | 9       | 1         | 90%          |
| Order Status         | 10          | 8       | 2         | 80%          |
| Create Order         | 10          | 7       | 3         | 70%          |
| **Average Accuracy** | 30          | 24      | 6         | 80%          |

```

```
