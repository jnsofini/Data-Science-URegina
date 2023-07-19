# Automatic Scorecard

Here we build a simple scorecard pipeline which can automatically generate a scorecard. This folder contains code that is working and was used as a final pipeline to build a risk scoring model. There are various steps followed in the pipeline which includes

- [Data ingestion](src/ingest.py): In this stage,  the data is gathered from sources.
- [Separation](src/test_train_split.py): In this step, we randomly partitions the data to ensure that the model's performance can be evaluated on unseen data. By using separate training and testing sets, train_test_split helps to avoid overfitting. The testing set allows us to estimate how well the model will perform on new, unseen data. This evaluation helps in selecting the best model, tuning hyperparameters, and making informed decisions about its deployment and usage in real-world scenarios.

- **Feature Reduction**: This steps involves a few processes bundled into a scikit-learn pipeline object. It holds data transformation as well as dimensionality reduction to improve the efficiency of the learning process. In the feature reduction part we aim to remove the feature with negligeable variation using **VarianceThreshold**.

    In the second part of the step, we preprocess the data
    including transforming every feature to ordinal data using WOE
    using **BinningProcess** module from Optbinning.

    Next we perform feature clustering using **Varclushi**. The features are clustered together based on their correlation. The feature with the highes informational value and the one at the center of the cluster are selected. With Varclushi, you can identify and eliminate redundant or irrelevant features from your dataset, leading to more efficient and interpretable models. By leveraging clustering and statistical techniques, Varclushi helps uncover the most informative features and improve overall model performance.

    Finally we reached the feature selection stage, a further smaller number of feature are further selected to provide a parsimonous model we used **RFECV (Recursive Feature Elimination with Cross-Validation)** from scikit-learn. RFECV helps improve model interpretability, reduce overfitting, and enhance prediction accuracy by automatically selecting the most relevant features for the task at hand.

- **Model**: The model stage involves building a scorecard with the final features. The **Scorecard** module in OptBinning allows you to develop scorecards by combining binning via **BinningProcess** and logistic regression via scikit-learn **LogisticRegression**.

The code is designed as a scikit-learn pipeline in which all the stages are coupled together and runs at once. The first thing we need to do is set the environment. This is achieved via pipenv by running

```sh
pipenv install --dev && pipenv shell
```

Assuming you have the data downloaded and stored in a directory called _data_, we split it by running the following

```python
python src/test_train_split.py
```

Next, it is time to run the pipeline. Just verify that you have the train and test data in a directory called _data_ in the same folder as the autoscorecard project.

To run the auto scorecard,

```python
python auto-scorecard.py
```

During the first run, the code will attempt to read files that are not generated yet. In subsequent runs, it can identify some files that are needed. This include files like information value tables. This means the result from the first run could differ from the one from subsequent runs. This is by design!
