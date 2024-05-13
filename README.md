###How to setup environment
pipenv install and it will download all the dependencies

Create .env file and the add OPENAI_API_KEY=<> in that file

there are two file to run 1 app.py and 2 main.py

app.py is for to run in chainlit for that use command "chainlit run app.py" and it will open URL automatically in Chrome on URL: http://localhost:8000

main.py is plain langchain experiment file and it will print response in console only not in Chrome
 if you want to add more documents, add it inside the /input_doc folder and curently it is only supporting PDF files so conver docs into PDF.
 To run main.py file use belwo command:
 python main.py

