from tkinter import *
from tkinter import ttk
from ttkbootstrap import Style
import ctypes
import pandas as pd
import atexit
from datetime import date
import numpy as np
import matplotlib.pyplot as plt

user32 = ctypes.windll.user32
ctypes.windll.shcore.SetProcessDpiAwareness(1)

totals = []
MaxAmount = [float(2000), float(55), float(30), float(66), float(150), float(90), float(30)]
Proportions = []
Today_Temp = [["Item","Calories","Protein (g)","Saturated Fat (g)","Unsaturated Fat (g)","Carbohydrate (g)","Sugar (g)","Fibre (g)"]]
pastFood_df = pd.read_csv("food_repo.csv")
todayFood_df = pd.read_csv("ConsumedToday.csv")
recordsFood_df = pd.read_csv("PastRecords.csv")

# Functions ####
def clearInputs():
    itemInput.delete(0, END)
    calInput.delete(0, END)
    proInput.delete(0, END)
    sfInput.delete(0, END)
    usfInput.delete(0, END)
    carInput.delete(0, END)
    sugInput.delete(0, END)
    fibInput.delete(0, END)

def add_pastfood():
    if len(itemInput.get()) != 0:
        getNewRepo = [
            str(itemInput.get()), calInput.get(), proInput.get(),
            sfInput.get(), usfInput.get(), carInput.get(),
            sugInput.get(), fibInput.get()
        ]
        for entry in getNewRepo[1:len(getNewRepo)]:
            try:
                # Convert it into integer
                int(entry)
            except ValueError:
                try:
                    # Convert it into float
                    float(entry)
                except ValueError:
                    return None
        pastFoodTV.insert("", index=0, values=getNewRepo)
        clearInputs()
        global pastFood_df

        newRow = len(pastFood_df)
        pastFood_df.loc[newRow] = getNewRepo

def get_pastfood():
    global pastFood_df
    # clear_pastfood()

    pastFoodTV["columns"] = list(pastFood_df.columns)
    pastFoodTV["show"] = "headings"

    # Column Structure
    pastFoodTV.column("Item", width = 120, minwidth = 1, anchor = W)
    pastFoodTV.column("Calories", width=75, minwidth=1, anchor=W)
    pastFoodTV.column("Protein (g)", width=75, minwidth=1, anchor=W)
    pastFoodTV.column("Saturated Fat (g)", width=130, minwidth=1, anchor=W)
    pastFoodTV.column("Unsaturated Fat (g)", width=130, minwidth=1, anchor=W)
    pastFoodTV.column("Carbohydrate (g)", width=130, minwidth=1, anchor=W)
    pastFoodTV.column("Sugar (g)", width=75, minwidth=1, anchor=W)
    pastFoodTV.column("Fibre (g)", width=75, minwidth=1, anchor=W)

    # Headers
    for column in pastFoodTV["columns"]:
        pastFoodTV.heading(column, text=column, anchor = W)

    # Data
    pastFoodRows = pastFood_df.to_numpy().tolist()
    for row in pastFoodRows:
        pastFoodTV.insert("", "end", values=row)

def getTodayFood():
    global todayFood_df

    todayFoodTV["columns"] = list(todayFood_df.columns)
    todayFoodTV["show"] = "headings"

    # Column Structure
    todayFoodTV.column("Item", width=120, minwidth=1, anchor=W)
    todayFoodTV.column("Calories", width=75, minwidth=1, anchor=W)
    todayFoodTV.column("Protein (g)", width=75, minwidth=1, anchor=W)
    todayFoodTV.column("Saturated Fat (g)", width=130, minwidth=1, anchor=W)
    todayFoodTV.column("Unsaturated Fat (g)", width=130, minwidth=1, anchor=W)
    todayFoodTV.column("Carbohydrate (g)", width=130, minwidth=1, anchor=W)
    todayFoodTV.column("Sugar (g)", width=75, minwidth=1, anchor=W)
    todayFoodTV.column("Fibre (g)", width=75, minwidth=1, anchor=W)

    # Headers
    for columnToday in todayFoodTV["columns"]:
        todayFoodTV.heading(columnToday, text=columnToday, anchor = W)

    # Data
    todayFoodRows = todayFood_df.to_numpy().tolist()
    for row in todayFoodRows:
        todayFoodTV.insert("", "end", values=row)

