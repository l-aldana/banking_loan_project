import pandas as pd
df = pd.read_csv(r'C:\Users\Flia. Aldana Miranda\Downloads\credit_scoring_eng.csv')
print()

#showing dataframe general information:
print(df.info())
#type values of clomuns are ok. there are missing values.
print()

#finding missing values:
print(df.isna().sum())
#there are missing values in 'days_employed' and 'total_income' columns
print()

#finding relation between 'days_employed' and 'total_income' missing data:
missing_data = df[df['days_employed'].isna() & df['total_income'].isna()]
print(missing_data)
#same numbers of rows. The missing data are related to each other
print()

#checking data in 'education' column:
print(df['education'].unique())
#there are different types of formats for data.
print()

#unifying format in 'education' column
df['education'] = df['education'].str.lower()
print(df['education'].unique())
print()

#checking data in 'children' column
print(df['children'].value_counts(dropna=False))
print()

#fixing data in 'children' column:
df['children'] = df['children'].abs()
df['children'] = df['children'].replace(20, 2)
print(df['children'].value_counts(dropna=False))
print()

#checking data in 'days_employed' column:
print(df['days_employed'].value_counts(dropna=False).sort_index(axis=0, ascending=False))
#there are days that are no logical because they represent even 100 years and also there are negative years
print()

#fixing data in 'days_employed' column:
df['days_employed'] = df['days_employed'].abs()
data1 = df[df['days_employed'] < 20000]
median = data1['days_employed'].median()
df['days_employed'] = df['days_employed'].fillna(median)
df.loc[df['days_employed'] > 20000, 'days_employed'] = median
print(df['days_employed'].value_counts(dropna=False).sort_index(axis=0, ascending=False))
print()

#checking data in 'dob_years' column:
print(df['dob_years'].value_counts(dropna=False).sort_index(axis=0, ascending=False))
#there are 101 records with age = 0. This is not logical
print()

#fixing data in 'dob_years' column:
data2 = df[df['dob_years'] != 0]
mean2 = data2['dob_years'].mean()
median2 = data2['dob_years'].median()
df.loc[df['dob_years'] == 0, 'dob_years'] = median2
print(df['dob_years'].value_counts(dropna=False).sort_index(axis=0, ascending=False))
print()

#a new column will be created with categories of 'dob_years':
def age_cat(dob_years):
    if dob_years < 20:
        return '<20'
    if dob_years < 30:
        return '20-29'
    if dob_years < 40:
        return '30-39'
    if dob_years < 50:
        return '40-49'
    if dob_years < 60:
        return '50-59'
    if dob_years < 70:
        return '60-69'
    else:
        return '+70'
df['age_cat'] = df['dob_years'].apply(age_cat)
print(df.head(10))
print()

#checking data in 'family_status' column:
print(df['family_status'].unique())
#records are ok
print()

#checking data in 'gender' column:
print(df['gender'].unique())
#'XNA' eill change to 'NA' (not available)
print()

#fixing data in 'gender' column:
df.loc[df['gender'] == 'XNA', 'gender'] = 'NA'
print(df['gender'].unique())
print()

#checking data in 'gender' column:
print(df['income_type'].value_counts(dropna=False))
#records are ok
print()

#checking duplicates in dataframe
print(df.duplicated().sum())
print()

#deleting duplicates in dataframe
df = df.drop_duplicates().reset_index(drop=True)
print(df.duplicated().sum())
print()

#double-checking the dataframe info:
print(df.info())
#only missing values in 'total_income' columns
print()

#fixing data in 'total_income' column:
data3 = df[df['total_income'].notnull()]
education_mean = data3.groupby('education')['total_income'].mean()
print(education_mean)
def miss_inco(education):
    if education == "bachelor's degree":
        return education_mean.loc["bachelor's degree"]
    if education == "graduate degree":
        return education_mean.loc["graduate degree"]
    if education == "primary education":
        return education_mean.loc["primary education"]
    if education == "secondary education":
        return education_mean.loc["secondary education"]
    if education == "some college":
        return education_mean.loc["some college"]
df.loc[df['total_income'].isna(), 'total_income'] = df['education'].apply(miss_inco)
print(df.info())
#there are no more missing values
print()

#clasification of 'purpose' column:
print(df['purpose'].value_counts(dropna=False).sort_index(axis=0, ascending=False))
#main groups of 'purpose' column: wedding, education, real estate, buying a car.
def purpose_cat(purpose):
    if 'wedding' in purpose:
        return 'wedding'
    if 'educat' in purpose:
        return 'education'
    if 'university' in purpose:
        return 'education'
    if 'real estate' in purpose:
        return 'real estate'
    if 'hous' in purpose:
        return 'real estate'
    if 'property' in purpose:
        return 'real estate'
    if 'car' in purpose:
        return 'buying a car'
df['purpose_cat'] = df['purpose'].apply(purpose_cat)
print(df['purpose_cat'].value_counts(dropna=False).sort_index(axis=0, ascending=False))
print()

#clasification of 'total_income' column:
def income_cat(total_income):
    if total_income < 100000:
        return 'low income'
    if total_income < 200000:
        return 'medium income'
    else:
        return 'high income'
df['income_cat'] = df['total_income'].apply(income_cat)
print(df['income_cat'].value_counts(dropna=False).sort_index(axis=0, ascending=False))
print()

#finding relation between 'children' and 'debt':
print(df.groupby('children')['debt'].mean()*100)
print()

#finding relation between 'family_status' and 'debt':
print(df.groupby('family_status')['debt'].mean()*100)
print()

#finding relation between 'income_cat' and 'debt':
print(df.groupby('income_cat')['debt'].mean()*100)
print()

#finding relation between 'purpose_cat' and 'debt':
print(df.groupby('purpose_cat')['debt'].mean()*100)