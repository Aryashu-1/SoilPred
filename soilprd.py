from cProfile import label
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import tkinter as tk
from tkinter import messagebox

# Load your dataset
plant_params = pd.read_csv('./Plant_Parameters.csv')

# Function to normalize the data
def Normalise(X):
    return (X - X.mean()) / X.std()

# Mapping unique plant types to numerical values
final_dict = {}
list_of_unique = plant_params['Plant Type'].unique()
for ind, ele in enumerate(list_of_unique):
    final_dict[ele] = ind

# Prepare features (X) and target variable (y)
y = plant_params['Plant Type']
y = y.apply(lambda x: final_dict[x])
X = plant_params.iloc[:, 0:9]

# Split the data into training and testing sets
Xtrain, Xtest, Ytrain, Ytest = train_test_split(X, y, test_size=0.8)

# Build KNN model
k_neighbors = 10
knn_model = KNeighborsClassifier(n_neighbors=k_neighbors)
knn_model.fit(Xtrain, Ytrain)

# Function to get predictions based on user input
def getPredictions(datalist):
    cols = Xtrain.columns
    my_dict = {}
    
    for i in range(9):
        my_dict[cols[i]] = datalist[i]
    
    df = pd.DataFrame([my_dict])
    preds = knn_model.predict(df)
    
    return preds

# Function to display data and predictions
def display_data():
    result_text.delete(1.0, tk.END)  
    
    try:
        data_list = [float(entry_fields[i].get()) for i in range(9)]
    except ValueError:
        result_text.insert(tk.END, "ENTER PROPER VALUES")
        result_text.config(bg='lightcoral', fg='white')  # Set background and text color for error message
        return
    
    predictions = getPredictions(data_list)
    predicted_plant_type = list_of_unique[predictions[0]]
    
    result_text.insert(tk.END, f"Predicted best suitable Plant for your soil: {predicted_plant_type}")
    result_text.config(bg='lightgreen', fg='blue')  # Set background and text color

# Placeholder function for 'About Us'
def about_us():
    messagebox.showinfo("About Us", "This is a Suitable Crop type prediction application.\n\nVersion: 1.0")

# Placeholder function for 'Contact Us'
def contact_us():
    messagebox.showinfo("Contact Us", "For any queries, please email us at dtteam4@gmail.com")

# Function to reset layout to default
def home():
    clear_entry_fields()
    reset_layout()

# Placeholder function for 'New'
def new_function():
    clear_entry_fields()

# Function to clear entry fields
def clear_entry_fields():
    for entry_field in entry_fields:
        entry_field.delete(0, tk.END)

# Function to reset layout to default
def reset_layout():
    for i, label in enumerate(labels):
        tk.Label(root, text=label, bg='lightblue', font=('Helvetica', 14)).grid(row=i, column=0, sticky='e', pady=(10, 5), padx=(20, 5))  # Set label background color and font
        entry_fields[i].grid(row=i, column=1, pady=(10, 5), padx=(0, 10), ipadx=10, ipady=5, sticky='w')  # Increase text input size and add padding

# Create the main window
root = tk.Tk()
root.title("Suiatble Crop Prediction App")

# Set window size
window_width = 800
window_height = 600

# Load background image and make it cover the entire window
background_image = tk.PhotoImage(file="./crop_prediction_bg 1.png")
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

# Center window on the screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Menu Bar
menubar = tk.Menu(root)

# File Menu
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=new_function)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.destroy)
menubar.add_cascade(label="File", menu=filemenu)
# Options Menu
optionsmenu = tk.Menu(menubar, tearoff=0)
optionsmenu.add_command(label="Home", command=home)
optionsmenu.add_command(label="About Us", command=about_us)
optionsmenu.add_command(label="Contact Us", command=contact_us)
menubar.add_cascade(label="Options", menu=optionsmenu)

# Adding the menu bar to the root window
root.config(menu=menubar)
# Create entry fields and labels
entry_fields = [tk.Entry(root, font=('Helvetica', 12)) for _ in range(9)]
labels = ['pH', 'Soil EC', 'Phosphorus', 'Potassium', 'Urea', 'T.S.P', 'M.O.P', 'Moisture', 'Temperature']

# Configure row and column to center the grid
for i in range(len(labels) + 2):  # +2 for the button and result_text
    root.grid_rowconfigure(i, weight=1)
    root.grid_columnconfigure(i, weight=1)


reset_layout()

# Display button
display_button = tk.Button(root, text="Display Data", command=display_data, bg='orange', fg='white', font=('Helvetica', 14), relief=tk.RIDGE, bd=5)  # Set button colors and style
display_button.grid(row=len(labels), column=0, columnspan=2, pady=10, sticky='n')

# Result text box
result_text = tk.Text(root, height=2, width=30)
result_text.grid(row=len(labels)+1, column=0, columnspan=2, pady=10, sticky='n')

# Start the main loop
root.mainloop()