def selectItem(self):
    global Today_Temp

    SelectedItem = pastFoodTV.focus()
    pastFoodDict = dict(pastFoodTV.item(SelectedItem))
    SelectedItem = pastFoodDict['values']
    # Data
    todayFoodTV.insert("", index=0, values=SelectedItem)

    Today_Temp.append(SelectedItem)
    Totals()

def makeRepoInputHeaders():
    inputRepoFrameTV["columns"] = list(todayFood_df.columns)
    inputRepoFrameTV["show"] = "headings"
    inputRepoFrameTV.column("Item", width=120, minwidth=1, anchor=W)
    inputRepoFrameTV.column("Calories", width=75, minwidth=1, anchor=W)
    inputRepoFrameTV.column("Protein (g)", width=75, minwidth=1, anchor=W)
    inputRepoFrameTV.column("Saturated Fat (g)", width=130, minwidth=1, anchor=W)
    inputRepoFrameTV.column("Unsaturated Fat (g)", width=130, minwidth=1, anchor=W)
    inputRepoFrameTV.column("Carbohydrate (g)", width=130, minwidth=1, anchor=W)
    inputRepoFrameTV.column("Sugar (g)", width=75, minwidth=1, anchor=W)
    inputRepoFrameTV.column("Fibre (g)", width=75, minwidth=1, anchor=W)

    # Headers
    for columnToday in todayFoodTV["columns"]:
        inputRepoFrameTV.heading(columnToday, text=columnToday, anchor = W)

def makeTotalsHeaders():
    global MaxAmount
    totalsFrameTV["columns"] = ["Calories", "Protein (g)",
        "Saturated Fat (g)", "Unsaturated Fat (g)",
        "Carbohydrate (g)", "Sugar (g)", "Fibre (g)"]

    totalsFrameTV["show"] = "headings"
    totalsFrameTV.column("Calories", width=75, minwidth=1, anchor=W)
    totalsFrameTV.column("Protein (g)", width=75, minwidth=1, anchor=W)
    totalsFrameTV.column("Saturated Fat (g)", width=130, minwidth=1, anchor=W)
    totalsFrameTV.column("Unsaturated Fat (g)", width=130, minwidth=1, anchor=W)
    totalsFrameTV.column("Carbohydrate (g)", width=130, minwidth=1, anchor=W)
    totalsFrameTV.column("Sugar (g)", width=75, minwidth=1, anchor=W)
    totalsFrameTV.column("Fibre (g)", width=75, minwidth=1, anchor=W)

    global todayFood_df

    Initial_Totals = []

    for l in range(len(todayFood_df.columns)):
        try:
            Initial_Totals.append(float(todayFood_df[todayFood_df.columns[l]].sum()))
        except ValueError:
            pass

    Initial_Totals = [round(g, 1) for g in Initial_Totals]
    totalsFrameTV.insert("", "end", values= Initial_Totals)

    # Headers
    for columnTotals in totalsFrameTV["columns"]:
        totalsFrameTV.heading(columnTotals, text=columnTotals, anchor = W)

    propFrameTV["columns"] = ["Calories (%)", "Protein (%)",
        "Saturated Fat (%)", "Unsaturated Fat (%)",
        "Carbohydrate (%)", "Sugar (%)", "Fibre (%)"]

    propFrameTV["show"] = "headings"
    propFrameTV.column("Calories (%)", width=75, minwidth=1, anchor=W)
    propFrameTV.column("Protein (%)", width=75, minwidth=1, anchor=W)
    propFrameTV.column("Saturated Fat (%)", width=130, minwidth=1, anchor=W)
    propFrameTV.column("Unsaturated Fat (%)", width=130, minwidth=1, anchor=W)
    propFrameTV.column("Carbohydrate (%)", width=130, minwidth=1, anchor=W)
    propFrameTV.column("Sugar (%)", width=75, minwidth=1, anchor=W)
    propFrameTV.column("Fibre (%)", width=75, minwidth=1, anchor=W)

    # Headers
    for columnProps in propFrameTV["columns"]:
        propFrameTV.heading(columnProps, text=columnProps, anchor = W)

    ini_proportions = [y / z for y, z in zip(Initial_Totals, MaxAmount)]
    ini_proportions = [(e*100) for e in ini_proportions]
    ini_proportions = [ round(elem, 2) for elem in ini_proportions ]

    propFrameTV.insert("", "end", values=ini_proportions)

