#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 14:40:15 2019

@author: sebastien
"""

import pandas as pd
    

def time_second_conv(time):
        # time must be a datetime object
        h = time.hour
        m = time.minute
        s = time.second
        return s + m*60 + h*3600
    
def normalize_hour(time):
    #time has to be in second over 24 hours
    return time/(24*3600)

def normalize_full_column(column):
        max_val = max(column)
        for i in range(len(column)):
            column[i] /= max_val 
        return column  

def check_nan(df):
        columns_name = df.columns
        nan = pd.isna(df)
        for col in columns_name:
            print(nan[col].value_counts())        

def preprocess(df):
    
    # drop useless columns
    col_to_drop = ["from", "to", "Id", "date", "index"]
    df.drop(columns=col_to_drop, inplace=True)
    
    """====================check NaN values======================="""
    
    check_nan(df)
        
    """====================split labels======================="""
    
    labels = df.pop("delay_minutes")
    labels = pd.DataFrame(labels)
    
    """====================manage schedule_time======================="""
    
    # create year, month, day, hour columns
    df["scheduled_time"] = pd.to_datetime(df["scheduled_time"])
    df['scheduled_hour'] = [time_second_conv(d.time()) for d in df['scheduled_time']]
    df['scheduled_day'] = [d.date().day for d in df['scheduled_time']]
    df['scheduled_month'] = [d.date().month for d in df['scheduled_time']]
    df['scheduled_year'] = [d.date().year for d in df['scheduled_time']]
    
    # drop scheduled_time
    df.drop(columns=["scheduled_time"], inplace=True)
    
    """======================normalization and categorization====================="""
    
    df = pd.concat([df.drop("line", axis=1), pd.get_dummies(df["line"])], axis=1)
    df = pd.concat([df.drop("status", axis=1), pd.get_dummies(df["status"])], axis=1)
    df = pd.concat([df.drop("from_id", axis=1), pd.get_dummies(df["from_id"])], axis=1)
    df = pd.concat([df.drop("to_id", axis=1), pd.get_dummies(df["to_id"])], axis=1)
    df = pd.concat([df.drop("train_id", axis=1), pd.get_dummies(df["train_id"])], axis=1)
    
    # normalize hours
    df['scheduled_hour'] = [normalize_hour(i) for i in df['scheduled_hour']]
    
    # normalize stop sequence on the global max
    df["stop_sequence"] = normalize_full_column(df["stop_sequence"])

    return df, labels
    













