import tkinter as tk
import customtkinter as ctk
from PIL import ImageTk, Image
import os
from tkinter import filedialog
from tkinter import messagebox
import csv
import pandas as pd
from tabulate import tabulate
import sys
import matplotlib.pyplot as plt


script_directory = os.path.dirname(__file__)

root = ctk.CTk()

root.geometry('800x700')
root.title("Pandas")
root.configure(fg_color = "#381B1D")
root.iconbitmap(script_directory + "\\Pandas.ico")
root.resizable(False,False)

def DelNewItems():
    NewItems = ['Frame_New', 'Frame_New1', 'Frame_New2', 'Frame_New3', 'Frame_New4', 'Frame_New5', 'Frame_New6', 'Nbtn1', 'Nbtn2', 'Nbtn3', 'Nbtn4', 'Nbtn5', 'Nbtn6']
    for item_name in NewItems:
        if item_name in globals():
            item = globals()[item_name]
            if hasattr(item, 'destroy'):
                item.destroy()

def Save():
    T_DataFrame = TextBox1.get("1.0", "end-1c").strip()
    Rows = T_DataFrame.split('\n')
    character = "-"
    filtered_Rows = [item for item in Rows if character not in item]
    DataFrame = [Row.split('|') for Row in filtered_Rows]
    NewDataFrame = []

    # Convert integers to numeric type
    for row in DataFrame:
        del row[0]
        del row[-1]
        new_row = []
        for item in row:
            try:
                new_row.append(int(item))
            except ValueError:
                new_row.append(item)  # Keep as string if not convertible to int
        NewDataFrame.append(new_row)

    csv_file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])

    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(NewDataFrame)

def clear_all():

     TextBox1.configure(state="normal")
     TextBox1.delete(1.0,tk.END)

def Upload():
    
    global df
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    filename = os.path.basename(file_path)
    df = pd.read_csv(file_path, index_col=0)
    if df.index.is_numeric():
        df.reset_index(drop=True, inplace=True)
    else :
        df = pd.read_csv(file_path)
    data = tabulate(df, headers='keys', tablefmt='github')  
    TextBox1.configure(state="normal")
    TextBox1.delete(1.0, tk.END) 
    TextBox1.insert(tk.END, data)  
    TextBox1.configure(state="disabled")
    
    FileFrame = ctk.CTkFrame(Frame1,width=80,height=30,  corner_radius=10,fg_color='#BAA099',bg_color="#BAA099")
    FileFrame.place(relx=0.88 ,rely=0.365)
    FileLabel = ctk.CTkLabel(FileFrame, text=filename,corner_radius=10, text_color="#381B1D",fg_color='#BAA099')
    FileLabel.place(relx=0.06,rely=0.08)

def Go_to():

    global df,Frame_New,ButtonTick
    Upload()

    def on_enter_press(event):
        ButtonTick.invoke()
    root.bind('<Return>' , on_enter_press)

    TextBox2.delete(1.0,tk.END)
    TextBox2.insert(tk.END, "Enter the Index / Indexes using commas : ")

    def ticked():
        text = TextBox2.get("1.0", tk.END)
        part_to_remove = "Enter the Index / Indexes using commas :"
        Indexes = text.replace(part_to_remove, "").strip().split(",")
        TextBox2.delete(1.0,tk.END)
        for i in Indexes :
            try:
               i = str(i)
               TextBox2.insert(tk.END, "- - - Index " + i + " - - -")
               i = int(i)
               TextBox2.insert(tk.END, '\n')
               TextBox2.insert(tk.END, df.loc[i])
               TextBox2.insert(tk.END, '\n' + '\n')
            except ValueError:
                TextBox2.insert(tk.END, '\n' + "Please Check Your Index")
            except KeyError:
                TextBox2.insert(tk.END, '\n' + "Cannot Find the Row")
    
    Frame_New = ctk.CTkFrame(Frame1, width=60 ,height=48 , corner_radius=10,border_width=2 ,border_color="white", bg_color="#946B60", fg_color="#BAA099")
    Frame_New.place(relx=0.9, rely=0.445)
    imgtick_path = os.path.join(script_directory+ "\\Button Icons\\Tick.png")
    btnTick_icon = tk.PhotoImage(file = imgtick_path)
    ButtonTick = ctk.CTkButton(Frame_New, image= btnTick_icon,text="", width=30 ,height=30 ,corner_radius=10,fg_color="transparent",bg_color="#BAA099",hover_color="#79452E" ,command = ticked )
    ButtonTick.place(relx=0.05,rely=0.1)