def endFunction():
    global pastFood_df
    global todayFood_df
    # Save Repo
    pastFood_df.to_csv('food_repo.csv', index=False)

    # Save today
    global Today_Temp

    Today_Temp = pd.DataFrame(Today_Temp[1:], columns=Today_Temp[0])
    Today_Final = Today_Temp.append(todayFood_df)
    Today_Final.to_csv("ConsumedToday.csv", index=False)

def getTotal(column = 1):
    global totals

    tot = 0
    tree = todayFoodTV
    for child in tree.get_children():
        tot += float(tree.item(child, 'values')[column])
    # print(tot)
    totals.append(tot)

def Totals():
    global MaxAmount

    getTotal(1)
    getTotal(2)
    getTotal(3)
    getTotal(4)
    getTotal(5)
    getTotal(6)
    getTotal(7)

    final_totals = (totals[-7:])
    final_totals = [round(g, 1) for g in final_totals]

    proportions = [c / d for c, d in zip(final_totals, MaxAmount)]
    proportions = [(e*100) for e in proportions]
    proportions = [ round(elem, 2) for elem in proportions ]

    # print(proportions)
    totalsFrameTV.delete(*totalsFrameTV.get_children())
    totalsFrameTV.insert("", "end", values=final_totals)

    propFrameTV.delete(*propFrameTV.get_children())
    propFrameTV.insert("", "end", values=proportions)

def newDay():
    if len(todayFoodTV.get_children()) > 0:
        global todayFood_df
        global Today_Temp
        global totals

        todayFood_df = todayFood_df[0:0]
        todayFood_df.to_csv("ConsumedToday.csv", index=False)

        insertNewRecord()

        todayFoodTV.delete(*todayFoodTV.get_children())
        totalsFrameTV.delete(*totalsFrameTV.get_children())
        totalsFrameTV.insert("", "end", values=[0,0,0,0,0,0,0])

        propFrameTV.delete(*propFrameTV.get_children())
        propFrameTV.insert("", "end", values=[0,0,0,0,0,0,0])

        Today_Temp = [["Item", "Calories", "Protein (g)", "Saturated Fat (g)", "Unsaturated Fat (g)", "Carbohydrate (g)", "Sugar (g)", "Fibre (g)"]]

