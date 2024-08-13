## IMPORTS

import pandas as pd
import numpy as np
import warnings

## HELPER FUNCTIONS

def _parse_missing_data_values(data, missing_data_values):
    """
    Parse missing data values and replace them with np.nan.
    """
    if isinstance(missing_data_values, str) and "," in missing_data_values: # comma separated
        missing_data_values_list = missing_data_values.split(',')
        for i in range(len(missing_data_values_list)):
            try:
                missing_data_values_list[i] = float(missing_data_values_list[i]) # cast numbers entered as strings back to numeric
            except:
                continue
        with warnings.catch_warnings(action="ignore"):
            data = data.replace(dict.fromkeys(missing_data_values_list, np.nan)).infer_objects(copy=False)
    elif missing_data_values is not np.nan and "," not in str(missing_data_values): # single value 
        with warnings.catch_warnings(action="ignore"):
            data = data.replace(missing_data_values, np.nan).infer_objects(copy=False)
    return data

def _row_info(data):
    #ROWS SUMMARY frequencies - procedure definition
    #important numbers for rows are calculated, here it is percentage of missings in each row
    #parameters:
    #     data - input data
    #Output: distribution of missingness in rows 
    data_temp=pd.DataFrame(data.isna().sum(axis=1),columns=['MD count'])
    data_temp['MD percentage']= data.isna().mean(axis=1) 
    data_temp['count']= data_temp['MD count']
    rows_summary=data_temp.groupby(['MD percentage','MD count']).count().reset_index()
    return(rows_summary)

def _column_info(data):
    #important summaries for each column are calculated
    #parameters:
    #     data - inputtable
    #Output: important MD summaries for columns
    
    #data frame for column info/summary:
    no_rows_df=data.shape[0]
    df_temp=pd.DataFrame(data.isna().sum(),columns=['MD count'])   #number of missings in columns
    df_temp['MD percentage']= data.isna().mean()                   #percentage of missings in columns
    df_temp['not missing count']=data.shape[0]-df_temp['MD count'] #number of not missings in columns
    df_temp['unique values']= data.nunique()                       #number of unique values
    #how much of the total count of missing values is due to particular column
    influence1=data.isna().sum() #initianion (it is not optimal,can be changed to anything)
    #in next loop we are finding how much complete rows we have in data with particular variable deleted
    #so it is this number of complete rows in smaller file minus number of complete rows in the full file
    if data.shape[1]==1:
        influence1=df_temp['MD count']
    else:     
        for i in data.columns:
            influence1[i]=(data.drop(columns=i).isna().mean(axis=1)==0).sum()-(data.isna().mean(axis=1)==0).sum()
           
    df_temp['how much influencing']=influence1
    df_temp['ratio of influenced MDs']=df_temp['how much influencing']/df_temp['MD count']   #what percentage of all missings in this variable is influenced by this variable 
    df_temp['percentage rows saved']=df_temp['how much influencing']/(data.isna().mean(axis=1)>0).sum()  # what percentage of incomplete rows will be saved if this variable will be deleted
    df_temp['percentage gain of complete rows']=df_temp['how much influencing']/no_rows_df
    columns_summary=df_temp.reset_index()
    columns_summary.rename(columns={'index':'column name'}, inplace=True)
    return(columns_summary)

def _file_info(data):
    #FILE SUMMARY function as data frame - procedure definition
    #calculating overal numbers/important characteristics for the full file
    #parameters:
    #     data - input table
    #Output: important MD summaries for input data    
    labels=['number of rows', 'number of columns','MD count','number of complete rows', 'number of complete columns','number of incomplete rows', 'number of incomplete columns']
    my_list=[data.shape[0],data.shape[1],data.isna().sum().sum(),(data.isna().mean(axis=1)==0).sum(),(data.isna().mean()==0).sum(),(data.isna().mean(axis=1)>0).sum(),(data.isna().mean()>0).sum()]
    file_summary=pd.Series(data=my_list,index=labels)
    file_summary['percentage of complete rows']= file_summary['number of complete rows']/ file_summary['number of rows']
    file_summary['percentage of complete columns']= file_summary['number of complete columns']/ file_summary['number of columns']
    file_summary['data space']=file_summary['number of rows']*file_summary['number of columns']
    file_summary['MD percentage']=file_summary['MD count']/ file_summary['data space']
    file_summary['MD space']=file_summary['number of incomplete rows']*file_summary['number of incomplete columns']
    file_summary['MD space percentage']=file_summary['MD space']/file_summary['data space']
    summary=pd.DataFrame(file_summary).transpose()
    return(summary)