def Quick_Filter():
    
    global df,Frame_New,ButtonTick,Frame_New1, Nbtn1,Frame_New2, Nbtn2,Frame_New3, Nbtn3,Frame_New4, Nbtn4,Frame_New5, Nbtn5,Frame_New6, Nbtn6
    Upload()
    DelNewItems()
  
    global Destroy_Filter_Buttons
    def Destroy_Filter_Buttons():
             Frame_New1.destroy()
             Frame_New2.destroy()
             Frame_New3.destroy()
             Frame_New4.destroy()
             Frame_New5.destroy()
             Frame_New6.destroy()
    
    def F_five_Rows():
        df1 = df.head(6)
        data1 = tabulate(df1, headers='keys', tablefmt='github')
        TextBox2.delete(1.0,tk.END)
        TextBox2.insert(tk.END, data1)
 
    def L_five_Rows():
        df2 = df.tail(6)
        data2 = tabulate(df2, headers='keys', tablefmt='github')
        TextBox2.delete(1.0,tk.END)
        TextBox2.insert(tk.END, data2)

    def Rows_F_H():

        global Frame_New,ButtonTick
        
        TextBox2.delete(1.0,tk.END)
        TextBox2.insert(tk.END, "How many rows do you want to display from head : ")

        def on_enter_press(event):
            ButtonTick.invoke()
        root.bind('<Return>' , on_enter_press)

        def ticked():

              try:    
                  N1 = TextBox2.get("1.0", tk.END)
                  part_to_remove = "How many rows do you want to display from head : "
                  N1_h = N1.replace(part_to_remove, "").strip()
                  n1 = int(N1_h) 
                  df3 = df.head(n1)
                  data3 = tabulate(df3, headers='keys', tablefmt='github')
                  TextBox2.delete(1.0,tk.END)
                  TextBox2.insert(tk.END, data3)
              except:
                  TextBox2.insert(tk.END, '\n')
                  TextBox2.insert(tk.END, "Please Enter a Valid Index")

        Frame_New = ctk.CTkFrame(Frame1, width=60 ,height=48 , corner_radius=10,border_width=2 ,border_color="white", bg_color="#946B60", fg_color="#BAA099")
        Frame_New.place(relx=0.9, rely=0.445)
        imgtick_path = os.path.join(script_directory+ "\\Button Icons\\Tick.png")
        btnTick_icon = tk.PhotoImage(file = imgtick_path)
        ButtonTick = ctk.CTkButton(Frame_New, image= btnTick_icon,text="", width=30 ,height=30 ,corner_radius=10,fg_color="transparent",bg_color="#BAA099",hover_color="#79452E" ,command = ticked )
        ButtonTick.place(relx=0.05,rely=0.1)
   
    def Rows_F_T():

        global Frame_New,ButtonTick
        TextBox2.delete(1.0,tk.END)
        TextBox2.insert(tk.END, "How many rows do you want to display from tail : ")

        def on_enter_press(event):
            ButtonTick.invoke()
        root.bind('<Return>' , on_enter_press)

        def ticked():
                  
                try:
                  N2 = TextBox2.get("1.0", tk.END)
                  part_to_remove = "How many rows do you want to display from tail :"
                  N2_t = N2.replace(part_to_remove, "").strip()
                  n2 = int(N2_t) 
                  df4 = df.tail(n2)
                  data4 = tabulate(df4, headers='keys', tablefmt='github')
                  TextBox2.delete(1.0,tk.END)
                  TextBox2.insert(tk.END, data4)
                except:
                  TextBox2.insert(tk.END, '\n')
                  TextBox2.insert(tk.END, "Please Enter a Valid Index")

        Frame_New = ctk.CTkFrame(Frame1, width=60 ,height=48 , corner_radius=10,border_width=2 ,border_color="white", bg_color="#946B60", fg_color="#BAA099")
        Frame_New.place(relx=0.9, rely=0.445)
        imgtick_path = os.path.join(script_directory+ "\\Button Icons\\Tick.png")
        btnTick_icon = tk.PhotoImage(file = imgtick_path)
        ButtonTick = ctk.CTkButton(Frame_New, image= btnTick_icon,text="", width=30 ,height=30 ,corner_radius=10,fg_color="transparent",bg_color="#BAA099",hover_color="#79452E" ,command = ticked )
        ButtonTick.place(relx=0.05,rely=0.1)


    Frame_New1 = ctk.CTkFrame(Frame1 , corner_radius=10,border_width=2 ,border_color="white", bg_color="#946B60", fg_color="#BAA099")
    Frame_New1.place(relx=0.02, rely=0.57)
    Nbtn1 = ctk.CTkButton(Frame_New1,text="Specific Rows",text_color="black", width=30 ,height=30 ,corner_radius=10,bg_color="#946B60",fg_color="#BAA099",hover_color="#79452E", command=Go_to)
    Nbtn1.pack()

    Frame_New2 = ctk.CTkFrame(Frame1 , corner_radius=10,border_width=2 ,border_color="white", bg_color="#946B60", fg_color="#BAA099")
    Frame_New2.place(relx=0.16, rely=0.57)
    Nbtn2 = ctk.CTkButton(Frame_New2,text="First 5 Rows",text_color="black", width=30 ,height=30 ,corner_radius=10,bg_color="#946B60",fg_color="#BAA099",hover_color="#79452E", command=F_five_Rows)
    Nbtn2.pack()

    Frame_New3 = ctk.CTkFrame(Frame1 , corner_radius=10,border_width=2 ,border_color="white", bg_color="#946B60", fg_color="#BAA099")
    Frame_New3.place(relx=0.285, rely=0.57)
    Nbtn3 = ctk.CTkButton(Frame_New3,text="Last 5 Rows",text_color="black", width=30 ,height=30 ,corner_radius=10,bg_color="#946B60",fg_color="#BAA099",hover_color="#79452E" ,command=L_five_Rows)
    Nbtn3.pack()

    Frame_New4 = ctk.CTkFrame(Frame1 , corner_radius=10,border_width=2 ,border_color="white", bg_color="#946B60", fg_color="#BAA099")
    Frame_New4.place(relx=0.411, rely=0.57)
    Nbtn4 = ctk.CTkButton(Frame_New4,text="Rows from Head",text_color="black", width=30 ,height=30 ,corner_radius=10,bg_color="#946B60",fg_color="#BAA099",hover_color="#79452E",command=Rows_F_H)
    Nbtn4.pack()

    Frame_New5 = ctk.CTkFrame(Frame1 , corner_radius=10,border_width=2 ,border_color="white", bg_color="#946B60", fg_color="#BAA099")
    Frame_New5.place(relx=0.568, rely=0.57)
    Nbtn5 = ctk.CTkButton(Frame_New5,text="Rows from Tail",text_color="black", width=30 ,height=30 ,corner_radius=10,bg_color="#946B60",fg_color="#BAA099",hover_color="#79452E", command=Rows_F_T)
    Nbtn5.pack()

    Frame_New6 = ctk.CTkFrame(Frame1 , corner_radius=10,border_width=2 ,border_color="white", bg_color="#946B60", fg_color="#BAA099")
    Frame_New6.place(relx=0.892, rely=0.57)
    Nbtn6 = ctk.CTkButton(Frame_New6,text="Hide All",text_color="black", width=30 ,height=30 ,corner_radius=10,bg_color="#946B60",fg_color="#BAA099",hover_color="#79452E",command=Destroy_Filter_Buttons)
    Nbtn6.pack()

def Remove():
    
    global df,Frame_New1, Nbtn1,Frame_New2, Nbtn2,Frame_New6, Nbtn6
     
    Upload()
    DelNewItems()
    
    def Destroy_Remove_Buttons():
             Frame_New1.destroy()
             Frame_New2.destroy()
             Frame_New6.destroy()
    
      

    def R_Empty():
        new_df = df.dropna()
        data5 = tabulate(new_df, headers='keys', tablefmt='github')
        TextBox1.configure(state="normal")
        TextBox1.delete(1.0,tk.END)
        TextBox1.insert(tk.END, data5) 
        TextBox1.configure(state="disabled")
        TextBox2.delete(1.0,tk.END)
        TextBox2.insert(tk.END, "All Rows with Empty cells were Removed") 
        
    def R_Duplicates():
        new_df = df.drop_duplicates()
        data6 = tabulate(new_df, headers='keys', tablefmt='github')
        TextBox1.configure(state="normal")
        TextBox1.delete(1.0,tk.END)
        TextBox1.insert(tk.END, data6) 
        TextBox1.configure(state="disabled")
        TextBox2.delete(1.0,tk.END)
        TextBox2.insert(tk.END, "All Duplicated Rows were Removed") 
              
    Frame_New1 = ctk.CTkFrame(Frame1 , corner_radius=10,border_width=2 ,border_color="white", bg_color="#946B60", fg_color="#BAA099")
    Frame_New1.place(relx=0.02, rely=0.57)
    Nbtn1 = ctk.CTkButton(Frame_New1,text="Remove rows with Empty cells",text_color="black", width=30 ,height=30 ,corner_radius=10,bg_color="#946B60",fg_color="#BAA099",hover_color="#79452E",command=R_Empty)
    Nbtn1.pack()

    Frame_New2 = ctk.CTkFrame(Frame1 , corner_radius=10,border_width=2 ,border_color="white", bg_color="#946B60", fg_color="#BAA099")
    Frame_New2.place(relx=0.3, rely=0.57)
    Nbtn2 = ctk.CTkButton(Frame_New2,text="Remove all Duplicated rows",text_color="black", width=30 ,height=30 ,corner_radius=10,bg_color="#946B60",fg_color="#BAA099",hover_color="#79452E",command=R_Duplicates)
    Nbtn2.pack()

    Frame_New6 = ctk.CTkFrame(Frame1 , corner_radius=10,border_width=2 ,border_color="white", bg_color="#946B60", fg_color="#BAA099")
    Frame_New6.place(relx=0.892, rely=0.57)
    Nbtn6 = ctk.CTkButton(Frame_New6,text="Hide All",text_color="black", width=30 ,height=30 ,corner_radius=10,bg_color="#946B60",fg_color="#BAA099",hover_color="#79452E",command=Destroy_Remove_Buttons)
    Nbtn6.pack()

