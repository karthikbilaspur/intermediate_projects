Summary of Enhancements
Text Summarization Methods: Implemented four summarization methods: sentence scoring, Gensim, TF-IDF and cosine similarity.
Sentiment Analysis: Integrated sentiment analysis using NLTK's VADER.
Error Handling: Implemented error handling for news article fetch and summarization failures.
About Page: Created an about page providing application information.
Improved User Interface: Enhanced styling and user experience.
Code Organization: Refactored code for readability and maintainability.
JavaScript Functionality: Added URL input validation, summarization method selection, sentiment visualization and error message handling.
README.md
MarkDown
# News Summarizer Web Application

A Flask web application utilizing natural language processing and machine learning to summarize news articles.

## Features

*   Text summarization using four methods: sentence scoring, Gensim, TF-IDF and cosine similarity
*   Sentiment analysis using NLTK's VADER
*   Error handling for news article fetch and summarization failures
*   About page providing application information
*   Improved user interface with enhanced styling and user experience

## Requirements

*   Flask (`pip install flask`)
*   NLTK (`pip install nltk`)
*   Gensim (`pip install gensim`)
*   BeautifulSoup (`pip install beautifulsoup4`)
*   Requests (`pip install requests`)
*   Textstat (`pip install textstat`)
*   Scikit-learn (`pip install scikit-learn`)
*   Sentiment (`pip install vaderSentiment`)

## Usage

1.  Clone repository.
2.  Install requirements using `pip install -r requirements.txt`.
3.  Run application using `python app.py`.
4.  Access application at `http://localhost:5000`.

## Contributing

Contributions are welcome. Fork repository, make changes and submit pull requests.

## License

[MIT License](https://opensource.org/licenses/MIT)

