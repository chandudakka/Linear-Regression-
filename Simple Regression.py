{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "name": "Untitled2.ipynb",
      "provenance": []
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "terysshXFofa"
      },
      "source": [
        "PREDICTION OF BOSTON HOUSE PRICES USING LINEAR REGRESSION\n",
        "\n",
        "Introduction What is linear regression? It is a predictive modeling technique that finds a relationship between independent variable(s) and dependent variable(s) (which is a continuous variable). The independent variable(iv)’s can be categorical(e.g. US, UK, 0/1) or continuous(1729, 3.141 etc), while dependent variable(dv)s are continuous. Underlying function mapping iv’s and dv’s can be linear, quadratic, polynomial or other non-linear functions(like sigmoid function in logistic regression), but this article is on linear technique. Regression techniques are heavily used in making real estate price prediction, financial forecasting, predicting traffic arrival time (ETA).\n",
        "\n",
        "Types of variables Categorical: Takes distinct values: Spam/Not Spam email, Diabetes +ve/-ve Continuous: Can take infinite values, e.g. money, time, weight. Dependent: Outcome of the experiment, house values in this blog Independent: Variable independent of what the researcher does. Area, location, #bedrooms etc. For additional reference, check this out: statistichowto.\n",
        "\n",
        "Linear Regression Techniques\n",
        "\n",
        "Ordinary Least Squares(OLS) In OLS, the objective is to find the best fit line through the data points. Best fit line is obtained by minimizing the sum of squared distances of data from the prediction line. This is an unbiased estimate(although variance is not minimized) as it minimizes bias for the data set in this observation space.\n",
        "Objective for Least Squares\n",
        "\n",
        "Key Assumptions: (i) OLS assumes linear relationship of dv and iv. (ii) Assumes homoskedasticity. Therefore, it suffers from heteroskedasticity. In short, it is the variability of the dependent variable with respect to the independent variable as the value of iv increases. A conical shape in the scatterplot of the data indicates heteroskedasticity.\n",
        "\n",
        "Multivariate Case In multivariate OLS, the objective function remains similar as for a single variable OLS.\n",
        "Objective for Multivariate Least Squares The key issue with multivariate OLS is multicollinearity. It is the condition in which two or more predictors have high correlation with one another(±1 indicates 100% correlation, 0 indicates no correlation). In data with multicollinearity, OLS does not yield a good estimate as the error by the variance term is significant and OLS only minimizes the bias error and not error due to variance. Therefore, we employ regularization techniques to minimize error due to variance and improve our model.\n",
        "\n",
        "Ridge Regression As discussed above, when data suffer from multicollinearity, unbiased estimator like OLS has a high error due to variance term. Ridge regression solves this problem by introducing a parameter α with an L2 regularization term to shrink the weight W in addition to the least square loss.\n",
        "Objective for Ridge Regression It has a similar assumption as the OLS except for homoskedasticity. Ridge regression shrinks the value of coefficients which are not highly correlated(not exactly zero).\n",
        "\n",
        "LASSO Regression Similar to ridge regression, it solves the multicollinearity problem by by regularization. Introducing a shrinkage parameter with an L1 norm to the weight W helps reduce the variance error in LASSO regression.\n",
        "Predicting Boston House-Prices Let’s dive in to coding the linear regression models. In this post, we are going to work with the Boston House prices dataset. It consists of 506 samples with 13 features with prices ranging from 5.0 to 50.0"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "XJrC8b_CFmNL"
      },
      "source": [
        "#import dependencies\n",
        "import pandas as pd\n",
        "import numpy as np\n",
        "from sklearn import linear_model\n",
        "from sklearn.model_selection import train_test_split"
      ],
      "execution_count": 1,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "IddV2n2XF4ct",
        "outputId": "509d4080-d7af-4550-a9c7-7365cea55d13"
      },
      "source": [
        "# Load the Boston Housing Data set from sklearn.datasets and print it\n",
        "from sklearn.datasets import load_boston\n",
        "boston = load_boston()\n",
        "print(boston)"
      ],
      "execution_count": 2,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "{'data': array([[6.3200e-03, 1.8000e+01, 2.3100e+00, ..., 1.5300e+01, 3.9690e+02,\n",
            "        4.9800e+00],\n",
            "       [2.7310e-02, 0.0000e+00, 7.0700e+00, ..., 1.7800e+01, 3.9690e+02,\n",
            "        9.1400e+00],\n",
            "       [2.7290e-02, 0.0000e+00, 7.0700e+00, ..., 1.7800e+01, 3.9283e+02,\n",
            "        4.0300e+00],\n",
            "       ...,\n",
            "       [6.0760e-02, 0.0000e+00, 1.1930e+01, ..., 2.1000e+01, 3.9690e+02,\n",
            "        5.6400e+00],\n",
            "       [1.0959e-01, 0.0000e+00, 1.1930e+01, ..., 2.1000e+01, 3.9345e+02,\n",
            "        6.4800e+00],\n",
            "       [4.7410e-02, 0.0000e+00, 1.1930e+01, ..., 2.1000e+01, 3.9690e+02,\n",
            "        7.8800e+00]]), 'target': array([24. , 21.6, 34.7, 33.4, 36.2, 28.7, 22.9, 27.1, 16.5, 18.9, 15. ,\n",
            "       18.9, 21.7, 20.4, 18.2, 19.9, 23.1, 17.5, 20.2, 18.2, 13.6, 19.6,\n",
            "       15.2, 14.5, 15.6, 13.9, 16.6, 14.8, 18.4, 21. , 12.7, 14.5, 13.2,\n",
            "       13.1, 13.5, 18.9, 20. , 21. , 24.7, 30.8, 34.9, 26.6, 25.3, 24.7,\n",
            "       21.2, 19.3, 20. , 16.6, 14.4, 19.4, 19.7, 20.5, 25. , 23.4, 18.9,\n",
            "       35.4, 24.7, 31.6, 23.3, 19.6, 18.7, 16. , 22.2, 25. , 33. , 23.5,\n",
            "       19.4, 22. , 17.4, 20.9, 24.2, 21.7, 22.8, 23.4, 24.1, 21.4, 20. ,\n",
            "       20.8, 21.2, 20.3, 28. , 23.9, 24.8, 22.9, 23.9, 26.6, 22.5, 22.2,\n",
            "       23.6, 28.7, 22.6, 22. , 22.9, 25. , 20.6, 28.4, 21.4, 38.7, 43.8,\n",
            "       33.2, 27.5, 26.5, 18.6, 19.3, 20.1, 19.5, 19.5, 20.4, 19.8, 19.4,\n",
            "       21.7, 22.8, 18.8, 18.7, 18.5, 18.3, 21.2, 19.2, 20.4, 19.3, 22. ,\n",
            "       20.3, 20.5, 17.3, 18.8, 21.4, 15.7, 16.2, 18. , 14.3, 19.2, 19.6,\n",
            "       23. , 18.4, 15.6, 18.1, 17.4, 17.1, 13.3, 17.8, 14. , 14.4, 13.4,\n",
            "       15.6, 11.8, 13.8, 15.6, 14.6, 17.8, 15.4, 21.5, 19.6, 15.3, 19.4,\n",
            "       17. , 15.6, 13.1, 41.3, 24.3, 23.3, 27. , 50. , 50. , 50. , 22.7,\n",
            "       25. , 50. , 23.8, 23.8, 22.3, 17.4, 19.1, 23.1, 23.6, 22.6, 29.4,\n",
            "       23.2, 24.6, 29.9, 37.2, 39.8, 36.2, 37.9, 32.5, 26.4, 29.6, 50. ,\n",
            "       32. , 29.8, 34.9, 37. , 30.5, 36.4, 31.1, 29.1, 50. , 33.3, 30.3,\n",
            "       34.6, 34.9, 32.9, 24.1, 42.3, 48.5, 50. , 22.6, 24.4, 22.5, 24.4,\n",
            "       20. , 21.7, 19.3, 22.4, 28.1, 23.7, 25. , 23.3, 28.7, 21.5, 23. ,\n",
            "       26.7, 21.7, 27.5, 30.1, 44.8, 50. , 37.6, 31.6, 46.7, 31.5, 24.3,\n",
            "       31.7, 41.7, 48.3, 29. , 24. , 25.1, 31.5, 23.7, 23.3, 22. , 20.1,\n",
            "       22.2, 23.7, 17.6, 18.5, 24.3, 20.5, 24.5, 26.2, 24.4, 24.8, 29.6,\n",
            "       42.8, 21.9, 20.9, 44. , 50. , 36. , 30.1, 33.8, 43.1, 48.8, 31. ,\n",
            "       36.5, 22.8, 30.7, 50. , 43.5, 20.7, 21.1, 25.2, 24.4, 35.2, 32.4,\n",
            "       32. , 33.2, 33.1, 29.1, 35.1, 45.4, 35.4, 46. , 50. , 32.2, 22. ,\n",
            "       20.1, 23.2, 22.3, 24.8, 28.5, 37.3, 27.9, 23.9, 21.7, 28.6, 27.1,\n",
            "       20.3, 22.5, 29. , 24.8, 22. , 26.4, 33.1, 36.1, 28.4, 33.4, 28.2,\n",
            "       22.8, 20.3, 16.1, 22.1, 19.4, 21.6, 23.8, 16.2, 17.8, 19.8, 23.1,\n",
            "       21. , 23.8, 23.1, 20.4, 18.5, 25. , 24.6, 23. , 22.2, 19.3, 22.6,\n",
            "       19.8, 17.1, 19.4, 22.2, 20.7, 21.1, 19.5, 18.5, 20.6, 19. , 18.7,\n",
            "       32.7, 16.5, 23.9, 31.2, 17.5, 17.2, 23.1, 24.5, 26.6, 22.9, 24.1,\n",
            "       18.6, 30.1, 18.2, 20.6, 17.8, 21.7, 22.7, 22.6, 25. , 19.9, 20.8,\n",
            "       16.8, 21.9, 27.5, 21.9, 23.1, 50. , 50. , 50. , 50. , 50. , 13.8,\n",
            "       13.8, 15. , 13.9, 13.3, 13.1, 10.2, 10.4, 10.9, 11.3, 12.3,  8.8,\n",
            "        7.2, 10.5,  7.4, 10.2, 11.5, 15.1, 23.2,  9.7, 13.8, 12.7, 13.1,\n",
            "       12.5,  8.5,  5. ,  6.3,  5.6,  7.2, 12.1,  8.3,  8.5,  5. , 11.9,\n",
            "       27.9, 17.2, 27.5, 15. , 17.2, 17.9, 16.3,  7. ,  7.2,  7.5, 10.4,\n",
            "        8.8,  8.4, 16.7, 14.2, 20.8, 13.4, 11.7,  8.3, 10.2, 10.9, 11. ,\n",
            "        9.5, 14.5, 14.1, 16.1, 14.3, 11.7, 13.4,  9.6,  8.7,  8.4, 12.8,\n",
            "       10.5, 17.1, 18.4, 15.4, 10.8, 11.8, 14.9, 12.6, 14.1, 13. , 13.4,\n",
            "       15.2, 16.1, 17.8, 14.9, 14.1, 12.7, 13.5, 14.9, 20. , 16.4, 17.7,\n",
            "       19.5, 20.2, 21.4, 19.9, 19. , 19.1, 19.1, 20.1, 19.9, 19.6, 23.2,\n",
            "       29.8, 13.8, 13.3, 16.7, 12. , 14.6, 21.4, 23. , 23.7, 25. , 21.8,\n",
            "       20.6, 21.2, 19.1, 20.6, 15.2,  7. ,  8.1, 13.6, 20.1, 21.8, 24.5,\n",
            "       23.1, 19.7, 18.3, 21.2, 17.5, 16.8, 22.4, 20.6, 23.9, 22. , 11.9]), 'feature_names': array(['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD',\n",
            "       'TAX', 'PTRATIO', 'B', 'LSTAT'], dtype='<U7'), 'DESCR': \".. _boston_dataset:\\n\\nBoston house prices dataset\\n---------------------------\\n\\n**Data Set Characteristics:**  \\n\\n    :Number of Instances: 506 \\n\\n    :Number of Attributes: 13 numeric/categorical predictive. Median Value (attribute 14) is usually the target.\\n\\n    :Attribute Information (in order):\\n        - CRIM     per capita crime rate by town\\n        - ZN       proportion of residential land zoned for lots over 25,000 sq.ft.\\n        - INDUS    proportion of non-retail business acres per town\\n        - CHAS     Charles River dummy variable (= 1 if tract bounds river; 0 otherwise)\\n        - NOX      nitric oxides concentration (parts per 10 million)\\n        - RM       average number of rooms per dwelling\\n        - AGE      proportion of owner-occupied units built prior to 1940\\n        - DIS      weighted distances to five Boston employment centres\\n        - RAD      index of accessibility to radial highways\\n        - TAX      full-value property-tax rate per $10,000\\n        - PTRATIO  pupil-teacher ratio by town\\n        - B        1000(Bk - 0.63)^2 where Bk is the proportion of blacks by town\\n        - LSTAT    % lower status of the population\\n        - MEDV     Median value of owner-occupied homes in $1000's\\n\\n    :Missing Attribute Values: None\\n\\n    :Creator: Harrison, D. and Rubinfeld, D.L.\\n\\nThis is a copy of UCI ML housing dataset.\\nhttps://archive.ics.uci.edu/ml/machine-learning-databases/housing/\\n\\n\\nThis dataset was taken from the StatLib library which is maintained at Carnegie Mellon University.\\n\\nThe Boston house-price data of Harrison, D. and Rubinfeld, D.L. 'Hedonic\\nprices and the demand for clean air', J. Environ. Economics & Management,\\nvol.5, 81-102, 1978.   Used in Belsley, Kuh & Welsch, 'Regression diagnostics\\n...', Wiley, 1980.   N.B. Various transformations are used in the table on\\npages 244-261 of the latter.\\n\\nThe Boston house-price data has been used in many machine learning papers that address regression\\nproblems.   \\n     \\n.. topic:: References\\n\\n   - Belsley, Kuh & Welsch, 'Regression diagnostics: Identifying Influential Data and Sources of Collinearity', Wiley, 1980. 244-261.\\n   - Quinlan,R. (1993). Combining Instance-Based and Model-Based Learning. In Proceedings on the Tenth International Conference of Machine Learning, 236-243, University of Massachusetts, Amherst. Morgan Kaufmann.\\n\", 'filename': '/usr/local/lib/python3.7/dist-packages/sklearn/datasets/data/boston_house_prices.csv'}\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "yYRT_bJwF60A"
      },
      "source": [
        "# Transform the data set into a data frame\n",
        "# data = the data we want or independent variables also known as the x values\n",
        "# feature_names = the column names of the data \n",
        "# target = the target of variable or the price of the houses or dependent variables also known as the y value \n",
        "\n",
        "df_x = pd.DataFrame(boston.data, columns=boston.feature_names)\n",
        "df_y = pd.DataFrame(boston.target)\n"
      ],
      "execution_count": 3,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 295
        },
        "id": "8H7TBt-wGHN_",
        "outputId": "6d503ba3-de7e-4df8-8be1-cf5b25debef7"
      },
      "source": [
        "# Get some Statistics from the data set, count, mean \n",
        "df_x.describe()"
      ],
      "execution_count": 4,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/html": [
              "<div>\n",
              "<style scoped>\n",
              "    .dataframe tbody tr th:only-of-type {\n",
              "        vertical-align: middle;\n",
              "    }\n",
              "\n",
              "    .dataframe tbody tr th {\n",
              "        vertical-align: top;\n",
              "    }\n",
              "\n",
              "    .dataframe thead th {\n",
              "        text-align: right;\n",
              "    }\n",
              "</style>\n",
              "<table border=\"1\" class=\"dataframe\">\n",
              "  <thead>\n",
              "    <tr style=\"text-align: right;\">\n",
              "      <th></th>\n",
              "      <th>CRIM</th>\n",
              "      <th>ZN</th>\n",
              "      <th>INDUS</th>\n",
              "      <th>CHAS</th>\n",
              "      <th>NOX</th>\n",
              "      <th>RM</th>\n",
              "      <th>AGE</th>\n",
              "      <th>DIS</th>\n",
              "      <th>RAD</th>\n",
              "      <th>TAX</th>\n",
              "      <th>PTRATIO</th>\n",
              "      <th>B</th>\n",
              "      <th>LSTAT</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>count</th>\n",
              "      <td>506.000000</td>\n",
              "      <td>506.000000</td>\n",
              "      <td>506.000000</td>\n",
              "      <td>506.000000</td>\n",
              "      <td>506.000000</td>\n",
              "      <td>506.000000</td>\n",
              "      <td>506.000000</td>\n",
              "      <td>506.000000</td>\n",
              "      <td>506.000000</td>\n",
              "      <td>506.000000</td>\n",
              "      <td>506.000000</td>\n",
              "      <td>506.000000</td>\n",
              "      <td>506.000000</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>mean</th>\n",
              "      <td>3.613524</td>\n",
              "      <td>11.363636</td>\n",
              "      <td>11.136779</td>\n",
              "      <td>0.069170</td>\n",
              "      <td>0.554695</td>\n",
              "      <td>6.284634</td>\n",
              "      <td>68.574901</td>\n",
              "      <td>3.795043</td>\n",
              "      <td>9.549407</td>\n",
              "      <td>408.237154</td>\n",
              "      <td>18.455534</td>\n",
              "      <td>356.674032</td>\n",
              "      <td>12.653063</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>std</th>\n",
              "      <td>8.601545</td>\n",
              "      <td>23.322453</td>\n",
              "      <td>6.860353</td>\n",
              "      <td>0.253994</td>\n",
              "      <td>0.115878</td>\n",
              "      <td>0.702617</td>\n",
              "      <td>28.148861</td>\n",
              "      <td>2.105710</td>\n",
              "      <td>8.707259</td>\n",
              "      <td>168.537116</td>\n",
              "      <td>2.164946</td>\n",
              "      <td>91.294864</td>\n",
              "      <td>7.141062</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>min</th>\n",
              "      <td>0.006320</td>\n",
              "      <td>0.000000</td>\n",
              "      <td>0.460000</td>\n",
              "      <td>0.000000</td>\n",
              "      <td>0.385000</td>\n",
              "      <td>3.561000</td>\n",
              "      <td>2.900000</td>\n",
              "      <td>1.129600</td>\n",
              "      <td>1.000000</td>\n",
              "      <td>187.000000</td>\n",
              "      <td>12.600000</td>\n",
              "      <td>0.320000</td>\n",
              "      <td>1.730000</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>25%</th>\n",
              "      <td>0.082045</td>\n",
              "      <td>0.000000</td>\n",
              "      <td>5.190000</td>\n",
              "      <td>0.000000</td>\n",
              "      <td>0.449000</td>\n",
              "      <td>5.885500</td>\n",
              "      <td>45.025000</td>\n",
              "      <td>2.100175</td>\n",
              "      <td>4.000000</td>\n",
              "      <td>279.000000</td>\n",
              "      <td>17.400000</td>\n",
              "      <td>375.377500</td>\n",
              "      <td>6.950000</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>50%</th>\n",
              "      <td>0.256510</td>\n",
              "      <td>0.000000</td>\n",
              "      <td>9.690000</td>\n",
              "      <td>0.000000</td>\n",
              "      <td>0.538000</td>\n",
              "      <td>6.208500</td>\n",
              "      <td>77.500000</td>\n",
              "      <td>3.207450</td>\n",
              "      <td>5.000000</td>\n",
              "      <td>330.000000</td>\n",
              "      <td>19.050000</td>\n",
              "      <td>391.440000</td>\n",
              "      <td>11.360000</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>75%</th>\n",
              "      <td>3.677083</td>\n",
              "      <td>12.500000</td>\n",
              "      <td>18.100000</td>\n",
              "      <td>0.000000</td>\n",
              "      <td>0.624000</td>\n",
              "      <td>6.623500</td>\n",
              "      <td>94.075000</td>\n",
              "      <td>5.188425</td>\n",
              "      <td>24.000000</td>\n",
              "      <td>666.000000</td>\n",
              "      <td>20.200000</td>\n",
              "      <td>396.225000</td>\n",
              "      <td>16.955000</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>max</th>\n",
              "      <td>88.976200</td>\n",
              "      <td>100.000000</td>\n",
              "      <td>27.740000</td>\n",
              "      <td>1.000000</td>\n",
              "      <td>0.871000</td>\n",
              "      <td>8.780000</td>\n",
              "      <td>100.000000</td>\n",
              "      <td>12.126500</td>\n",
              "      <td>24.000000</td>\n",
              "      <td>711.000000</td>\n",
              "      <td>22.000000</td>\n",
              "      <td>396.900000</td>\n",
              "      <td>37.970000</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "</div>"
            ],
            "text/plain": [
              "             CRIM          ZN       INDUS  ...     PTRATIO           B       LSTAT\n",
              "count  506.000000  506.000000  506.000000  ...  506.000000  506.000000  506.000000\n",
              "mean     3.613524   11.363636   11.136779  ...   18.455534  356.674032   12.653063\n",
              "std      8.601545   23.322453    6.860353  ...    2.164946   91.294864    7.141062\n",
              "min      0.006320    0.000000    0.460000  ...   12.600000    0.320000    1.730000\n",
              "25%      0.082045    0.000000    5.190000  ...   17.400000  375.377500    6.950000\n",
              "50%      0.256510    0.000000    9.690000  ...   19.050000  391.440000   11.360000\n",
              "75%      3.677083   12.500000   18.100000  ...   20.200000  396.225000   16.955000\n",
              "max     88.976200  100.000000   27.740000  ...   22.000000  396.900000   37.970000\n",
              "\n",
              "[8 rows x 13 columns]"
            ]
          },
          "metadata": {},
          "execution_count": 4
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "LUUO9MueGNK_"
      },
      "source": [
        "# Intialise the linear regression model\n",
        "reg = linear_model.LinearRegression()"
      ],
      "execution_count": 5,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "u8gmyYWmGPGO"
      },
      "source": [
        "# Split the data into 67% training and 33% testing data\n",
        "x_train, x_test, y_train, y_test = train_test_split(df_x, df_y, test_size= 0.33, random_state= 42)"
      ],
      "execution_count": 6,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "DKHlvU2bGWNW",
        "outputId": "bbb25813-8728-439a-f6e1-625ce02b1b25"
      },
      "source": [
        "# Train the model with our training data\n",
        "reg.fit(x_train, y_train)"
      ],
      "execution_count": 7,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "LinearRegression(copy_X=True, fit_intercept=True, n_jobs=None, normalize=False)"
            ]
          },
          "metadata": {},
          "execution_count": 7
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "gNtM6aRtGakn",
        "outputId": "12282998-ee16-4687-a020-48a3e5cb9bab"
      },
      "source": [
        "# Print the co-efficients/weights for each feature/coloum of our model\n",
        "print(reg.coef_) #f(x) = mx + da + b = y"
      ],
      "execution_count": 8,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "[[-1.28749718e-01  3.78232228e-02  5.82109233e-02  3.23866812e+00\n",
            "  -1.61698120e+01  3.90205116e+00 -1.28507825e-02 -1.42222430e+00\n",
            "   2.34853915e-01 -8.21331947e-03 -9.28722459e-01  1.17695921e-02\n",
            "  -5.47566338e-01]]\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "DYb63Ji6Gcp3",
        "outputId": "d8e0c064-391c-4d6f-bbdf-72f7e7471e2e"
      },
      "source": [
        "# print the predictions on our test data\n",
        "y_pred = reg.predict(x_test)\n",
        "print(y_pred)"
      ],
      "execution_count": 9,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "[[28.53469469]\n",
            " [36.6187006 ]\n",
            " [15.63751079]\n",
            " [25.5014496 ]\n",
            " [18.7096734 ]\n",
            " [23.16471591]\n",
            " [17.31011035]\n",
            " [14.07736367]\n",
            " [23.01064388]\n",
            " [20.54223482]\n",
            " [24.91632351]\n",
            " [18.41098052]\n",
            " [-6.52079687]\n",
            " [21.83372604]\n",
            " [19.14903064]\n",
            " [26.0587322 ]\n",
            " [20.30232625]\n",
            " [ 5.74943567]\n",
            " [40.33137811]\n",
            " [17.45791446]\n",
            " [27.47486665]\n",
            " [30.2170757 ]\n",
            " [10.80555625]\n",
            " [23.87721728]\n",
            " [17.99492211]\n",
            " [16.02608791]\n",
            " [23.268288  ]\n",
            " [14.36825207]\n",
            " [22.38116971]\n",
            " [19.3092068 ]\n",
            " [22.17284576]\n",
            " [25.05925441]\n",
            " [25.13780726]\n",
            " [18.46730198]\n",
            " [16.60405712]\n",
            " [17.46564046]\n",
            " [30.71367733]\n",
            " [20.05106788]\n",
            " [23.9897768 ]\n",
            " [24.94322408]\n",
            " [13.97945355]\n",
            " [31.64706967]\n",
            " [42.48057206]\n",
            " [17.70042814]\n",
            " [26.92507869]\n",
            " [17.15897719]\n",
            " [13.68918087]\n",
            " [26.14924245]\n",
            " [20.2782306 ]\n",
            " [29.99003492]\n",
            " [21.21260347]\n",
            " [34.03649185]\n",
            " [15.41837553]\n",
            " [25.95781061]\n",
            " [39.13897274]\n",
            " [22.96118424]\n",
            " [18.80310558]\n",
            " [33.07865362]\n",
            " [24.74384155]\n",
            " [12.83640958]\n",
            " [22.41963398]\n",
            " [30.64804979]\n",
            " [31.59567111]\n",
            " [16.34088197]\n",
            " [20.9504304 ]\n",
            " [16.70145875]\n",
            " [20.23215646]\n",
            " [26.1437865 ]\n",
            " [31.12160889]\n",
            " [11.89762768]\n",
            " [20.45432404]\n",
            " [27.48356359]\n",
            " [10.89034224]\n",
            " [16.77707214]\n",
            " [24.02593714]\n",
            " [ 5.44691807]\n",
            " [21.35152331]\n",
            " [41.27267175]\n",
            " [18.13447647]\n",
            " [ 9.8012101 ]\n",
            " [21.24024342]\n",
            " [13.02644969]\n",
            " [21.80198374]\n",
            " [ 9.48201752]\n",
            " [22.99183857]\n",
            " [31.90465631]\n",
            " [18.95594718]\n",
            " [25.48515032]\n",
            " [29.49687019]\n",
            " [20.07282539]\n",
            " [25.5616062 ]\n",
            " [ 5.59584382]\n",
            " [20.18410904]\n",
            " [15.08773299]\n",
            " [14.34562117]\n",
            " [20.85155407]\n",
            " [24.80149389]\n",
            " [-0.19785401]\n",
            " [13.57649004]\n",
            " [15.64401679]\n",
            " [22.03765773]\n",
            " [24.70314482]\n",
            " [10.86409112]\n",
            " [19.60231067]\n",
            " [23.73429161]\n",
            " [12.08082177]\n",
            " [18.40997903]\n",
            " [25.4366158 ]\n",
            " [20.76506636]\n",
            " [24.68588237]\n",
            " [ 7.4995836 ]\n",
            " [18.93015665]\n",
            " [21.70801764]\n",
            " [27.14350579]\n",
            " [31.93765208]\n",
            " [15.19483586]\n",
            " [34.01357428]\n",
            " [12.85763091]\n",
            " [21.06646184]\n",
            " [28.58470042]\n",
            " [15.77437534]\n",
            " [24.77512495]\n",
            " [ 3.64655689]\n",
            " [23.91169589]\n",
            " [25.82292925]\n",
            " [23.03339677]\n",
            " [25.35158335]\n",
            " [33.05655447]\n",
            " [20.65930467]\n",
            " [38.18917361]\n",
            " [14.04714297]\n",
            " [25.26034469]\n",
            " [17.6138723 ]\n",
            " [20.60883766]\n",
            " [ 9.8525544 ]\n",
            " [21.06756951]\n",
            " [22.20145587]\n",
            " [32.2920276 ]\n",
            " [31.57638342]\n",
            " [15.29265938]\n",
            " [16.7100235 ]\n",
            " [29.10550932]\n",
            " [25.17762329]\n",
            " [16.88159225]\n",
            " [ 6.32621877]\n",
            " [26.70210263]\n",
            " [23.3525851 ]\n",
            " [17.24168182]\n",
            " [13.22815696]\n",
            " [39.49907507]\n",
            " [16.53528575]\n",
            " [18.14635902]\n",
            " [25.06620426]\n",
            " [23.70640231]\n",
            " [22.20167772]\n",
            " [21.22272327]\n",
            " [16.89825921]\n",
            " [23.15518273]\n",
            " [28.69699805]\n",
            " [ 6.65526482]\n",
            " [23.98399958]\n",
            " [17.21004545]\n",
            " [21.0574427 ]\n",
            " [25.01734597]\n",
            " [27.65461859]\n",
            " [20.70205823]\n",
            " [40.38214871]]\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "06GlMPttGgtQ",
        "outputId": "24573a40-44d3-4b42-88cd-c18fef210373"
      },
      "source": [
        "# Print the actual values\n",
        "print(y_test)"
      ],
      "execution_count": 11,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "        0\n",
            "173  23.6\n",
            "274  32.4\n",
            "491  13.6\n",
            "72   22.8\n",
            "452  16.1\n",
            "..    ...\n",
            "110  21.7\n",
            "321  23.1\n",
            "265  22.8\n",
            "29   21.0\n",
            "262  48.8\n",
            "\n",
            "[167 rows x 1 columns]\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "-ERBkT_KGnzP",
        "outputId": "1eb0f926-5fb3-47aa-d412-14ea6d0e761c"
      },
      "source": [
        "# Check the model performance/accuracy using Mean Squared error(MSE)\n",
        "print( np.mean((y_pred - y_test)**2 ))# Check the model performance/accuracy using Mean Squared error(MSE)\n",
        "print( np.mean((y_pred - y_test)**2 ))"
      ],
      "execution_count": 12,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "0    20.724023\n",
            "dtype: float64\n",
            "0    20.724023\n",
            "dtype: float64\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "2yrHYS3jGpmo",
        "outputId": "087ba6e1-9783-4f0f-fdb2-6040687fe4e1"
      },
      "source": [
        "# Check the model performance/accuracy using Mean Squared error (MSE) and sklearn.metrics\n",
        "from sklearn.metrics import mean_squared_error\n",
        "print( mean_squared_error(y_test, y_pred))"
      ],
      "execution_count": 13,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "20.724023437339717\n"
          ]
        }
      ]
    }
  ]
}