def Replace():
    
    global df,Frame_New,ButtonTick,Frame_New1, Nbtn1,Frame_New2, Nbtn2,Frame_New3, Nbtn3,Frame_New4, Nbtn4,Frame_New5, Nbtn5,Frame_New6, Nbtn6
    Upload()
    DelNewItems()
    
    def Destroy_Replace_Buttons():
             Frame_New1.destroy()
             Frame_New2.destroy()
             Frame_New6.destroy()
    
    def Rp_S_V():
        
        global Frame_New,ButtonTick
        TextBox2.delete(1.0,tk.END)
        TextBox2.insert(tk.END, "Enter the Column Name , Index of Row & New Value (ex : Column , Row , Value): ")
        def on_enter_press(event):
            ButtonTick.invoke()
        root.bind('<Return>' , on_enter_press)

        def ticked():

            try:
               text = TextBox2.get("1.0", tk.END)
               part_to_remove = "Enter the Column Name , Index of Row & New Value (ex : Column , Row , Value):"
               Column_Row = text.replace(part_to_remove, "").strip()
               Column_Row_N = Column_Row.strip().split(",")
               N_Column = Column_Row_N[0] 
               N_Row = int(Column_Row_N[1])
               N_Value = Column_Row_N[2]
               df.at[N_Row, N_Column] = N_Value
               TextBox1.configure(state="normal")
               TextBox1.delete(1.0,tk.END)
               data = tabulate(df, headers='keys', tablefmt='github')
               TextBox1.insert(tk.END, data)
               TextBox1.configure(state="disabled")
               TextBox2.insert(tk.END, '\n')
               N_Row = str(Column_Row_N[1])
               TextBox2.insert(tk.END, "Row " + "'"+  N_Row + "'"+ " in Column " +  "'" + N_Column + "'" + " is Replaced with " + "'" + N_Value + "'")
            except:
                TextBox2.insert(tk.END, '\n')
                TextBox2.insert(tk.END, "Please use the correct format")

        Frame_New = ctk.CTkFrame(Frame1, width=60 ,height=48 , corner_radius=10,border_width=2 ,border_color="white", bg_color="#946B60", fg_color="#BAA099")
        Frame_New.place(relx=0.9, rely=0.445)
        imgtick_path = os.path.join(script_directory+ "\\Button Icons\\Tick.png")
        btnTick_icon = tk.PhotoImage(file = imgtick_path)
        ButtonTick = ctk.CTkButton(Frame_New, image= btnTick_icon,text="", width=30 ,height=30 ,corner_radius=10,fg_color="transparent",bg_color="#BAA099",hover_color="#79452E" ,command = ticked )
        ButtonTick.place(relx=0.05,rely=0.1)

    def Rp_E_C():

         Destroy_Replace_Buttons()
         global Frame_New3,Frame_New4,Frame_New5,Nbtn3,Nbtn4,Nbtn5 

         def Destroy_EC_Buttons():
             Frame_New3.destroy()
             Frame_New4.destroy()
             Frame_New5.destroy()
         
         def Rp_E_C_SC():
            
               global Frame_New,ButtonTick
               TextBox2.delete(1.0,tk.END)
               TextBox2.insert(tk.END, "Enter the Column Name and the Value to Replace using commas (ex : Column , Value): ")
               def on_enter_press(event):
                      ButtonTick.invoke()
               root.bind('<Return>' , on_enter_press)

               def ticked():
                    try:
                        text = TextBox2.get("1.0", tk.END)
                        part_to_remove = "Enter the Column Name and the Value to Replace using commas (ex : Column , Value):"
                        Column = text.replace(part_to_remove, "").strip()
                        Column_Value = Column.strip().split(",")
                        N_Column = str(Column_Value[0])
                        N_Value = str(Column_Value[1])
                        df.fillna({ N_Column: N_Value }, inplace=True)
                        TextBox1.configure(state="normal")
                        TextBox1.delete(1.0,tk.END)
                        data = tabulate(df, headers='keys', tablefmt='github')
                        TextBox1.insert(tk.END, data)
                        TextBox1.configure(state="disabled")
                        TextBox2.insert(tk.END, '\n')
                        TextBox2.insert(tk.END, "All Empty cells in " + "'" + N_Column + "'" + " is replaced with "+ "'" + N_Value + "'")
                    except:
                        TextBox2.insert(tk.END, '\n')
                        TextBox2.insert(tk.END, "Please use the correct format")

               Frame_New = ctk.CTkFrame(Frame1, width=60 ,height=48 , corner_radius=10,border_width=2 ,border_color="white", bg_color="#946B60", fg_color="#BAA099")
               Frame_New.place(relx=0.9, rely=0.445)
               imgtick_path = os.path.join(script_directory+ "\\Button Icons\\Tick.png")
               btnTick_icon = tk.PhotoImage(file = imgtick_path)
               ButtonTick = ctk.CTkButton(Frame_New, image= btnTick_icon,text="", width=30 ,height=30 ,corner_radius=10,fg_color="transparent",bg_color="#BAA099",hover_color="#79452E" ,command = ticked )
               ButtonTick.place(relx=0.05,rely=0.1)

         def Rp_A_EC():
               
               global Frame_New,ButtonTick
               TextBox2.delete(1.0,tk.END)
               TextBox2.insert(tk.END, "Enter the value to Replace : ")
               def on_enter_press(event):
                    ButtonTick.invoke()
               root.bind('<Return>' , on_enter_press)

               def ticked():

                  text = TextBox2.get("1.0", tk.END)
                  part_to_remove = "Enter the value to Replace :"
                  Value = text.replace(part_to_remove, "").strip()
                  df.fillna(Value, inplace=True)
                  TextBox1.configure(state="normal")
                  TextBox1.delete(1.0,tk.END)
                  data = tabulate(df, headers='keys', tablefmt='github')
                  TextBox1.insert(tk.END, data)
                  TextBox1.configure(state="disabled")
                  TextBox2.insert(tk.END, '\n')
                  TextBox2.insert(tk.END, "All Empty cells have Replaced with " + "'" + Value + "'")
               
               Frame_New = ctk.CTkFrame(Frame1, width=60 ,height=48 , corner_radius=10,border_width=2 ,border_color="white", bg_color="#946B60", fg_color="#BAA099")
               Frame_New.place(relx=0.9, rely=0.445)
               imgtick_path = os.path.join(script_directory+ "\\Button Icons\\Tick.png")
               btnTick_icon = tk.PhotoImage(file = imgtick_path)
               ButtonTick = ctk.CTkButton(Frame_New, image= btnTick_icon,text="", width=30 ,height=30 ,corner_radius=10,fg_color="transparent",bg_color="#BAA099",hover_color="#79452E" ,command = ticked )
               ButtonTick.place(relx=0.05,rely=0.1)

         Frame_New3 = ctk.CTkFrame(Frame1 , corner_radius=10,border_width=2 ,border_color="white", bg_color="#946B60", fg_color="#BAA099")
         Frame_New3.place(relx=0.02, rely=0.57)
         Nbtn3 = ctk.CTkButton(Frame_New3,text="All Empty cells",text_color="black", width=30 ,height=30 ,corner_radius=10,bg_color="#946B60",fg_color="#BAA099",hover_color="#79452E",command=Rp_A_EC)
         Nbtn3.pack()

         Frame_New4 = ctk.CTkFrame(Frame1 , corner_radius=10,border_width=2 ,border_color="white", bg_color="#946B60", fg_color="#BAA099")
         Frame_New4.place(relx=0.17, rely=0.57)
         Nbtn4 = ctk.CTkButton(Frame_New4,text="Empty cells in specific Column",text_color="black", width=30 ,height=30 ,corner_radius=10,bg_color="#946B60",fg_color="#BAA099",hover_color="#79452E",command=Rp_E_C_SC)
         Nbtn4.pack()

         Frame_New5 = ctk.CTkFrame(Frame1 , corner_radius=10,border_width=2 ,border_color="white", bg_color="#946B60", fg_color="#BAA099")
         Frame_New5.place(relx=0.892, rely=0.57)
         Nbtn5 = ctk.CTkButton(Frame_New5,text="Hide All",text_color="black", width=30 ,height=30 ,corner_radius=10,bg_color="#946B60",fg_color="#BAA099",hover_color="#79452E",command=Destroy_EC_Buttons)
         Nbtn5.pack()

    Frame_New1 = ctk.CTkFrame(Frame1 , corner_radius=10,border_width=2 ,border_color="white", bg_color="#946B60", fg_color="#BAA099")
    Frame_New1.place(relx=0.02, rely=0.57)
    Nbtn1 = ctk.CTkButton(Frame_New1,text="Replace Empty cells",text_color="black", width=30 ,height=30 ,corner_radius=10,bg_color="#946B60",fg_color="#BAA099",hover_color="#79452E",command=Rp_E_C)
    Nbtn1.pack()

    Frame_New2 = ctk.CTkFrame(Frame1 , corner_radius=10,border_width=2 ,border_color="white", bg_color="#946B60", fg_color="#BAA099")
    Frame_New2.place(relx=0.2, rely=0.57)
    Nbtn2 = ctk.CTkButton(Frame_New2,text="Replace / Add Specific Values",text_color="black", width=30 ,height=30 ,corner_radius=10,bg_color="#946B60",fg_color="#BAA099",hover_color="#79452E",command=Rp_S_V)
    Nbtn2.pack()

    Frame_New6 = ctk.CTkFrame(Frame1 , corner_radius=10,border_width=2 ,border_color="white", bg_color="#946B60", fg_color="#BAA099")
    Frame_New6.place(relx=0.892, rely=0.57)
    Nbtn6 = ctk.CTkButton(Frame_New6,text="Hide All",text_color="black", width=30 ,height=30 ,corner_radius=10,bg_color="#946B60",fg_color="#BAA099",hover_color="#79452E",command=Destroy_Replace_Buttons)
    Nbtn6.pack()

