# UIT Facebook Group 's Posts Classification

In this project, I use Machine Learning to classify the posts on [UIT Facebook Groups](https://www.facebook.com/groups/UIT.K2018/) into 4 topics: notification, finding lost items, personal question, other.

## Getting data

I use Selenium to repeat scrolling the page, then extract content of the posts
``` get_data.py ```

## Removing duplicates before annotation

Because there are posts which are posted in multiple groups, we need to remove those duplicates.
After removing duplicates, the dataset size decreased from 13154 to 9094.
``` remove_duplicate_before_annotation.ipynb ```

## Annotation

I use [Doccano](https://github.com/doccano/doccano) for annotation.

## Extracting features and classifying

Loading data + Taking a look at data + Feature Extraction + Classification + Hyperparameter Tuning
``` text_classification.ipynb ```

Vectorizer model: ``` tfidf.pickle ```
Tuned Linear SVC model: ``` finalized_model.sav ```

## Testing

Just run all cells in ``` test.ipynb ```, it will install required packages and clone this repo.

## Reference
[Scrape data using Selenium](https://www.youtube.com/watch?v=EawbYWaTP_k)

[Vietnamese Tokenizer](https://github.com/undertheseanlp/underthesea)

[Vietnamese Text Normalizer](https://github.com/langmaninternet/VietnameseTextNormalizer)

[Pandas Dataframe](https://pandas.pydata.org/pandas-docs/stable/user_guide/dsintro.html)

[Scikit-learn 's Document](https://scikit-learn.org/stable/)

