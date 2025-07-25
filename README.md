# Classroom-Activity-Generator
🧠 AI Classroom App
An AI-powered interactive classroom tool designed to generate custom activities, evaluate student responses using LLMs, and support multilingual environments through translation. Built using FastAPI, React, and OpenAI's GPT models, this app is ideal for educators seeking automated, dynamic, and engaging learning experiences.


✨ Features
🔁 Dynamic Activity Generation: Generate diverse activities (e.g., quizzes, fill-in-the-blanks, coding tasks) using AI.

🧪 Student Response Evaluation: Automatically grade responses using GPT and provide feedback.

🌐 Multilingual Support: Translate content into multiple languages using Google Translate API.

📥 Downloadable Reports: Export activity evaluations and summaries as downloadable CSV files.

⚙️ Customizable Prompt Engine: Modify activity generation behavior using system-level prompt design.

🖤 Clean UI with Dark Orange-Black Theme: Intuitive and stylish Streamlit interface.



🤖 Agentic Design Insight
The backend includes a modular design via ai_engine.py, where an agentic approach has been introduced. While the current task is atomic and relatively simple, the architecture is extensible and scalable for agentic workflows—where a single autonomous agent can manage and coordinate a series of sub-tasks to accomplish a high-level goal.

Think of the agent like a “broker” or “project manager” — capable of breaking down a large task into actionable steps, executing them iteratively, and synthesizing a coherent output.
This agentic setup becomes particularly powerful for complex education pipelines like syllabus creation, exam paper generation, or adaptive learning paths.



Directions to follow
->you clone this project
-> create a .env file in the backend folder
->use open ai key(I have used open_ai router )
->then you are good to gooooo
