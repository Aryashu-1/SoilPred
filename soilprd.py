from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
from sklearn.model_selection import train_test_split


plant_params = pd.read_csv('./Plant_Parameters.csv')


def Normalise(X):
    return (X-X.mean())/X.std()

final_dict = {}
list_of_unique = plant_params['Plant Type'].unique()
for ind,ele in enumerate(list_of_unique):
    final_dict[ele] = ind



y = plant_params['Plant Type']
y = y.apply(lambda x : final_dict[x])
X = plant_params.iloc[:,0:9]


Xtrain,Xtest,Ytrain,Ytest = train_test_split(X,y,test_size=0.8)

k_neighbors = 10  # You can adjust the number of neighbors (k) as needed
knn_model = KNeighborsClassifier(n_neighbors=k_neighbors)
knn_model.fit(Xtrain, Ytrain)





def getPredics(datalist):
    
    cols = Xtrain.columns
    
    my_dict = {}
    
    for i in range(9):
        
        my_dict[cols[i]] = datalist[i]
    
    
    df = pd.DataFrame([my_dict])
    
    preds = knn_model.predict(df)
    
    return preds
    


import tkinter as tk

def display_data():
    result_text.delete(1.0, tk.END)  


    data_list = [float(entry_fields[i].get()) for i in range(9)]
    
    prdic = getPredics(data_list)
    
    prdic = prdic[0]


    result_text.insert(tk.END,list_of_unique[prdic])


root = tk.Tk()
root.title("Text Data Display")


entry_fields = [tk.Entry(root) for _ in range(9)]


display_button = tk.Button(root, text="Display Data", command=display_data)


result_text = tk.Text(root, height=10, width=30)


for entry_field in entry_fields:
    entry_field.pack(pady=5)

display_button.pack(pady=10)
result_text.pack(pady=10)


root.mainloop()
