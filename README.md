# 🍽️ MoodMeal-AI – AI Food Recommendation System

## 📌 Project Overview

**MoodMeal-AI** is an AI-powered food recommendation system that suggests suitable food based on the user's **mood, preferences, and dietary requirements**.

The project uses **Python, Machine Learning, and a recommendation system** to analyze user inputs and provide personalized food suggestions. It is designed to make food selection easier, faster, and more personalized.

---

## 🎯 Objectives

* Recommend food based on the user's current mood.
* Provide personalized food suggestions.
* Consider dietary preferences and restrictions.
* Use Machine Learning concepts for recommendation.
* Develop a simple and user-friendly interface.
* Demonstrate the practical application of AI and Data Science.

---

## ✨ Features

* 😊 Mood-based food recommendations
* 🍴 Personalized food suggestions
* 🥗 Dietary preference support
* 🔍 Food search and recommendation
* 🤖 Machine Learning-based recommendation
* 🌐 Simple web interface
* 📊 Dataset-based food analysis

---

## 🛠️ Technologies Used

| Technology   | Purpose                   |
| ------------ | ------------------------- |
| Python       | Main programming language |
| Pandas       | Data processing           |
| NumPy        | Numerical operations      |
| Scikit-learn | Machine Learning          |
| Flask        | Web application           |
| HTML         | Frontend structure        |
| CSS          | Frontend styling          |
| JavaScript   | Frontend interaction      |
| CSV          | Food dataset              |

---

## 🧠 How the System Works

The system follows these basic steps:

```text
User Input
    ↓
Mood & Food Preferences
    ↓
Data Preprocessing
    ↓
Feature Processing
    ↓
Recommendation Algorithm
    ↓
Food Matching
    ↓
Personalized Recommendations
```

### 1. User Input

The user provides information such as:

* Current mood
* Food preference
* Dietary preference
* Cuisine preference
* Other relevant requirements

### 2. Data Processing

The food dataset is loaded using **Pandas** and processed to make it suitable for recommendation.

### 3. Recommendation

The system compares the user's preferences with the available food data and identifies suitable food items.

### 4. Results

The application displays personalized food recommendations to the user.

---

## 📂 Project Structure

```text
MoodMeal-AI/
│
├── app.py
├── recommender.py
├── food_dataset.csv
├── requirements.txt
├── README.md
├── .gitignore
│
├── templates/
│   └── index.html
│
└── static/
    ├── style.css
    └── script.js
```

> **Note:** The `venv/` folder should not be uploaded to GitHub.

---

## ⚙️ Installation

### Step 1: Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/MoodMeal-AI.git
```

### Step 2: Open the project

```bash
cd MoodMeal-AI
```

### Step 3: Create a virtual environment

```bash
python -m venv venv
```

### Step 4: Activate the virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

### Step 5: Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Project

Run the Flask application:

```bash
python app.py
```

Then open the local URL displayed in the terminal, usually:

```text
http://127.0.0.1:5000/
```

---

## 📊 Dataset

The project uses a food dataset containing information about different food items and their characteristics.

Example attributes may include:

* Food name
* Category
* Cuisine
* Mood
* Dietary type
* Ingredients
* Calories
* Taste
* Preference

The dataset is processed using **Pandas** before being used by the recommendation system.

---

## 🤖 Machine Learning

The project demonstrates Machine Learning concepts including:

* Data preprocessing
* Feature selection
* Data transformation
* Similarity-based recommendation
* Prediction/recommendation
* Model evaluation where applicable

The recommendation component analyzes the relationship between user preferences and food characteristics to generate suitable recommendations.

---

## 💡 Example

### User Input

```text
Mood: Happy
Preference: Vegetarian
Cuisine: Indian
```

### Recommended Food

```text
🥗 Vegetable Biryani
🍛 Paneer Tikka
🥘 Masala Dosa
```

The recommendations depend on the available dataset and matching criteria.

---

## 🔮 Future Enhancements

The project can be further improved by adding:

* 🧠 Advanced Machine Learning models
* 🤖 LLM-based food recommendations
* 💬 AI chatbot integration
* 📱 Mobile application
* 🗺️ Nearby restaurant recommendations
* 🥗 Personalized nutrition information
* 🔥 Calorie and health-based recommendations
* ⭐ User ratings and feedback
* 📈 Recommendation history
* 🎙️ Voice-based interaction

---

## 🎓 Learning Outcomes

Through this project, we learn how to:

* Work with real-world datasets.
* Perform data preprocessing using Python.
* Apply Machine Learning concepts.
* Build a recommendation system.
* Develop a web application using Flask.
* Connect a Machine Learning system with a frontend.
* Organize and publish a project using GitHub.

---

## 👨‍💻 Project

**Project Name:** MoodMeal-AI
**Project Type:** AI & Machine Learning Project
**Domain:** Artificial Intelligence / Data Science
**Language:** Python

---

## 📜 License

This project is developed for **educational and academic purposes**.