def Calculate():
    
    global df,Frame_New,ButtonTick,Frame_New1, Nbtn1,Frame_New2, Nbtn2,Frame_New3, Nbtn3,Frame_New4, Nbtn4,Frame_New5, Nbtn5
    Upload()
    DelNewItems()

    TextBox2.delete(1.0, tk.END) 
    
    def Destroy_Cal_Buttons():
        Frame_New1.destroy()
        Frame_New2.destroy()
        Frame_New3.destroy()
        Frame_New4.destroy()
        Frame_New5.destroy()
    
    def Cal_Sum():

        global Frame_New,ButtonTick
        TextBox2.delete(1.0, tk.END)
        TextBox2.insert(tk.END, "Enter the Column Name : ")
        
        def on_enter_press(event):
            ButtonTick.invoke()
        root.bind('<Return>' , on_enter_press)

        def ticked():
                text = TextBox2.get("1.0", tk.END)        
                part_to_remove = "Enter the Column Name :"
                Column_ = text.replace(part_to_remove, "").strip()
                try:
                    mode_ = df[Column_].sum()
                    TextBox2.insert(tk.END, '\n')
                    TextBox2.insert(tk.END, mode_)
                except:
                    TextBox2.insert(tk.END, '\n')
                    TextBox2.insert(tk.END, "Cannot calculate Sum of ' " + Column_ + " '")
 
        Frame_New = ctk.CTkFrame(Frame1, width=60 ,height=48 , corner_radius=10,border_width=2 ,border_color="white", bg_color="#946B60", fg_color="#BAA099")
        Frame_New.place(relx=0.9, rely=0.445)
        imgtick_path = os.path.join(script_directory+ "\\Button Icons\\Tick.png")
        btnTick_icon = tk.PhotoImage(file = imgtick_path)
        ButtonTick = ctk.CTkButton(Frame_New, image= btnTick_icon,text="", width=30 ,height=30 ,corner_radius=10,fg_color="transparent",bg_color="#BAA099",hover_color="#79452E" ,command = ticked )
        ButtonTick.place(relx=0.05,rely=0.1)

    def Cal_Mean():

        global Frame_New,ButtonTick
        TextBox2.delete(1.0, tk.END)
        TextBox2.insert(tk.END, "Enter the Column Name : ")

        def on_enter_press(event):
            ButtonTick.invoke()
        root.bind('<Return>' , on_enter_press)

        def ticked():
                text = TextBox2.get("1.0", tk.END)        
                part_to_remove = "Enter the Column Name :"
                Column_ = text.replace(part_to_remove, "").strip()
                try:
                    mode_ = df[Column_].mean()
                    TextBox2.insert(tk.END, '\n')
                    TextBox2.insert(tk.END, mode_)
                except:
                    TextBox2.insert(tk.END, '\n')
                    TextBox2.insert(tk.END, "Cannot calculate Mean of ' " + Column_ + " '")

        Frame_New = ctk.CTkFrame(Frame1, width=60 ,height=48 , corner_radius=10,border_width=2 ,border_color="white", bg_color="#946B60", fg_color="#BAA099")
        Frame_New.place(relx=0.9, rely=0.445)
        imgtick_path = os.path.join(script_directory+ "\\Button Icons\\Tick.png")
        btnTick_icon = tk.PhotoImage(file = imgtick_path)
        ButtonTick = ctk.CTkButton(Frame_New, image= btnTick_icon,text="", width=30 ,height=30 ,corner_radius=10,fg_color="transparent",bg_color="#BAA099",hover_color="#79452E" ,command = ticked )
        ButtonTick.place(relx=0.05,rely=0.1)

    def Cal_Median():

        global Frame_New,ButtonTick
        TextBox2.delete(1.0, tk.END)
        TextBox2.insert(tk.END, "Enter the Column Name : ")
        
        def on_enter_press(event):
            ButtonTick.invoke()
        root.bind('<Return>' , on_enter_press)

        def ticked():
                text = TextBox2.get("1.0", tk.END)        
                part_to_remove = "Enter the Column Name :"
                Column_ = text.replace(part_to_remove, "").strip()
                try:
                    mode_ = df[Column_].median()
                    TextBox2.insert(tk.END, '\n')
                    TextBox2.insert(tk.END, mode_)
                except:
                    TextBox2.insert(tk.END, '\n')
                    TextBox2.insert(tk.END, "Cannot calculate Median of ' " + Column_ + " '")

        Frame_New = ctk.CTkFrame(Frame1, width=60 ,height=48 , corner_radius=10,border_width=2 ,border_color="white", bg_color="#946B60", fg_color="#BAA099")
        Frame_New.place(relx=0.9, rely=0.445)
        imgtick_path = os.path.join(script_directory+ "\\Button Icons\\Tick.png")
        btnTick_icon = tk.PhotoImage(file = imgtick_path)
        ButtonTick = ctk.CTkButton(Frame_New, image= btnTick_icon,text="", width=30 ,height=30 ,corner_radius=10,fg_color="transparent",bg_color="#BAA099",hover_color="#79452E" ,command = ticked )
        ButtonTick.place(relx=0.05,rely=0.1)

    def Cal_Mode():

        global Frame_New,ButtonTick
        TextBox2.delete(1.0, tk.END)
        TextBox2.insert(tk.END, "Enter the Column Name : ")

        def on_enter_press(event):
            ButtonTick.invoke()
        root.bind('<Return>' , on_enter_press)

        def ticked():
                text = TextBox2.get("1.0", tk.END)        
                part_to_remove = "Enter the Column Name :"
                Column_ = text.replace(part_to_remove, "").strip()
                try:
                    mode_ = df[Column_].mode()[0]
                    TextBox2.insert(tk.END, '\n')
                    TextBox2.insert(tk.END, mode_)
                except:
                    TextBox2.insert(tk.END, '\n')
                    TextBox2.insert(tk.END, "Cannot calculate Mode of ' " + Column_ + " '")

        Frame_New = ctk.CTkFrame(Frame1, width=60 ,height=48 , corner_radius=10,border_width=2 ,border_color="white", bg_color="#946B60", fg_color="#BAA099")
        Frame_New.place(relx=0.9, rely=0.445)
        imgtick_path = os.path.join(script_directory+ "\\Button Icons\\Tick.png")
        btnTick_icon = tk.PhotoImage(file = imgtick_path)
        ButtonTick = ctk.CTkButton(Frame_New, image= btnTick_icon,text="", width=30 ,height=30 ,corner_radius=10,fg_color="transparent",bg_color="#BAA099",hover_color="#79452E" ,command = ticked )
        ButtonTick.place(relx=0.05,rely=0.1)
        
    Frame_New1 = ctk.CTkFrame(Frame1 , corner_radius=10,border_width=2 ,border_color="white", bg_color="#946B60", fg_color="#BAA099")
    Frame_New1.place(relx=0.02, rely=0.57)
    Nbtn1 = ctk.CTkButton(Frame_New1,text="Sum",text_color="black", width=30 ,height=30 ,corner_radius=10,bg_color="#946B60",fg_color="#BAA099",hover_color="#79452E",command=Cal_Sum)
    Nbtn1.pack()

    Frame_New2 = ctk.CTkFrame(Frame1 , corner_radius=10,border_width=2 ,border_color="white", bg_color="#946B60", fg_color="#BAA099")
    Frame_New2.place(relx=0.1, rely=0.57)
    Nbtn2 = ctk.CTkButton(Frame_New2,text="Mean",text_color="black", width=30 ,height=30 ,corner_radius=10,bg_color="#946B60",fg_color="#BAA099",hover_color="#79452E",command=Cal_Mean)
    Nbtn2.pack()

    Frame_New3 = ctk.CTkFrame(Frame1 , corner_radius=10,border_width=2 ,border_color="white", bg_color="#946B60", fg_color="#BAA099")
    Frame_New3.place(relx=0.19, rely=0.57)
    Nbtn3 = ctk.CTkButton(Frame_New3,text="Median",text_color="black", width=30 ,height=30 ,corner_radius=10,bg_color="#946B60",fg_color="#BAA099",hover_color="#79452E",command=Cal_Median)
    Nbtn3.pack()

    Frame_New4 = ctk.CTkFrame(Frame1 , corner_radius=10,border_width=2 ,border_color="white", bg_color="#946B60", fg_color="#BAA099")
    Frame_New4.place(relx=0.29, rely=0.57)
    Nbtn4 = ctk.CTkButton(Frame_New4,text="Mode",text_color="black", width=30 ,height=30 ,corner_radius=10,bg_color="#946B60",fg_color="#BAA099",hover_color="#79452E",command=Cal_Mode)
    Nbtn4.pack()

    Frame_New5 = ctk.CTkFrame(Frame1 , corner_radius=10,border_width=2 ,border_color="white", bg_color="#946B60", fg_color="#BAA099")
    Frame_New5.place(relx=0.892, rely=0.57)
    Nbtn5 = ctk.CTkButton(Frame_New5,text="Hide All",text_color="black", width=30 ,height=30 ,corner_radius=10,bg_color="#946B60",fg_color="#BAA099",hover_color="#79452E",command=Destroy_Cal_Buttons)
    Nbtn5.pack()