## USER CALLABLE FUNCTIONS

def summarize(df, missing_data_values=None, preprocess=True):
    """
    Summarize missing values across columns and rows, as well as optionally perform basic preprocessing.

    Parameters
    ----------
    df : pandas.DataFrame or array-like (pd.Series, np.ndarray, list), required
        The column(s) containing missing values.
    missing_data_values : optional (default=None)
        Additional values to recognize as missing values. 
        For multiple values, input should be formatted as a comma separated string with all missing data values.
    preprocess : optional (default=True)
        True/False flag to specify if analysis should be done on raw data or if some basic cleaning should happen first.
        Cleaning will involve removing invariant variables and empty rows and columns.

    Returns
    -------
    file_summary : pandas.DataFrame
        Dataframe summarizing missing data information across the entire input dataframe.
    row_summary : pandas.DataFrame
        Dataframe summarizing missing data information across rows.
    column_summary : pandas.DataFrame
        Dataframe summarizing missing data information across columns.
    report : pandas.DataFrame
        Dataframe containing written explanations of findings.
    preprocessed_data : pandas.DataFrame
        Dataframe containing preprocessed data; will be different than input if preprocess parameter is set to True.
    """

    #Initiation of objects
    report=pd.DataFrame({'Analysis':[],
                         'Insights':[]})
    #removing values which are representing MDs
    if missing_data_values is not None:
        df = _parse_missing_data_values(df, missing_data_values)
        
    #(Invariant variables check and removal)
    #(Empty rows and columns check and removal)
    n_empty_col=(df.isna().mean()==1).sum()
    n_empty_row=(df.isna().mean(axis=1)==1).sum()
    n_invariant=(df.nunique()==1).sum()
    separator=", "
    
    #Next will run only in case we have fully empty columns or fully empty rows or invariant variables
    if (n_empty_col>0 or n_empty_row>0 or n_invariant>0):

        #Empty rows and empty columns check
          
        column_summary_raw0=_column_info(df)
        row_summary_raw0=_row_info(df)
        file_summary_raw0=_file_info(df)
        
      
        #--------- REPORT lines creation section (START) ---------
        #invariant variables REPORT
        report_phase='Check for invariant variables'
        invariant_columns=list(column_summary_raw0[(column_summary_raw0['unique values']==1)]['column name'])
        invariant_partially=list(column_summary_raw0[(column_summary_raw0['unique values']==1)&(column_summary_raw0['MD count']>0)]['column name'])
    
        if (len(invariant_columns)==0):
            report.loc[len(report.index)] = [report_phase,'No invariant columns in the data.'] 
        if (len(invariant_columns)==1):
            if (preprocess==True):
                report.loc[len(report.index)] = [report_phase,'Column '+''.join(invariant_columns)+' is invariant (is equal always to the same value). It was removed and not used for further analysis because not bringing any information.'] 
            else:
                report.loc[len(report.index)] = [report_phase,'Column '+''.join(invariant_columns)+' is invariant (is equal always to the same value). Column was not removed from the actual analysis.'] 
        if (len(invariant_columns)>1):
            #separator=",\n"
            if (preprocess==True):
                report.loc[len(report.index)] = [report_phase,'There are {0:0.0f} invariant variables (columns with only one value). These columns were removed and not used for further analysis because not bringing any information.'.format(len(invariant_columns))] 
            else:
                report.loc[len(report.index)] = [report_phase,'There are {0:0.0f} invariant variables (columns with only one value). These columns were not removed from the analysis.'.format(len(invariant_columns))] 
            report.loc[len(report.index)] = [report_phase,'Here is the list of invariant variables: '+separator.join(invariant_columns)]
        if (len(invariant_partially)>0):
            #separator=",\n"
            report.loc[len(report.index)] = [report_phase,'There is a subset of invariant variables which have also some MDs. If the missing value represents some category, we recommend to modify respective column, add the proper value and start analysis again (in case there is a meaning of missing value, variables are in fact not invariant and should be used for analysis). List of such columns:\n'+separator.join(invariant_partially)]
        
        # REPORT for empty columns
        # number of empty columns
        report_phase='Check for empty columns'
        if (n_empty_col>0):
            if (n_empty_col==1).sum()==1:
                if (preprocess==True):
                    report.loc[len(report.index)] = [report_phase,'There is 1 column ('+list(column_summary_raw0[column_summary_raw0['unique values']==0]['column name'])[0]+') which has 0 valid values. It was removed and not used for missing data analysis because not bringing any information.'] 
                else:
                    report.loc[len(report.index)] = [report_phase,'There is 1 column ('+list(column_summary_raw0[column_summary_raw0['unique values']==0]['column name'])[0]+') which has 0 valid values. It was not removed before the analysis.'] 
            else:
                if (preprocess==True):
                    report.loc[len(report.index)] = [report_phase,'There are {0:0.0f} columns which have 0 valid values. These were removed and not used during missing data analysis because not bringing any information.'.format(n_empty_col)] 
                else:
                    report.loc[len(report.index)] = [report_phase,'There are {0:0.0f} columns which have 0 valid values. These were not removed from missing data analysis.'.format(n_empty_col)] 
                #separator=",\n"
                empty_columns=list(column_summary_raw0[column_summary_raw0['unique values']==0]['column name'])
                report.loc[len(report.index)] = [report_phase,'List of empty columns: '+separator.join(empty_columns)] 
                if (preprocess==False):
                    report.loc[len(report.index)] = [report_phase,"Empty columns are strongly influencing results of missing data analysis!"] 
        else:
            report.loc[len(report.index)] = [report_phase,"No empty columns!"] 
        #--------- REPORT lines creation section (END) ---------
        
        #removing invariant and missing columns only in case parameter preprocess is True
        if (preprocess==True):            
            #empty columns are deleted but only in case, user want to do that
            df=df[df.isna().mean()[df.isna().mean()<1].index]
         
            #invariant variables are deleted
            if df.shape[1]>0: 
            #only in case we have not empty data
                df.drop(columns=list((df.nunique()==1).index[df.nunique()==1]),inplace=True)        
                
            
        #--------- REPORT lines creation section (START) ---------
        # empty rows check       
        # number of empty rows 
        report_phase='Check for empty rows'
        n_empty_row=(df.isna().mean(axis=1)==1).sum()
        if n_empty_row>0:
            if (n_empty_row==1):
                if (preprocess==False):
                    report.loc[len(report.index)] = [report_phase,'There is 1 row which has 0 valid values (after invariant variable removal). It was removed and not used for further analysis because not bringing any information.'] 
                else:
                    report.loc[len(report.index)] = [report_phase,'There is 1 row which has 0 valid values. This row is contributing to summaries about missing data.'] 
            else:
                if (preprocess==False):
                    report.loc[len(report.index)] = [report_phase,'There are {0:0.0f} rows which have 0 valid values (after invariant variable removal). These were removed and not used for further analysis because not bringing any information.'.format(n_empty_row)]
                else:
                    report.loc[len(report.index)] = [report_phase,'There are {0:0.0f} rows which have 0 valid values. This rows are strongly contributing to summaries about missing data.'.format(n_empty_row)]
        else:
            report.loc[len(report.index)] = [report_phase,"No empty rows!"] 
        #--------- REPORT lines creation section (END) ---------
            
        #removing empty rows only in case parameter preprocess is True
        if (preprocess==True):
            #empty rows will be deleted
            if df.shape[1]>0: 
                #only in case we have still not empty data
                df=df[(df.isna().mean(axis=1)<1)]
        
        if (df.shape[0]>0 and df.shape[1]>0): 
            #only in case we have not empty data
            #####################  
               
            column_summary=_column_info(df)
            row_summary=_row_info(df)
            file_summary=_file_info(df)
                        
    
        else:
            #in this situation Raw1 is in fact empty, so not existing
            #creating file data frames for first Raw0
            column_summary=column_summary_raw0[column_summary_raw0.index==-99]  
            row_summary=row_summary_raw0[row_summary_raw0.index==-99]
            file_summary=file_summary_raw0[file_summary_raw0.index==-99]
            #row_inclusion not needed, we are not appending anything
            if (preprocess==True):
                report.loc[len(report.index)] = ['Raw data review','Data has only invariant or empty columns, not possible to analyze further.']
            else:
                report.loc[len(report.index)] = ['Raw data review','Data has only invariant or empty columns.']
            
    #Here follows the section where all checks are ok     
    else:
          
        column_summary=_column_info(df)
        row_summary=_row_info(df)
        file_summary=_file_info(df)
         
        
        #--------- REPORT lines creation section (START) ---------
        # any pre-check did not find any problem with the data       
        report.loc[len(report.index)] = ['Check for invariant variables',"No invariant columns!"] 
        report.loc[len(report.index)] = ['Check for empty columns',"No empty columns!"] 
        report.loc[len(report.index)] = ['Check for empty rows',"No empty rows!"] 
        #--------- REPORT lines creation section (END) ---------


    #Analysis after invariant check
    #(raw data results)
    if(df.shape[0]>0 and df.shape[1]>0):
        #makes sense only if data not empty
        #--------- REPORT lines creation section (START) ---------
        #some reporting options
        report_step='Raw data review'
        if (preprocess==False):
            report.loc[len(report.index)] = [report_step,'Dataset has {0:0.0f} rows and {1:0.0f} columns.'.format(file_summary['number of rows'][0],file_summary['number of columns'][0])]
        else:
            report.loc[len(report.index)] = [report_step,'Dataset (after preprocessing) has {0:0.0f} rows and {1:0.0f} columns.'.format(file_summary['number of rows'][0],file_summary['number of columns'][0])]
        report.loc[len(report.index)] = [report_step,'There are {0:0.0f} MDs ({2:0.2f}% of all data points) spread across {1:0.0f} columns.'.format(file_summary['MD count'][0],file_summary['number of incomplete columns'][0],file_summary['MD percentage'][0]*100)]
        if file_summary['MD count'].iloc[0]==0:
            report.loc[len(report.index)] = [report_step,'Congratulations! Investigated data is clean without any missing values. No further analysis needed.']
        if file_summary['percentage of complete rows'][0]<0.5:   
            report.loc[len(report.index)] = [report_step,'Data has only {0:0.2f}% complete rows.'.format(file_summary['percentage of complete rows'][0]*100)]
        else:
            report.loc[len(report.index)] = [report_step,'Data has {0:0.2f}% complete columns.'.format(file_summary['percentage of complete rows'][0]*100)]
    
        #MD space thoughts
        # idea is to give guidance what strategy might work based on shape of MD space
        param1=10   #MD fraction>=param1 - MDs sparse 
        param2=2    #MD fraction<=param2 - MDs are dense in MD space 
        param3=0.5  #PercR lower level
        param4=0.5  #PercC lower level
        param5=0.8  #PercR upper level
        param6=0.8  #PercC upper level
    
        if(file_summary['MD count'][0]>0):
            MDfraction=file_summary['MD space'][0]/file_summary['MD count'][0]
            percR=file_summary['number of incomplete rows'][0]/file_summary['number of rows'][0]
            percC=file_summary['number of incomplete columns'][0]/file_summary['number of columns'][0]
            if MDfraction>=param1:
                report.loc[len(report.index)] = [report_step,'MD space is sparse. To remove MD you might need to delete several rows or/and columns, or alternatively use MD imputation methods.'] 
            if MDfraction<=param2:
                if ((percR<=param3)&(percC<=param4)):
                    report.loc[len(report.index)] = [report_step,'MD space is dense. It is likely that strategies for removing rows or columns will lead to large amount of removed valid cases.']     
                if ((percR<=param3)&(percC>=param6)):
                     report.loc[len(report.index)] = [report_step,'MD space is dense. Based on MD space shape, we recommend to review strategies for columns removal.']     
                if ((percR>=param5)&(percC<=param4)):
                    [report_step,'MD space is dense. Based on MD space shape, we recommend to review strategies for row removal.']
                if ((percR>=param5)&(percC>=param6)):
                    [report_step,'MD space is dense; in addition MD space is large. MD handling will be extremely challenging for this dataset.']
            if ((MDfraction<=param2)&(MDfraction>=param1)):
                if ((percR<=param3)&(percC>=param6)):
                     report.loc[len(report.index)] = [report_step,'Based on MD space shape, we recommend to review strategies for column removal.']     
                if ((percR>=param5)&(percC<=param4)):
                    [report_step,'Based on MD space shape, we recommend to review strategies for rows removal.']
    
    
            if MDfraction==1:
                report.loc[len(report.index)] = [report_step,'MD structure is very simple in this dataset. All MDs are grouped within a block in MD space. Review additional graphs to identify columns and rows combinations involved.']         
    
        #--------- REPORT lines creation section (END) ---------
    #filling tables in case, they are empty (after preprocessing nothing left for analysis:
    if file_summary.shape[0]==0:
        file_summary=pd.DataFrame({'number of rows':[0],
                    'number of columns':[0],
                    'MD count':[0],
                    'number of complete rows':[0],
                    'number of complete columns':[0],
                    'number of incomplete rows':[0],
                    'number of incomplete columns':[0],
                    'percentage of complete rows':[0],
                    'percentage of complete columns':[0],
                    'data space':[0],
                    'MD percentage':[0],
                    'MD space':[0],
                    'MD space percentage':[0]})
    if row_summary.shape[0]==0:
        row_summary=pd.DataFrame({'MD percentage':[0],
                    'MD count':[0],
                    'count':[0]})
    if column_summary.shape[0]==0:
        column_summary=pd.DataFrame({'column name':['no columns in report'],
                    'MD count':[0],
                    'MD percentage':[0],
                    'not missing count':[0],
                    'unique values':[0],
                    'how much influencing':[0],
                    'ratio of influenced MDs':[0],
                    'percentage rows saved':[0],
                    'percentage gain of complete rows':[0]})
    if df.shape[1]==0 or df.shape[0]==0:  
        df=pd.DataFrame({'(empty table)':['']})
    preprocessed_data=df
    return file_summary, row_summary, column_summary, report, preprocessed_data


