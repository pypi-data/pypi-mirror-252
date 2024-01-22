import pandas as pd
import numpy as np 
import sys
import os



# For raising custom errors
class MyCustomError(Exception):
    def __init__(self, message="An error has occured"):
        self.message = message
        super().__init__(self.message)

    
def topsis(dec_matrix, weights, impacts):
    squared_decision_matrix = dec_matrix**2
    sum_elements_bycol = (squared_decision_matrix).sum(axis=0)
    norm_matrix = dec_matrix/np.sqrt(sum_elements_bycol)

    weighted_matrix = norm_matrix * weights
  
    ideal = []
    negative_ideal = []
    
    for i in range(0, len(impacts)):
        if impacts[i] == "+":
            ideal.append(np.max(weighted_matrix[:, i]))
            negative_ideal.append(np.min(weighted_matrix[:, i]))
        else:
            ideal.append(np.min(weighted_matrix[:, i]))
            negative_ideal.append(np.max(weighted_matrix[:, i]))

    S_ideal = np.sqrt(((weighted_matrix - ideal)**2).sum(axis=1))
    S_negative_ideal = np.sqrt(((weighted_matrix - negative_ideal)**2).sum(axis=1))
    
    closeness = S_negative_ideal/(S_negative_ideal + S_ideal)
    
    rank = np.argsort(closeness)[::-1] + 1

    return closeness,rank



def main():
    # Getting all the parameters from the command line

    script_name = sys.argv[0]
    try:
        arg1 = sys.argv[1]
        arg2 = sys.argv[2]
        arg3 = sys.argv[3]
        arg4 = sys.argv[4]
    except IndexError:
        print("Enter appropriate number of arguments!")
        sys.exit()

    # try:
    #     if script_name.split('.')[0]+'-data' != arg1.split('.')[0] or len(arg1.split('.')[0].split('-')) != 2 or arg1.split('.')[0].split('-')[1] != 'data':
    #         raise MyCustomError(f"The input file is wrongly formatted! {len(arg1.split('.')[0].split('-'))} and {arg1.split('.')[0].split('-')[1]}")
    # except MyCustomError as e:
    #     print(e)
    #     sys.exit()

    # # Checking for valid output file
    # try:
    #     split_ = arg4.split('.')
    #     if len(split_) != 2:
    #         raise MyCustomError("The output file name is wrongly formatted as it isnt any file!")
    #     if split_[-1] != 'csv':
    #         raise MyCustomError("The output file name is wrongly formatted as it isnt a csv file!")
    #     # if split_[0] != script_name.split('.')[0]+'-result':
    #     #     raise MyCustomError(f"The output file name is wrongly formatted! it should be {arg1}-result.csv")
    # except MyCustomError as e: 
    #     print(e)
    #     sys.exit()

    # final_destination = arg4

    # Checking if the weights are numerical
    try:
        weights = [float(s) for s in arg2[0::2]]
    except ValueError:
        print("Weights should strictly be floating numbers!")
        sys.exit()



    # Checking if the impacts signs are either + or -
    def check_correct_impacts(sign):
        if sign!='+' and sign!='-':
            raise MyCustomError("Impact sign Should be either + or -!")

    try:
        impacts = [s for s in arg3[0::2]]
        for s in impacts:
            check_correct_impacts(s)
    except MyCustomError as e:
        print(e)
        sys.exit()


    # Checking if the input file exists or not
    current_directory = os.getcwd()

    try:
        dataframe = pd.read_csv(f'{current_directory}/{arg1}')
    except:
        print(f"File '{arg1}' doesn't exists in the current directory!")
        sys.exit()


    # All the exceptions regarding the dataframe-
        
    # First let us see if the dataframe has atleast 3 columns-
        

    def check_atleast3_col(val):
        if val<3:
            raise MyCustomError("csv file needs atleast 3 columns")
        
        
    try:
        check_atleast3_col(dataframe.shape[1])
    except MyCustomError as e:
        print(e)
        sys.exit()

    # Checking if the first column is model name
        
    def check_if_first_col(dataframe):
        for ind,name in enumerate(dataframe[dataframe.columns[0]]):
            if name[0] != 'M' and ind != name[-1]:
                print('error')
                raise MyCustomError("Models name isnt in proper format!")

    try:
        check_if_first_col(dataframe)
    except MyCustomError as e:
        print(e)
        sys.exit()



    data_slice = dataframe.iloc[:,1:]

    # Checking for non numeric entries in the dataframe

    try:
        data_slice = np.array(data_slice)
    except:
        print("The parameters in the csv file isn't in numerical format!")

    # Checking for appropriate number of entries in the impacts and weights in the args
        
    def checking_for_impacts(data_slice,impacts):
        if data_slice.shape[1] != len(impacts):
            raise MyCustomError(f"Shape of impacts isn't same as the total paramaters , impacts has {len(impacts)} length and there are {data_slice.shape[1]} parameters")
        
    def checking_for_weights(data_slice,weights):
        if data_slice.shape[1] != len(weights):
            raise MyCustomError(f"Shape of weights isn't same as the total paramaters , weights has {len(weights)} length and there are {data_slice.shape[1]} parameters")
        
    try:
        checking_for_impacts(data_slice,impacts)
    except MyCustomError as e:
        print(e)
        sys.exit()


    try:
        checking_for_weights(data_slice,weights)
    except MyCustomError as e:
        print(e)
        sys.exit()

        # ... The rest of your existing code ...

    Score , Rank = topsis(data_slice, weights, impacts)
    dataframe['Topsis Score'] = Score

    new_r = Rank.copy()
    
    for ind,r in enumerate(Rank):
        new_r[r-1] = ind+1

    dataframe['Rank'] = new_r
    

    print(dataframe)
    dataframe.to_csv(arg4, index=False)

if __name__ == "__main__":
    main()