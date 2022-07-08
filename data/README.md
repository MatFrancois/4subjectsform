# DataManager

Before annotation, to classify tweets by context, we used fasttext embedding.

We defined few accounts that represent a community. Identified some community that represent the subject, and used a fasttext model trained on them to do a first classification on our tweet.

This "classification" is done in `remove_rt.py`.