def getRecords():
    global recordsFood_df

    pastTotalsFrameTV["columns"] = list(recordsFood_df.columns)
    pastTotalsFrameTV["show"] = "headings"

    # Column Structure
    pastTotalsFrameTV.column("Date", width=80, minwidth=1, anchor=W)
    pastTotalsFrameTV.column("Calories", width=75, minwidth=1, anchor=W)
    pastTotalsFrameTV.column("Protein (g)", width=75, minwidth=1, anchor=W)
    pastTotalsFrameTV.column("Saturated Fat (g)", width=130, minwidth=1, anchor=W)
    pastTotalsFrameTV.column("Unsaturated Fat (g)", width=130, minwidth=1, anchor=W)
    pastTotalsFrameTV.column("Carbohydrate (g)", width=130, minwidth=1, anchor=W)
    pastTotalsFrameTV.column("Sugar (g)", width=75, minwidth=1, anchor=W)
    pastTotalsFrameTV.column("Fibre (g)", width=75, minwidth=1, anchor=W)

    # Headers
    for column in pastTotalsFrameTV["columns"]:
        pastTotalsFrameTV.heading(column, text=column, anchor=W)

    pastPropFrameTV["columns"] = ["Date", "Calories (%)", "Protein (%)",
        "Saturated Fat (%)", "Unsaturated Fat (%)",
        "Carbohydrate (%)", "Sugar (%)", "Fibre (%)"]

    pastPropFrameTV["show"] = "headings"
    pastPropFrameTV.column("Date", width=80, minwidth=1, anchor=W)
    pastPropFrameTV.column("Calories (%)", width=75, minwidth=1, anchor=W)
    pastPropFrameTV.column("Protein (%)", width=75, minwidth=1, anchor=W)
    pastPropFrameTV.column("Saturated Fat (%)", width=130, minwidth=1, anchor=W)
    pastPropFrameTV.column("Unsaturated Fat (%)", width=130, minwidth=1, anchor=W)
    pastPropFrameTV.column("Carbohydrate (%)", width=130, minwidth=1, anchor=W)
    pastPropFrameTV.column("Sugar (%)", width=75, minwidth=1, anchor=W)
    pastPropFrameTV.column("Fibre (%)", width=75, minwidth=1, anchor=W)

    # Headers
    for column in pastPropFrameTV["columns"]:
        pastPropFrameTV.heading(column, text=column, anchor=W)

    # Data
    recordFoodRows = recordsFood_df.to_numpy().tolist()
    for row in recordFoodRows:
        pastTotalsFrameTV.insert("", "end", values=row)
        temp_date = row[0]
        temp_record = row[1:]
        pro_record = [c / d for c, d in zip(temp_record, MaxAmount)]
        pro_record = [(e * 100) for e in pro_record]
        pro_record = [round(elem, 2) for elem in pro_record]
        pro_record = [temp_date] + pro_record

        pastPropFrameTV.insert("", "end", values=pro_record)

def insertNewRecord():
    record_total = []
    global recordsFood_df

    for i in range(0,7):
        for child in totalsFrameTV.get_children():
            record_temp = float(totalsFrameTV.item(child, 'values')[i])
        record_total.append(record_temp)


    pro_record2 = [c / d for c, d in zip(record_total, MaxAmount)]
    pro_record2 = [(e * 100) for e in pro_record2]

    record_total = [round(elem, 1) for elem in record_total]
    pro_record2 = [round(elem, 2) for elem in pro_record2]

    record_total = [date.today().strftime("%d/%m/%Y")] + record_total
    pro_record2 = [date.today().strftime("%d/%m/%Y")] + pro_record2

    pastTotalsFrameTV.insert("",index=0,values = record_total)
    pastPropFrameTV.insert("",index=0,values=pro_record2)

    recordsFood_df.index = recordsFood_df.index + 1
    recordsFood_df = recordsFood_df.reindex(np.arange(len(recordsFood_df)+1))
    recordsFood_df.loc[0] = record_total

    recordsFood_df.to_csv("PastRecords.csv", index = False)

def plotGraphs():
    import pandas as pd
    import seaborn as sns
    import matplotlib.pyplot as plt

    title = 'Total Amount (g)'

    df1 = pd.read_csv("PastRecords.csv")
    df1["Date"] = pd.to_datetime(df1["Date"], dayfirst=True)
    df1 = df1.drop(["Calories"], axis=1)
    df = df1.melt('Date', var_name='Nutrient Type', value_name='Total Amount Consumed (g)')
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)

    g = sns.scatterplot(x="Date", y='Total Amount Consumed (g)', hue='Nutrient Type', data=df)
    g2 = sns.lineplot(x="Date", y='Total Amount Consumed (g)', hue='Nutrient Type', data=df, legend=False)

    plt.show()