def Correlation():
    
    global df ,Frame_New1 ,Frame_New2 ,ButtonQuestion, ButtonVisual
    Upload()
    DelNewItems()
     # Convert non-numeric columns to numeric, setting errors='coerce' to handle non-numeric values
    df = df.apply(pd.to_numeric, errors='coerce')
    
    # Calculate correlation matrix
    N_df = df.corr()
    # Convert correlation matrix to string
    correlation_str = N_df.to_string()
    
    TextBox2.delete(1.0, tk.END)
    TextBox2.insert(tk.END, correlation_str)
    
    def Help():
        messagebox.showinfo("What is Correlation ?" , "In Pandas, correlation values are invaluable metrics for users seeking to understand the relationships between variables within their datasets. The correlation coefficient, ranging from -1 to 1, offers a quantitative measure of the strength and direction of linear associations between numerical variables. A coefficient close to 1 signifies a strong positive correlation, indicating that as one variable increases, the other tends to increase as well. Conversely, a coefficient near -1 suggests a strong negative correlation, where one variable typically decreases as the other increases. A correlation coefficient close to 0 indicates little to no linear relationship between the variables. By interpreting these correlation values, users can uncover patterns, dependencies, and potential insights within their data, facilitating informed decision-making and deeper exploratory analysis.")

    def Visualize():

        plt.figure(figsize=(8, 6))
        for column in N_df.columns:
            plt.plot(N_df.index, N_df[column], marker='o', label=column)

        plt.title('Correlation Coefficients')
        plt.xlabel('Variable')
        plt.ylabel('Correlation Coefficient')
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    Frame_New1 = ctk.CTkFrame(Frame1, width=60 ,height=48 , corner_radius=10,border_width=2 ,border_color="white", bg_color="#946B60", fg_color="#BAA099")
    Frame_New1.place(relx=0.9, rely=0.445)
    imgQuestion_path = os.path.join(script_directory+ "\\Button Icons\\Question.png")
    btnQuestion_icon = tk.PhotoImage(file = imgQuestion_path)
    ButtonQuestion = ctk.CTkButton(Frame_New1, image= btnQuestion_icon,text="", width=30 ,height=30 ,corner_radius=10,fg_color="transparent",bg_color="#BAA099",hover_color="#79452E" ,command = Help )
    ButtonQuestion.place(relx=0.05,rely=0.1)

    Frame_New2 = ctk.CTkFrame(Frame1, width=60 ,height=48 , corner_radius=10,border_width=2 ,border_color="white", bg_color="#946B60", fg_color="#BAA099")
    Frame_New2.place(relx=0.815, rely=0.445)
    imgVisual_path = os.path.join(script_directory+ "\\Button Icons\\Visual.png")
    btnVisual_icon = tk.PhotoImage(file = imgVisual_path)
    ButtonVisual = ctk.CTkButton(Frame_New2, image= btnVisual_icon,text="", width=30 ,height=30 ,corner_radius=10,fg_color="transparent",bg_color="#BAA099",hover_color="#79452E" ,command = Visualize )
    ButtonVisual.place(relx=0.05,rely=0.1)

