# Lab 1: Sentiment Analysis Using Traditional Machine Learning

**Module:** PUSL 3205 - Large Language Models and Generative AI
**Tools:** Python, Pandas, NumPy, NLTK, Scikit-learn, Matplotlib, Seaborn

## Objective
Practise basic NLP by building a classifier that predicts whether a sentence expresses positive or negative sentiment, using text preprocessing, a Bag of Words representation and traditional machine learning models.

## Dataset
[UCI Sentiment Labelled Sentences](https://archive.ics.uci.edu/dataset/331/sentiment%2Blabelled%2Bsentences): 3,000 sentences taken from Amazon product reviews, IMDB movie reviews and Yelp restaurant reviews. Each sentence is labelled 1 (positive) or 0 (negative). The classes are perfectly balanced, with 1,500 sentences each.

## What I did

1. **Loaded the data.** Read the three tab-separated files and combined them into one DataFrame with `text` and `label` columns.
2. **Preprocessed the text.** Converted to lowercase, removed punctuation, numbers and symbols, removed extra whitespace, and stored the result in a new `clean_text` column. I compared original and cleaned sentences side by side. Stopwords were kept on purpose, because words like "not" can flip the sentiment of a sentence.
3. **Explored the data.** Displayed positive and negative examples, plotted the class balance, and charted the 15 most frequent words in each class (stopwords removed for counting only).
4. **Split the dataset.** 80% training (2,400 sentences) and 20% testing (600 sentences), stratified so both sets keep the same class balance.
5. **Created a Bag of Words.** Used `CountVectorizer`, fitted on the training set only to avoid data leakage. The vocabulary has 4,479 unique words.
6. **Trained two models.** Logistic Regression and a linear SVM (`LinearSVC`).
7. **Evaluated** both models with accuracy, precision, recall and F1, plus a confusion matrix for Logistic Regression.
8. **Tested the model on new sentences.**

## Results

Evaluated on the 600 held-out test sentences:

| Model | Accuracy | Precision | Recall | F1 |
|-------|----------|-----------|--------|----|
| Logistic Regression | 0.822 | 0.804 | 0.850 | 0.827 |
| SVM (LinearSVC) | 0.810 | 0.784 | 0.857 | 0.818 |

Precision, recall and F1 are for the positive class.

## Key observations

- **Both models perform similarly.** Logistic Regression is slightly ahead (82.2% vs 81.0% accuracy), but the gap is small, so I would not call one clearly better on this dataset.
- **Both models are better at finding positives than negatives.** Recall for positive sentences (0.85 to 0.86) is higher than for negative ones (0.76 to 0.79), so the models more often label a negative sentence as positive than the other way round.
- **Word frequencies:** "great", "good", "best", "love" and "excellent" dominate the positive class, while "bad" is the clearest negative word. Many top words ("movie", "phone", "food", "film", "place", "service") appear in both classes because they describe the topic rather than the sentiment.
- **"good" also appears 53 times in negative sentences**, most likely in phrases like "not good". Bag of Words ignores word order, so negation is hard for it to capture.
- **Testing new sentences:** the model correctly classified "This phone is amazing, I love it!" as positive and "The food was terrible and the service was slow." as negative. It labelled the neutral sentence "It was okay I guess" as negative, which is a limitation of a binary classifier: it has no neutral class.

## Limitations and ideas for improvement
- Bag of Words loses word order and context, so negation and sarcasm are difficult.
- The dataset is fairly small (3,000 sentences).
- Next steps could include TF-IDF, n-grams (such as "not good") and cross-validation to get more reliable scores.

## How to run
1. Install the libraries: `pip install pandas numpy nltk scikit-learn matplotlib seaborn`
2. Open `Labsheet01.ipynb` in Jupyter Notebook.
3. Keep the `data` folder in the same folder as the notebook.
4. Select **Kernel → Restart & Run All**. The first run downloads the NLTK stopwords list, so it needs an internet connection.

## Folder contents
```
lab-01-sentiment-analysis/
├── README.md
├── Labsheet01.ipynb
└── data/
    ├── amazon_cells_labelled.txt
    ├── imdb_labelled.txt
    └── yelp_labelled.txt
```