# Main Application ####
if __name__ == '__main__':
    # Root
    width = 1920
    height = 1080
    style = Style(theme='cyclingtheme', themes_file='CyclingApp_theme.json')
    root = style.master
    root.title("Diet App")
    root.state('zoomed')
    # root.iconbitmap('icon location')
    root.geometry(str(width)+"x"+str(height))
    root.pack_propagate(False)

    # Tabs
    my_notebook = ttk.Notebook(root)
    my_notebook.pack(pady = 5)

    foodFrame = ttk.Frame(my_notebook, width = width*.99, height = height*.95)
    foodFrame.pack(fill = "both", expand = 1)
    cyclingFrame = ttk.Frame(my_notebook, width = width*.99, height = height*.95)
    cyclingFrame.pack(fill = "both", expand = 1)

    my_notebook.add(foodFrame, text = "Food")
    my_notebook.add(cyclingFrame, text = "Cycling Stats")

    # Food History
    pastFoodFrame = ttk.LabelFrame(foodFrame, text = "Food Database")
    pastFoodFrame.place(height = height/3, width = width/2.03, rely = 0.095)
    pastFoodTV = ttk.Treeview(pastFoodFrame)
    pastFoodTV.place(relheight = 1, relwidth = 1)

    pastFoodScroll_y = ttk.Scrollbar(pastFoodFrame, orient = "vertical", command = pastFoodTV.yview)
    pastFoodTV.configure(yscrollcommand = pastFoodScroll_y.set)
    pastFoodTV.bind('<ButtonRelease-1>', selectItem)
    pastFoodScroll_y.pack(side = "right", fill = "y")

    # Today's Food
    todayFoodFrame = ttk.LabelFrame(foodFrame, text = "Eaten Today")
    todayFoodFrame.place(height = height/2.752, width = width/2.03, relx = 0.501, rely = 0.062)
    todayFoodTV = ttk.Treeview(todayFoodFrame)
    todayFoodTV.place(relheight = 1, relwidth = 1)

    todayFoodScroll_y = ttk.Scrollbar(todayFoodFrame, orient="vertical", command=todayFoodTV.yview)
    todayFoodTV.configure(yscrollcommand=todayFoodScroll_y.set)
    todayFoodScroll_y.pack(side="right", fill="y")

    # Repo Add
    inputRepoFrame = ttk.LabelFrame(foodFrame, text = "New item")
    inputRepoFrame.place(height=height / 12, width=width / 2.03, relx=0, rely=0)
    inputRepoFrameTV = ttk.Treeview(inputRepoFrame)
    inputRepoFrameTV.place(relheight=0.5, relwidth=1)

    # RepoInputs
    itemInput = ttk.Entry(inputRepoFrame)
    itemInput.place(relheight=0.45, relwidth=1 / 7, rely=.5, relx=0.0025)
    calInput = ttk.Entry(inputRepoFrame)
    calInput.place(relheight=0.45, relwidth=1 / 10.7, rely=.5, relx=1/7+0.0075)
    proInput = ttk.Entry(inputRepoFrame)
    proInput.place(relheight=0.45, relwidth=1 / 11, rely=.5, relx=0.249)
    sfInput = ttk.Entry(inputRepoFrame)
    sfInput.place(relheight=0.45, relwidth=1 / 6.65, rely=.5, relx=0.345)
    usfInput = ttk.Entry(inputRepoFrame)
    usfInput.place(relheight=0.45, relwidth=1 / 6.6, rely=.5, relx=0.501)
    carInput = ttk.Entry(inputRepoFrame)
    carInput.place(relheight=0.45, relwidth=1 / 6.8, rely=.5, relx=0.658)
    sugInput = ttk.Entry(inputRepoFrame)
    sugInput.place(relheight=0.45, relwidth=1 / 10.5, rely=.5, relx=0.8095)
    fibInput = ttk.Entry(inputRepoFrame)
    fibInput.place(relheight=0.45, relwidth=1 / 11.5, rely=.5, relx=0.9085)

    # Buttons
    buttonFrame = ttk.LabelFrame(foodFrame)
    buttonFrame.place(height=height / 19, width=width / 2.03, relx=0.501, rely=0)

    testButton = ttk.Button(buttonFrame, text = "Add new item", command = lambda:add_pastfood(), style = 'secondary.Outline.TButton')
    testButton.place(relx=0.0035, rely=0.0)
    testButton.config(width = 20)

    newDayButton = ttk.Button(buttonFrame, text = "New day", command = lambda:newDay(), style = 'warning.Outline.TButton')
    newDayButton.place(relx=0.82, rely=0)
    newDayButton.config(width = 20)

    # Totals
    todaySummary = ttk.LabelFrame(foodFrame, text = "Today's summary")
    todaySummary.place(height=height / 10.5, width=width / 2.03, relx=0.501, rely=0.47)

    my_notebook2 = ttk.Notebook(todaySummary)
    my_notebook2.pack()

    totalsFrame = Frame(my_notebook2, width=width * .99, height=height * .95)
    totalsFrame.pack(fill="both", expand=1)

    my_notebook2.add(totalsFrame, text = "Totals")
    totalsFrameTV = ttk.Treeview(totalsFrame)
    totalsFrameTV.place(relheight=1, relwidth=1)

    propFrame = Frame(my_notebook2, width=width * .99, height=height * .95)
    propFrame.pack(fill="both", expand=1)

    my_notebook2.add(propFrame, text = "Allowance Proportions")
    propFrameTV = ttk.Treeview(propFrame)
    propFrameTV.place(relheight=1, relwidth=1)

    # Past Totals
    pastTotalsFrame = ttk.LabelFrame(foodFrame, text = "Past Records")
    pastTotalsFrame.place(height=height / 2.65, width=width / 2.03, relx=0.501, rely=0.58)

    my_notebook3 = ttk.Notebook(pastTotalsFrame)
    my_notebook3.pack(fill="both", expand=1)

    pastTotalsTab = Frame(my_notebook3, width=width * .99, height=height * .95)
    my_notebook3.add(pastTotalsTab, text = "Totals")

    pastTotalsFrameTV = ttk.Treeview(pastTotalsTab)
    pastTotalsFrameTV.place(relheight=1, relwidth=1)

    pastTotalsFrame_y = ttk.Scrollbar(pastTotalsTab, orient="vertical", command=pastTotalsFrameTV.yview)
    pastTotalsFrameTV.configure(yscrollcommand=pastTotalsFrame_y.set)
    pastTotalsFrame_y.pack(side="right", fill="y")

    pastPropFrame = Frame(my_notebook3, width=width * .99, height=height * .95)
    my_notebook3.add(pastPropFrame, text = "Allowance Proportions")

    pastPropFrameTV = ttk.Treeview(pastPropFrame)
    pastPropFrameTV.place(relheight=1, relwidth=1)

    pastPropFrame_y = ttk.Scrollbar(pastPropFrame, orient="vertical", command=pastPropFrameTV.yview)
    pastPropFrameTV.configure(yscrollcommand=pastPropFrame_y.set)
    pastPropFrame_y.pack(side="right", fill="y")

    # Progress Graphs
    GraphsFrame = ttk.LabelFrame(foodFrame, text = "Progress Graphs")
    GraphsFrame.place(height=height / 2.098, width=width / 2.03, relx=0, rely=0.47)

    my_notebook4 = ttk.Notebook(GraphsFrame)
    my_notebook4.pack(fill="both", expand=1)

    TotalsPlotTab = Frame(my_notebook4, width=width * .99, height=height * .95)
    my_notebook4.add(TotalsPlotTab, text="Totals Plot")

    propsPlotTab = Frame(my_notebook4, width=width * .99, height=height * .95)
    my_notebook4.add(propsPlotTab, text="Proportions Plot")

    get_pastfood()
    getTodayFood()
    makeRepoInputHeaders()
    makeTotalsHeaders()
    getRecords()
    plotGraphs()
    root.mainloop()

atexit.register(endFunction)