def Set():

    global df,Frame_New,ButtonTick,Frame_New1, Nbtn1,Frame_New2, Nbtn2,Frame_New3, Nbtn3
    Upload()
    DelNewItems()
    
    def Destroy_Set_Buttons():
        Frame_New1.destroy()
        Frame_New2.destroy()
        Frame_New3.destroy()

    def Set_Max():

        global Frame_New,ButtonTick
        TextBox2.delete(1.0, tk.END)
        TextBox2.insert(tk.END, "Enter the Column Name and maximum value using commas(ex: Column, Value) : ")

        def on_enter_press(event):
            ButtonTick.invoke()
        root.bind('<Return>' , on_enter_press)

        def ticked():
            try:
                text = TextBox2.get("1.0", tk.END)
                part_to_remove = "Enter the Column Name and maximum value using commas(ex: Column, Value) :"
                Column_ = text.replace(part_to_remove, "").strip()
                Column_Value = Column_.strip().split(",")
                N_Column = Column_Value[0]
                N_Value = int(Column_Value[1])
                for  idx, value in df[N_Column].items():
                    if value > N_Value:
                      df.loc[idx, N_Column] = N_Value
                      TextBox1.configure(state="normal")
                      TextBox1.delete(1.0, tk.END)
                      data = tabulate(df, headers='keys', tablefmt='github')
                      TextBox1.insert(tk.END, data)
                      TextBox1.configure(state="disabled")
                TextBox2.insert(tk.END,"\n")
                TextBox2.insert(tk.END, "DONE")
            except:
                TextBox2.insert(tk.END,"\n")
                TextBox2.insert(tk.END, "Cannot do It !!!")
               
        Frame_New = ctk.CTkFrame(Frame1, width=60 ,height=48 , corner_radius=10,border_width=2 ,border_color="white", bg_color="#946B60", fg_color="#BAA099")
        Frame_New.place(relx=0.9, rely=0.445)
        imgtick_path = os.path.join(script_directory+ "\\Button Icons\\Tick.png")
        btnTick_icon = tk.PhotoImage(file = imgtick_path)
        ButtonTick = ctk.CTkButton(Frame_New, image= btnTick_icon,text="", width=30 ,height=30 ,corner_radius=10,fg_color="transparent",bg_color="#BAA099",hover_color="#79452E" ,command = ticked )
        ButtonTick.place(relx=0.05,rely=0.1)

    def Set_Min():

        global Frame_New,ButtonTick
        TextBox2.delete(1.0, tk.END)
        TextBox2.insert(tk.END, "Enter the Column Name and minimum value using commas(ex: Column, Value) : ")

        def on_enter_press(event):
            ButtonTick.invoke()
        root.bind('<Return>' , on_enter_press)

        def ticked():
            try:
                text = TextBox2.get("1.0", tk.END)
                part_to_remove = "Enter the Column Name and minimum value using commas(ex: Column, Value) :"
                Column_ = text.replace(part_to_remove, "").strip()
                Column_Value = Column_.strip().split(",")
                N_Column = Column_Value[0]
                N_Value = int(Column_Value[1])
                for  idx, value in df[N_Column].items():
                    if value < N_Value:
                      df.loc[idx, N_Column] = N_Value
                      TextBox1.configure(state="normal")
                      TextBox1.delete(1.0, tk.END)
                      data = tabulate(df, headers='keys', tablefmt='github')
                      TextBox1.insert(tk.END, data)
                      TextBox1.configure(state="disabled")
                TextBox2.insert(tk.END,"\n")
                TextBox2.insert(tk.END, "DONE")
            except:
                TextBox2.insert(tk.END,"\n")
                TextBox2.insert(tk.END, "Cannot do It !!!")
               
        Frame_New = ctk.CTkFrame(Frame1, width=60 ,height=48 , corner_radius=10,border_width=2 ,border_color="white", bg_color="#946B60", fg_color="#BAA099")
        Frame_New.place(relx=0.9, rely=0.445)
        imgtick_path = os.path.join(script_directory+ "\\Button Icons\\Tick.png")
        btnTick_icon = tk.PhotoImage(file = imgtick_path)
        ButtonTick = ctk.CTkButton(Frame_New, image= btnTick_icon,text="", width=30 ,height=30 ,corner_radius=10,fg_color="transparent",bg_color="#BAA099",hover_color="#79452E" ,command = ticked )
        ButtonTick.place(relx=0.05,rely=0.1)

    Frame_New1 = ctk.CTkFrame(Frame1 , corner_radius=10,border_width=2 ,border_color="white", bg_color="#946B60", fg_color="#BAA099")
    Frame_New1.place(relx=0.02, rely=0.57)
    Nbtn1 = ctk.CTkButton(Frame_New1,text="Maximum Value",text_color="black", width=30 ,height=30 ,corner_radius=10,bg_color="#946B60",fg_color="#BAA099",hover_color="#79452E",command=Set_Max)
    Nbtn1.pack()

    Frame_New2 = ctk.CTkFrame(Frame1 , corner_radius=10,border_width=2 ,border_color="white", bg_color="#946B60", fg_color="#BAA099")
    Frame_New2.place(relx=0.18, rely=0.57)
    Nbtn2 = ctk.CTkButton(Frame_New2,text="Minimum Value",text_color="black", width=30 ,height=30 ,corner_radius=10,bg_color="#946B60",fg_color="#BAA099",hover_color="#79452E",command=Set_Min)
    Nbtn2.pack()

    Frame_New3 = ctk.CTkFrame(Frame1 , corner_radius=10,border_width=2 ,border_color="white", bg_color="#946B60", fg_color="#BAA099")
    Frame_New3.place(relx=0.892, rely=0.57)
    Nbtn5 = ctk.CTkButton(Frame_New3,text="Hide All",text_color="black", width=30 ,height=30 ,corner_radius=10,bg_color="#946B60",fg_color="#BAA099",hover_color="#79452E",command=Destroy_Set_Buttons)
    Nbtn5.pack()

def Create():
    def create_dataframe():
      try:
        
        columns = column_entry.get().split(",")
        data = data_text.get("1.0", tk.END).strip()
        data_rows = data.split("\n")
 
        df = pd.DataFrame([row.split(",") for row in data_rows], columns=columns)
        TextBox1.configure(state="normal")
        
        data = tabulate(df, headers='keys', tablefmt='github')  # Format DataFrame using tabulate
        TextBox1.delete(1.0, tk.END)  # Clear the text box
        TextBox1.insert(tk.END, data)  # Insert CSV data into the text box
        TextBox1.configure(state="disabled")

      except :
        data_text.delete(1.0, tk.END)
        data_text.insert(tk.END, "Please check again your data")

    # Create Tkinter window
    root1 = ctk.CTk()
    root1.geometry("300x280")
    root1.configure(fg_color = "#79452E")
    root1.iconbitmap(script_directory + "\\Pandas.ico")
    root1.title("Create Pandas DataFrame")
    root1.resizable(False,False)

    column_label = ctk.CTkLabel(root1, text="Enter column names separated by commas:",text_color="white")
    column_label.pack()
    column_entry = ctk.CTkEntry(root1, fg_color="#BAA099",width=250)
    column_entry.pack()

    data_label = ctk.CTkLabel(root1, text="Enter data (one row per line):" ,text_color="white")
    data_label.pack()
    data_text = ctk.CTkTextbox(root1, height=150, width=250, fg_color="#BAA099")
    data_text.pack()

    create_button = ctk.CTkButton(root1, text="Create DataFrame", command=create_dataframe, fg_color="#946B60",hover_color="#BAA099")
    create_button.place(relx=0.26 , rely=0.855)

    root1.mainloop()

