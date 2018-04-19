from tkinter import Tk, Button, Label, Entry
from tkinter import mainloop
import application as model

def callback():
    result = model.app(e.get(), e1.get())
    if(result.prediction == "Y"):
        pred_string = "Approval Status: APPROVED"
    else:
        pred_string = "Approval Status: NOT APPROVED"
    
    
    if(result.water_data is not None):
        water_string = "The number of water bodies near the site are: " + str(result.water_data.shape[0])
    else:
        water_string = " "
    
    if(result.earthquake_data is not None):
        earthquake_string = "The number of earthquakes in the region: " + str(result.earthquake_data.shape[0])
    else:
        earthquake_string = " "
        
    if(result.rules is not None):
        rules_sub = result.rules.iloc[:,1:4]
        #rules_sub = rules_sub[[1,2]]
        rules_string = "The following rules apply to the location: \n" + str(rules_sub)
    else:
        rules_string = " "
        
    if((result.weather_data is not None) and (result.weather_data.empty == False)):
        weather_string = str(result.weather_data)
    else:
        weather_string = " " 
    
    values = [result.prediction_df[0][0],result.prediction_df[0][1],result.prediction_df[0][2],result.prediction_df[0][3],result.prediction_df[0][4],result.prediction_df[0][5],result.prediction_df[0][6],result.prediction_df[0][7]]
    value_strings = ["","","","","","","",""]
    
    i = 0
    while i<len(values):
        if(values[i]==3):
            value_strings[i] = "Highly favorable"
        elif(values[i]==2):
            value_strings[i] = "Favorable"
        elif(values[i]==1):
            value_strings[i] = "Less favorable"
        elif(values[i]==-1):
            value_strings[i] = "Data not available"

        i = i+1
                        
    l2["text"] = pred_string + "\n" + water_string + "\n" + earthquake_string + "\n" 
    prediction_string = "Seaport: "+value_strings[0]+"\n Land Price: "+value_strings[1]+"\n Oil Reserve: "+value_strings[2]+"\n Existing Plants: "+value_strings[3]+"\n Disasters: "+value_strings[4]+"\n Railroad: "+value_strings[5]+"\n Population Density: "+value_strings[6]+"\n Elevation: "+value_strings[7]
    l3["text"] = rules_string  + "\n" + weather_string + "\n" + prediction_string 


master = Tk()
master .minsize(300,300)
master .geometry("620x400")
master .title("Environmental genome")

b = Button(master, text="Let's check", command=callback)
b.place(x=220, y=60)

l = Label(master, text="Enter zipcode:")
l.place(x=130, y=0)

l1 = Label(master, text="Enter radius:")
l1.place(x=130, y=18)

l2 = Label(master, text="")
l2.place(x=130, y=36)

l3 = Label(master, text="")
l3.place(x=130, y=100)

l4 = Label(master, text="")
l4.place(x=130, y=72)

e = Entry(master)
e.place(x=10, y=100)
e.pack()

e1 = Entry(master)
e1.place(x=20, y=150)
e1.pack()

mainloop()
