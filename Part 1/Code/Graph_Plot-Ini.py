
# coding: utf-8

# Create CSV data for Part 1 and Part 2

# In[ ]:
import pandas as pd

Final_data_df = pd.read_csv('FinalData.csv', encoding = 'ISO-8859-1')
Input2_df = pd.read_csv('ds2.csv')
Data_zero_column=Final_data_df.loc[Final_data_df['List ID'] == 1].copy()
Data_zero_column.reset_index(drop=True,inplace=True)
Data_zero_column.columns.values[6:]=Input2_df['Word']
Data_zero_column.to_csv('ListID_zero_data.csv')
vertical_sum=Data_zero_column.loc[:,'customer':'automation'].sum(axis=0)
vertical_sum.to_frame(name=None)
vertical_sum.to_csv('Histogram_data.csv')


# Create CSV data for Part 1 and Part 2

# In[ ]:


Final_data_df = pd.read_csv('FinalData.csv', encoding = 'ISO-8859-1')
Input2_df = pd.read_csv('ds1.csv')
Data_zero_column=Final_data_df.loc[Final_data_df['List ID'] == 0].copy()
Data_zero_column.reset_index(drop=True,inplace=True)
Data_zero_column.columns.values[6:]=Input2_df['Word']
Data_zero_column.to_csv('ListID_one_data.csv')
vertical_sum=Data_zero_column.loc[:,'customer':'biometric'].sum(axis=0)
vertical_sum.to_frame(name=None)
vertical_sum.to_csv('List_freqn_Histogram_data.csv')