def Adjust():

    global df
    Upload()

    root2 = ctk.CTk()
    root2.geometry("280x180")
    root2.configure(fg_color = "#79452E")
    root2.iconbitmap(script_directory + "\\Pandas.ico")
    root2.title("Adjust Columns")
    root2.resizable(False,False)

    column_names = df.columns.tolist()
    DataTypes = ["Float","Integer","String","Boolean","Date & Time","Category Data"]

    def Done():
        selected_Column = Column_box.get()
        selected_DataType = DataType_box.get()
        TextBox2.delete(1.0, tk.END)

        def EnterData():
            data = tabulate(df, headers='keys', tablefmt='github')  
            TextBox1.configure(state="normal")
            TextBox1.delete(1.0, tk.END)  
            TextBox1.insert(tk.END, data) 
            TextBox1.configure(state="disabled")
    
        if selected_DataType == "Float" :
            try: 
                df[selected_Column] = df[selected_Column].astype(float)
                EnterData()
                TextBox2.delete(1.0, tk.END)  
                TextBox2.insert(tk.END, "Data in ' " + selected_Column + " ' is converted to Float")
            except :
                TextBox2.delete(1.0, tk.END) 
                TextBox2.insert(tk.END, "Cannot convert ' " + selected_Column + " ' to Float")

        elif selected_DataType == "Integer" :
            try:
                df[selected_Column] = df[selected_Column].astype(int)
                EnterData()
                TextBox2.delete(1.0, tk.END) 
                TextBox2.insert(tk.END, "Data in ' " + selected_Column + " ' is converted to Integer")
            except :
                TextBox2.delete(1.0, tk.END) 
                TextBox2.insert(tk.END, "Cannot convert ' " + selected_Column + " ' to Integer")

        elif selected_DataType == "String" :
            try:
                df[selected_Column] = df[selected_Column].astype(str)
                EnterData()
                TextBox2.delete(1.0, tk.END) 
                TextBox2.insert(tk.END, "Data in ' " + selected_Column + " ' is converted to String")
            except :
                TextBox2.delete(1.0, tk.END) 
                TextBox2.insert(tk.END, "Cannot convert ' " + selected_Column + " ' to String")

        elif selected_DataType == "Boolean" :
            try:
                df[selected_Column] = df[selected_Column].astype(bool)
                EnterData()
                TextBox2.delete(1.0, tk.END)  
                TextBox2.insert(tk.END, "Data in ' " + selected_Column + " ' is converted to Boolean")
            except :
                TextBox2.delete(1.0, tk.END) 
                TextBox2.insert(tk.END, "Cannot convert ' " + selected_Column + " ' to Boolean")

        elif selected_DataType == "Date & Time" :
            try:
                df[selected_Column] = pd.to_datetime(df[selected_Column])
                EnterData()
                TextBox2.delete(1.0, tk.END)  
                TextBox2.insert(tk.END, "Data in ' " + selected_Column + " ' is converted to Date & Time")
            except :
                TextBox2.delete(1.0, tk.END) 
                TextBox2.insert(tk.END, "Cannot convert ' " + selected_Column + " ' to Date & Time")

        elif selected_DataType == "Category Data" :
            try:
                df[selected_Column] = df[selected_Column].astype('category')
                EnterData()
                TextBox2.delete(1.0, tk.END) 
                TextBox2.insert(tk.END, "Data in ' " + selected_Column + " ' is converted to Category data")
            except :
                TextBox2.delete(1.0, tk.END) 
                TextBox2.insert(tk.END, "Cannot convert ' " + selected_Column + " ' to Category Data")

    column_label = ctk.CTkLabel(root2, text="Choose the Column to Adjust",text_color="white")
    column_label.pack()

    Column_box = ctk.CTkComboBox(root2, values = column_names, fg_color="#CAB69D")
    Column_box.pack()

    DataType_label = ctk.CTkLabel(root2, text="Choose the Data Type to Adjust",text_color="white")
    DataType_label.pack()

    DataType_box = ctk.CTkComboBox(root2, values = DataTypes, fg_color="#CAB69D")
    DataType_box.pack()


    Button_Done = ctk.CTkButton(root2, text="Done", fg_color="#946B60",hover_color="#BAA099", width=60 ,command = Done)
    Button_Done.place(relx=0.4, rely=0.7)

    root2.mainloop()

Frame1 = ctk.CTkFrame(root, width=785, height=685, fg_color="#79452E", corner_radius=15)
Frame1.place(relx=0.01,rely=0.01)

TextBox1 = ctk.CTkTextbox(Frame1, width=770 ,height=280, corner_radius=15, fg_color="#BAA099", text_color="black",border_width=1.5, border_color="#381B1D",font=("Arial", 20))
TextBox1.place(relx=0.009,rely=0.01)

TextBox2 = ctk.CTkTextbox(Frame1, width=770, height=135, corner_radius=15, fg_color="#946B60", text_color="white",border_width=1, border_color="#BAA099",font=("Arial", 17))
TextBox2.place(relx=0.009,rely=0.43)

    #   - - Button Frames - -
Frame2 = ctk.CTkFrame(Frame1, width=70, height=70, corner_radius=10, fg_color="#BAA099")
Frame2.place(relx=0.01, rely=0.65)

Frame3 = ctk.CTkFrame(Frame1, width=70, height=70, corner_radius=10, fg_color="#BAA099")
Frame3.place(relx=0.23, rely=0.65)

Frame4 = ctk.CTkFrame(Frame1, width=70, height=70, corner_radius=10, fg_color="#BAA099")
Frame4.place(relx=0.45, rely=0.65)

Frame5 = ctk.CTkFrame(Frame1, width=70, height=70, corner_radius=10, fg_color="#BAA099")
Frame5.place(relx=0.67, rely=0.65)

Frame6 = ctk.CTkFrame(Frame1, width=70, height=70, corner_radius=10, fg_color="#BAA099")
Frame6.place(relx=0.89, rely=0.65)

Frame7 = ctk.CTkFrame(Frame1, width=70, height=70, corner_radius=10, fg_color="#BAA099")
Frame7.place(relx=0.01, rely=0.82)

Frame8 = ctk.CTkFrame(Frame1, width=70, height=70, corner_radius=10, fg_color="#BAA099")
Frame8.place(relx=0.23, rely=0.82)

Frame9 = ctk.CTkFrame(Frame1, width=70, height=70, corner_radius=10, fg_color="#BAA099")
Frame9.place(relx=0.45, rely=0.82)

Frame10 = ctk.CTkFrame(Frame1, width=70, height=70, corner_radius=10, fg_color="#BAA099")
Frame10.place(relx=0.67, rely=0.82)

Frame11 = ctk.CTkFrame(Frame1, width=70, height=70, corner_radius=10, fg_color="#BAA099")
Frame11.place(relx=0.89, rely=0.82)

Frame_Clear = ctk.CTkFrame(Frame1, width=60 ,height=48 , corner_radius=10,border_width=2 ,border_color="white", bg_color="#BAA099", fg_color="#946B60")
Frame_Clear.place(relx=0.9, rely=0.025)