def compare_summary_stats(original_df, new_df, missing_data_values=None):
    """
    Compares summary statistics between raw data with missing values and a cleaned dataframe where missing values have been removed and/or imputed.

    Parameters
    ----------
    original_df : pandas.DataFrame or array-like (pd.Series, np.ndarray, list), required
        The original dataframe containing missing values.
    new_df : pandas.DataFrame or array-like (pd.Series, np.ndarray, list), required
        The new dataframe where missing values have been removed and/or imputed. Can be the output dataframe from any of the removal or imputation features.
    missing_data_values : optional (default=None)
        Additional values to recognize as missing values. 
        For multiple values, input should be formatted as a comma separated string with all missing data values.

    Returns
    -------
    descr_cont : pandas.DataFrame
        Dataframe containing min, max, 25%ile, median, mean, 75%ile, standard deviation, and size of each column.
    descr_cat : pandas.DataFrame
        Dataframe containing frequencies of categorical variables.
    cor_cont : pandas.DataFrame
        Dataframe containing difference in correlations for continuous variables.
    """

    #removing values which are representing MDs
    if missing_data_values is not None:
        original_df = _parse_missing_data_values(original_df, missing_data_values)
        new_df = _parse_missing_data_values(new_df, missing_data_values)

    #should we include in the results counts of missing data (if yes, then following parameter is False)
    not_count_mds=False
    #solving possible empty variables because empty columns causing problems 
    new_df2=new_df.dropna(axis=1,how='all')
    
    #Defining what is categorical
    categorical=list(new_df2.dtypes[new_df2.dtypes=='object'].index)
    
    #calculating frequencies of categories for categorical variables
    if len(categorical)>0:
        df_temp=pd.DataFrame({},columns=['data origin','column','category','count'])
        for i in categorical:
            df1=original_df[i].value_counts(dropna=not_count_mds).reset_index()
            df1['data origin']='Original'
            df1['column']=i
            df1['category']=df1[i]
            #df1['Count']=df1['count']
            df1.drop(columns=[i],inplace=True)
            df_temp=pd.concat([df_temp, df1])
       
        for i in categorical:
            df2=new_df[i].value_counts(dropna=not_count_mds).reset_index()
            df2['data origin']='New'
            df2['column']=i
            df2['category']=df2[i]
            #df2['count']=df2['count']
            df2.drop(columns=[i],inplace=True)
            df_temp=pd.concat([df_temp,df2])
    else:
        #this cases in when there are no categorical columns to analyze
        #df_temp=pd.DataFrame({},columns=['data origin','column','category','count']) #this is creating empty table (not good for Spotfire output, we need to decide how to handle Python implementation)
        df_temp=pd.DataFrame({'data origin':['No categorical data in clean table'], 'column':[''], 'category':[''], 'count':[0]})
    descr_cat=df_temp
    
    #calculating descriptives for continuous variables
    if len(categorical)<new_df2.shape[1]:
        descr2=new_df2.describe().transpose()
        descr1=original_df[descr2.index].describe().transpose()
        descr1['valid %']= descr1['count']/original_df.shape[0]
        descr2['valid %']= descr2['count']/new_df.shape[0]
        descr1['data origin']='Original'
        descr2['data origin']='New'
        descr_cont=pd.concat([descr1.reset_index(),descr2.reset_index()])
        descr_cont=descr_cont.rename(columns={'index': 'column'})
        
        #below is a correlation, we are creating it in the form of pairs
        cor_original_matrix=original_df[descr2.index].corr()
        cor_new_matrix=new_df2[descr2.index].corr()
        cor_dif_matrix=cor_original_matrix-cor_new_matrix
        cor_original=cor_original_matrix.reset_index().melt(id_vars=['index'])
        cor_new=cor_new_matrix.reset_index().melt(id_vars=['index'])
        cor_cont=cor_dif_matrix.reset_index().melt(id_vars=['index'])
        cor_cont.columns=['column 1', 'column 2', 'correlation difference']
        cor_cont['correlation original']=cor_original['value']
        cor_cont['correlation new']=cor_new['value']
        cor_cont['correlation abs(difference)']=abs(cor_cont['correlation difference'])
    else:
        #following might be applicable in Spotfire code maybe (not needed in Python function (need to be defined))
        descr_cont=pd.DataFrame({'data origin':['No continuous variables in new data'],
                    'column':[''],
                    'count':[0],
                    'mean':[0],
                    'std':[0],
                    'min':[0],
                    '25%':[0],
                    '50%':[0],
                    '75%':[0],
                    'max':[0],
                    'valid%':[0]})
        cor_cont=pd.DataFrame({'column 1':[''], 'column 2':[''], 'correlation difference':[0], 'correlation original':[0], 'correlation new':[0]})           
    return descr_cont, descr_cat, cor_cont