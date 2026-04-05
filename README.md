"# Project-Q-A-assistant-" 
Domain Q&A Assistant 🤖
A Streamlit web application that answers questions using AI, restricted to a selected domain.
Features

Select a domain: Fitness, Travel, Biology, or Personal Finance
Upload a CSV knowledge base
Ask questions and get AI-powered answers
Quick preset questions for each domain
Adjustable response tone, length, and audience level

How to Run

Install dependencies:

   pip install -r requirements.txt

Run the app:

   streamlit run app.py

Enter your OpenAI API key in the sidebar
Select a domain and upload a CSV file

CSV Format
Your knowledge base CSV must have these two columns:
topic, information
Protein, Essential for muscle building. Aim for 0.8-1g per pound of body weight.
Rest, Rest days are important for recovery. Take at least 1-2 rest days per week.


Project Structure

├── app.py                      # Main application
├── requirements.txt            # Dependencies
├── sample_data_fitness.csv     # Sample fitness knowledge base
├── sample_data_travel.csv      # Sample travel knowledge base
├── sample_data_biology.csv     # Sample biology knowledge base
├── sample_data_finance.csv     # Sample finance knowledge base
└── README.md                   # Project documentation

