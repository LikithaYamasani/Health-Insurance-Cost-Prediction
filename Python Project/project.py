### Importing the packages
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import backend as backend
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor
import xgboost as xg
from math import sqrt
import pickle

### Setting up the project
backend.setup_database()
dataset = backend.fetch_customer_data()

def plot_graphs():
    plot_mean_charges_by_sex_and_smoker()
    age_distribution_by_sex()
    plot_mean_charges_by_region_and_smoker()
    plot_mean_charges_by_region_and_customer()
    plot_age_count_graph()
    plot_age_smoker_graph()
    plot_age_count_density_graph()
    plot_age_charges_graph()
    plot_region_charges_data()
    plot_bmi_sex_graph()
    plot_correlation_graph()
    
def plot_mean_charges_by_sex_and_smoker():
    dataset = backend.fetch_charges_smoker_sex_data()
    sns.factorplot(x = 'Smoker', y = 'Charges', hue = 'Sex', data = dataset, kind = 'bar')
    plt.ylabel('Mean Charges')
    plt.title('Mean Charges by Sex and Smoker')
    plt.show()

def age_distribution_by_sex():
    dataset = backend.fetch_age_sex_data()
    sns.kdeplot(dataset['Age'][dataset['Sex'] == 'male'], label = 'Male')
    sns.kdeplot(dataset['Age'][dataset['Sex'] == 'female'], label = 'Female')
    plt.xlabel('Age')
    plt.legend()
    plt.title('Age Distribution by Sex')
    plt.show()
    
def plot_mean_charges_by_region_and_smoker():
    dataset = backend.fetch_smokers_region_data()
    plt.pie(dataset['Number_of_Smokers'], labels = dataset['Region'], autopct='%.0f%%')
    plt.title('Count of Smokers per Region')
    plt.show()
    
def plot_mean_charges_by_region_and_customer():
    dataset = backend.fetch_customers_region_data()
    sns.barplot(dataset['Region'],dataset['Number_of_Customers'])
    plt.ylabel('Count')
    plt.title('Count of Customers per Region')
    plt.show()
    
def plot_age_count_graph():
    dataset = backend.fetch_age_count_data()
    sns.barplot(dataset['Age_Range'],dataset['Number_of_Customers'])
    plt.title('Count of Customers per Age Group')
    plt.xlabel('Age Group')
    plt.show()
    
def plot_age_smoker_graph():
    dataset = backend.fetch_age_and_smoker_data()
    plt.pie(dataset['Number_of_Customers'], labels = dataset['Age_Range'], autopct='%.0f%%')
    plt.title('Count of Smokers per Age Group')
    plt.show()
    
def plot_age_count_density_graph():
    dataset = backend.fetch_age_data()
    sns.distplot(dataset['Age'], color='green')
    plt.title('Count of Customers per Age Group')
    plt.xlabel('Age Group')
    plt.show()    

def plot_age_charges_graph():
    dataset = backend.fetch_age_charges_data()
    sns.barplot(dataset['Age_Range'],dataset['Mean_Charges'])
    plt.ylabel('Average')
    plt.title('Average Charges per Age Group')
    plt.show()
    
def plot_region_charges_data():
    dataset = backend.fetch_region_charges_data()
    sns.barplot(dataset['Region'],dataset['Mean_Charges'])
    plt.ylabel('Average')
    plt.title('Average Charges per Region')
    plt.show()
    
def plot_bmi_sex_graph():
    dataset = backend.fetch_bmi_sex_data()
    sns.kdeplot(dataset['BMI'][dataset['Sex'] == 'male'], label = 'Male')
    sns.kdeplot(dataset['BMI'][dataset['Sex'] == 'female'], label = 'Female')
    plt.xlabel('Bmi')
    plt.legend()
    plt.title('Bmi Distribution by Sex')
    plt.show()

def plot_correlation_graph():
    dataset = backend.fetch_correlation_data()
    plt.figure(figsize=(15,7))
    sns.heatmap(dataset.corr(), annot=True)
    plt.title('Correlation Plot')
    plt.show()
    
plot_graphs()  

### One Hot Encoding the dataset
def one_hot_encoding_data(dataset):
    encoded_dataset = pd.get_dummies(data = dataset, columns = ['Sex', 'Smoker'])
    target_data = encoded_dataset['Charges']
    encoded_dataset['Target'] = target_data
    encoded_dataset.drop(['Charges'], axis = 1, inplace = True)
    return encoded_dataset[['Age', 'BMI', 'Children', 'Sex_female', 
                            'Sex_male', 'Smoker_no', 'Smoker_yes', 'Target']]


### Data preprocessing
def data_preprocessing(dataset):
    dataset = one_hot_encoding_data(dataset)
    X = dataset.iloc[:, : -1].values
    Y = dataset.iloc[:, -1].values
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, random_state = 27, shuffle = True)
    return X_train, X_test, Y_train, Y_test

### Random Forest Regression (100 trees)
def random_forest_regression():
    X_train, X_test, Y_train, Y_test = data_preprocessing(dataset)
    random_forest_regressor = RandomForestRegressor(n_estimators = 100, random_state = 27)
    random_forest_regressor.fit(X_train, Y_train)
    Y_pred = random_forest_regressor.predict(X_test)
    mse = round(mean_squared_error(Y_test, Y_pred), 3)
    rmse = round(sqrt(mse), 3)
    
    # Saving model to disk
    pickle.dump(random_forest_regressor, open('model.pkl','wb'))
    
    return rmse


print(random_forest_regression())
