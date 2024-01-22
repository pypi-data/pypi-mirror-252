import pandas as pd
import numpy as np
import re
import os  #for using path.join so that file path specified works in every operating system
# USE ARGPARSE FOR COMMAND LINE UTILITY
# import argparse

#Find topsis score from eucledian distance of idela positive and ideal_negative
def Euclidean_Distance( sample, Attribute_Type):
    Positive_Ideal_Point = Ideal_Solution(sample, Attribute_Type)[0]
    Negative_Ideal_Point = Ideal_Solution(sample, Attribute_Type)[1]

    Negative_Si = np.sum((sample-Negative_Ideal_Point)**2, axis = 1)**0.5
    Positive_Si = np.sum((sample-Positive_Ideal_Point)**2, axis = 1)**0.5
    C = Negative_Si/(Negative_Si + Positive_Si)
    return (sample,C)

def Weight_Prod(data, w):
    if sum(w) != 1:
        print("Shape of w is not satisfied.w must be equal 1")
    else:
        if data.shape[1] != len(w):
            print("Shape of w is not satisfied.")
        else:
            for i in range (0, data.shape[1]):
                data.iloc[:, i] = data.iloc[:, i]*w[i]
                
        return data

def Ideal_Solution(sample, Attribute_Type):
    Positive_Ideal_Solutions = []
    Negative_Ideal_Solutions = []
    for i in range(0, len(Attribute_Type)):
        if Attribute_Type[i] == "+":
            Positive_Ideal = max(sample.iloc[:, i]) 
            Negative_Ideal = min(sample.iloc[:, i])
            
            Positive_Ideal_Solutions.append(Positive_Ideal)
            Negative_Ideal_Solutions.append(Negative_Ideal)
        elif Attribute_Type[i] == "-":
            Positive_Ideal = min(sample.iloc[:, i]) 
            Negative_Ideal = max(sample.iloc[:, i])
        
            Positive_Ideal_Solutions.append(Positive_Ideal)
            Negative_Ideal_Solutions.append(Negative_Ideal)
            
    return (Positive_Ideal_Solutions, Negative_Ideal_Solutions)





def topsis(weights,impacts,inputfilename,outputfilename):
    # parser = argparse.ArgumentParser(description ='Kuch bhi')
    # p1=parser.add_argument('Weights',
    #                     type = str,
    #                     help ='Enter Weights')
    # p2=parser.add_argument('Impact',
    #                     type = str,
    #                     help ='Enter Impact')

    # p3=parser.add_argument(dest ='inputfilename',
    #                     type=str,
    #                     help ='input csv file name')

    # p4=parser.add_argument(dest ='outputfilename',
    #                     type=str,
    #                     help ='Output csv file name')

    # args = parser.parse_args()

    # weights=args.Weights.split(',')
    weight=[float(x) for x in weights]
    # print(weight)

    # impacts=args.Impact
    impacts=impacts.split(',')
    # print(impacts)



    # RAISE EXCEPTIONS
    # #1.
    # if(len(weight)!=len(impacts)):
    #     raise argparse.ArgumentError(p2,"Size of Weights and dfs")

    #2.
    if (bool(re.match(r'^[0-9.,]*$',weights)))!=True:
        raise Exception("Input Weights or Impact should only contain numbers separated by comma")
    # if(bool(re.match(r'^[+-,]*$', args.Impact))!=True):
    #     raise Exception('kya bekar sa impact')

    # print(args.outputfilename)


    # 4.
    # File exception handling
    try:
        data=pd.read_excel(os.path.join(inputfilename))
    except:
        raise Exception("File not found")
    else:
        if(data.shape[1]<3):
            raise Exception("input csv file must contain 3 or more columns")
        if all((data.dtypes[1:]) =='float')!=True:
            raise Exception("All columns after 1 should be numeric")
        


    # MAIN PROGRAM FOR TOPSIS

    #All Inputs:
    #1.w
    w=weight
    #2.Attribute type
    a=impacts
    # Drop first Column Which is Categorical
    sample=data.iloc[:,1:]


    # Find root sum sqaures of individual columns
    rss=[]
    for i in sample.columns:
        root_sum_squares=sample[i].apply(lambda x:pow(x,2))
        rss.append(pow(root_sum_squares.sum(),1/2))
    rss

    # Normalised Decision Matrix
    for i in range(0,sample.shape[1]):
        sample.iloc[:,i]=sample.iloc[:,i].div(rss[i])


    #Normalised Weighted Decision Matrix


    Weight_Prod(sample,w)


    # Find Ideal and Worst Solution



    Output=Euclidean_Distance(sample,a)

    Scores=pd.DataFrame(Output[1])

    df=pd.concat([data, Scores], axis=1)
    df.rename(columns = {0: "Topsis Score"},  
            inplace = True) 
    df["rank"]=(df["Topsis Score"].rank(ascending=False)).astype(int)
    df.sort_values(by="rank",inplace=True)


    #Generating output
    df.to_csv(outputfilename)