Frame_Save = ctk.CTkFrame(Frame1, width=60 ,height=48 , corner_radius=10,border_width=2 ,border_color="white", bg_color="#BAA099", fg_color="#946B60")
Frame_Save.place(relx=0.815, rely=0.025)

#   - - Labels - -

Label1 = ctk.CTkLabel(Frame1, fg_color="transparent", text="Create",text_color="white", font=("Arial", 20))
Label1.place(relx=0.015, rely=0.76)

Label2 = ctk.CTkLabel(Frame1, fg_color="transparent", text="Upload",text_color="white", font=("Arial", 20))
Label2.place(relx=0.235, rely=0.76)

Label3 = ctk.CTkLabel(Frame1, fg_color="transparent", text="Go To",text_color="white", font=("Arial", 20))
Label3.place(relx=0.459, rely=0.76)

Label4 = ctk.CTkLabel(Frame1, fg_color="transparent", text="Quick Filter",text_color="white", font=("Arial", 20))
Label4.place(relx=0.65, rely=0.76)

Label5 = ctk.CTkLabel(Frame1, fg_color="transparent", text="Remove",text_color="white", font=("Arial", 20))
Label5.place(relx=0.89, rely=0.76)

Label1 = ctk.CTkLabel(Frame1, fg_color="transparent", text="Replace",text_color="white", font=("Arial", 20))
Label1.place(relx=0.013, rely=0.93)

Label2 = ctk.CTkLabel(Frame1, fg_color="transparent", text="Adjust",text_color="white", font=("Arial", 20))
Label2.place(relx=0.24, rely=0.93)

Label3 = ctk.CTkLabel(Frame1, fg_color="transparent", text="Calculate",text_color="white", font=("Arial", 20))
Label3.place(relx=0.445, rely=0.93)

Label4 = ctk.CTkLabel(Frame1, fg_color="transparent", text="Correlation",text_color="white", font=("Arial", 20))
Label4.place(relx=0.66, rely=0.93)

Label5 = ctk.CTkLabel(Frame1, fg_color="transparent", text="Set",text_color="white", font=("Arial", 20))
Label5.place(relx=0.915, rely=0.93)

#   - - Buttons - -
btn1_path = os.path.join(script_directory + "\\Button Icons\\Create.png" )
btn1_icon = tk.PhotoImage(file = btn1_path)

btn1 = ctk.CTkButton(Frame2,text=None,image=btn1_icon ,corner_radius=10, fg_color="transparent", border_width=2 , border_color="white",width=10,height=63,hover_color="#946B60",command=Create)
btn1.place(relx=0.04, rely=0.05)

btn2_path = os.path.join(script_directory + "\\Button Icons\\Upload.png" )
btn2_icon = tk.PhotoImage(file = btn2_path)

btn2 = ctk.CTkButton(Frame3,text=None,image=btn2_icon ,corner_radius=10, fg_color="transparent", border_width=2 , border_color="white",width=10,height=63,hover_color="#946B60",command=Upload)
btn2.place(relx=0.04, rely=0.05)

btn3_path = os.path.join(script_directory + "\\Button Icons\\Go to.png" )
btn3_icon = tk.PhotoImage(file = btn3_path)

btn3 = ctk.CTkButton(Frame4,text=None,image=btn3_icon ,corner_radius=10, fg_color="transparent", border_width=2 , border_color="white",width=10,height=63,hover_color="#946B60", command=Go_to)
btn3.place(relx=0.04, rely=0.05)

btn4_path = os.path.join(script_directory + "\\Button Icons\\Filter.png" )
btn4_icon = tk.PhotoImage(file = btn4_path)

btn4 = ctk.CTkButton(Frame5,text=None,image=btn4_icon ,corner_radius=10, fg_color="transparent", border_width=2 , border_color="white",width=10,height=63,hover_color="#946B60", command= Quick_Filter)
btn4.place(relx=0.04, rely=0.05)

btn5_path = os.path.join(script_directory + "\\Button Icons\\Remove.png" )
btn5_icon = tk.PhotoImage(file = btn5_path)

btn5 = ctk.CTkButton(Frame6,text=None,image=btn5_icon ,corner_radius=10, fg_color="transparent", border_width=2 , border_color="white",width=10,height=63,hover_color="#946B60", command=Remove)
btn5.place(relx=0.04, rely=0.05)

btn6_path = os.path.join(script_directory + "\\Button Icons\\Replace.png" )
btn6_icon = tk.PhotoImage(file = btn6_path)

btn6 = ctk.CTkButton(Frame7,text=None,image=btn6_icon ,corner_radius=10, fg_color="transparent", border_width=2 , border_color="white",width=10,height=63,hover_color="#946B60", command=Replace)
btn6.place(relx=0.04, rely=0.05)

btn7_path = os.path.join(script_directory + "\\Button Icons\\Adjust.png" )
btn7_icon = tk.PhotoImage(file = btn7_path)

btn7 = ctk.CTkButton(Frame8,text=None,image=btn7_icon ,corner_radius=10, fg_color="transparent", border_width=2 , border_color="white",width=10,height=63,hover_color="#946B60",command = Adjust)
btn7.place(relx=0.04, rely=0.05)

btn8_path = os.path.join(script_directory + "\\Button Icons\\Calculate.png" )
btn8_icon = tk.PhotoImage(file = btn8_path)

btn8 = ctk.CTkButton(Frame9,text=None,image=btn8_icon ,corner_radius=10, fg_color="transparent", border_width=2 , border_color="white",width=10,height=63,hover_color="#946B60",command=Calculate)
btn8.place(relx=0.04, rely=0.05)

btn9_path = os.path.join(script_directory + "\\Button Icons\\Correlation.png" )
btn9_icon = tk.PhotoImage(file = btn9_path)

btn9 = ctk.CTkButton(Frame10,text=None,image=btn9_icon ,corner_radius=10, fg_color="transparent", border_width=2 , border_color="white",width=10,height=63,hover_color="#946B60",command=Correlation)
btn9.place(relx=0.04, rely=0.05)

btn10_path = os.path.join(script_directory + "\\Button Icons\\Set.png" )
btn10_icon = tk.PhotoImage(file = btn10_path)

btn10 = ctk.CTkButton(Frame11,text=None,image=btn10_icon ,corner_radius=10, fg_color="transparent", border_width=2 , border_color="white",width=10,height=63,hover_color="#946B60",command=Set)
btn10.place(relx=0.04, rely=0.05)

img_path = os.path.join(script_directory+ "\\Button Icons\\Clear.png")
btnClear_icon = tk.PhotoImage(file = img_path)
Button1 = ctk.CTkButton(Frame_Clear, image= btnClear_icon,text="", width=30 ,height=30 ,corner_radius=10,fg_color="transparent",bg_color="#946B60",hover_color="#79452E",command=clear_all )
Button1.place(relx=0.05,rely=0.1)

img1_path = os.path.join(script_directory+ "\\Button Icons\\Save.png")
btnSave_icon = tk.PhotoImage(file = img1_path)
Button1 = ctk.CTkButton(Frame_Save, image= btnSave_icon,text="", width=30 ,height=30 ,corner_radius=10,fg_color="transparent",bg_color="#946B60",hover_color="#79452E",command=Save )
Button1.place(relx=0.05,rely=0.1)

root.mainloop()