from tkinter import *
from tkinter import ttk
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from mpl_toolkits.mplot3d import Axes3D
from tkinter import messagebox
import requests
import networkx as nx
import matplotlib.pyplot as plt
import nltk
import numpy as np
import tkinter as tk
from PIL import ImageTk, Image

#---------------------------------------------------------------------------------#

def SearchBar():
    root = Tk()
    root.title("Search Bar")
    root.geometry("1200x900")
    root['background']='#4d1a8b'

    def starter():
    	query = search.get()
    	nums = int(number.get())
    	checkers(query,nums,root)

    image = Image.open("Market.png")

    resize_image = image.resize((800,500))
    alpha_image = resize_image.convert("RGBA")
    img = ImageTk.PhotoImage(resize_image)

    label2 = Label(root, image=img,borderwidth=0)
    label2.image = img
    label2.pack(side = TOP)

    Label(root,bg = '#4d1a8b',fg = "white",text = "From apnews.com",font=("Times New Roman", 30),width = 20).pack()


    Label(root,bg = '#4d1a8b',fg = "#e2e7be",text = "Search",font=("Times New Roman", 20),width = 20).pack()

    search = Entry(root,font=("Times New Roman", 25),width = 30,justify = CENTER)
    search.focus_force()
    search.pack()

    Label(root,bg = '#4d1a8b',width = 25).pack()

    Label(root,bg = '#4d1a8b',fg = "#e2e7be",text = "Numbers of headlines needed",font=("Times New Roman", 20),width = 25).pack()
    Label(root,bg = '#4d1a8b',fg = "#e2e7be",text = "(Up to 50)",font=("Times New Roman", 15),width = 25).pack()

    number = Entry(root,font=("Times New Roman", 20),width = 10,justify = CENTER)
    number.focus_force()
    number.pack()

    Label(root,bg = '#4d1a8b',width = 25).pack()

    border1 = tk.Frame(root, highlightbackground = "#862235", highlightthickness = 2, bd=0)
    btn = Button(border1,text = 'Enter',fg = 'white',bg = '#d42b69',activebackground="#e3759e",font = ("Times New Roman",14),height = 1,width = 12,command = starter,borderwidth = 0)
    btn.pack()
    border1.pack()

    Label(root,bg = '#4d1a8b',width = 25).pack()

    border2 = tk.Frame(root, highlightbackground = "#862235", highlightthickness = 2, bd=0)
    exit = Button(border2,text = 'Exit',fg = 'white',bg = 'Red',activebackground="#e3759e",font = ("Times New Roman",14),height = 1,width = 12,command = root.destroy,borderwidth = 0)
    exit.pack()
    border2.pack()

    Label(root,bg = '#4d1a8b',width = 25).pack() 

    root.mainloop()
#---------------------------------------------------------------------------------#

def checkers(query,nums,root):
    URL = f"https://apnews.com/search?q={query}"
    r = requests.get(URL)
    if r.status_code == 200:
        if nums > 2 and nums < 50:
        	Label(root,bg = '#4d1a8b',fg = "#e2e7be",text = "You are good to go",font=("Times New Roman", 20),width = 25).pack()
        	headlines = scraps(r,nums)
        	G = SETUP(headlines)
        	Page_main(G , headlines,query,nums)
        else:
            messagebox.showerror('Not Valid!','Must be between 2 and 50 headlines')

    else:
        print(f"{query} Didn't work, find something else!")

#---------------------------------------------------------------------------------#
#Home:
def Page_main(G , headlines,query,nums):

    def del1():
        heatmap_plot(G)

    def del2():
        create_graph(G)

    def del3():
        thrd_graph(G)

    def del4():
        centralitics(G)


    def delete():
        pa.destroy()


    pa = Toplevel()
    pa.title("Main")
    pa.geometry("700x200")
    pa.resizable(False, False)
    pa['background']='#4d1a8b'

    Label(pa,bg = '#4d1a8b',font=("Times New Roman", 20 , "bold"),fg = "#e2e7be",text=f'Topic: {query}').pack(side = TOP)
    Label(pa,bg = '#4d1a8b',font=("Times New Roman", 20 , "bold"),fg = "#e2e7be",text=f'Nums of headlines: {nums}').pack(side = TOP)

    Button(pa,activebackground="cyan",bg="blue",font=("Times New Roman", 12),text='2D Graph',height=2, width=15,fg="white", command=del2).pack(side = LEFT)
    Button(pa,activebackground="cyan",bg="blue",font=("Times New Roman", 12),text='3D Graph',height=2, width=15,fg="white", command=del3).pack(side = LEFT)
    Button(pa,activebackground="cyan",bg="blue",font=("Times New Roman", 12),text='Heat map',height=2, width=15,fg="white", command=del1).pack(side = LEFT)
    Button(pa,activebackground="cyan",bg="blue",font=("Times New Roman", 12),text='Centrality',height=2, width=15,fg="white", command=del4).pack(side = LEFT)
    Button(pa,bg="red",font=("Times New Roman", 12),text='Quit',height=2, width=15,fg="white", command=delete).pack(side = LEFT)
    pa.mainloop()



#Scrap the data
def scraps(r,nums):
    soup2 = BeautifulSoup(r.content, "html.parser")
    headlines = soup2.find_all('div', class_='PagePromo-title')
    for headline in headlines[:nums]:
        print("\n",headline.get_text(strip=True))
    print("#-------------------------------------------#")
    return [headline.get_text(strip=True) for headline in headlines[:nums]]

#---------------------------------------------------------------------------------#

#make plots
def SETUP(headlines):
    G = nx.Graph()
    for headline in headlines:
        G.add_node(headline)

    for i in range(len(headlines)):
        for j in range(i + 1, len(headlines)):
            tokens1 = set(word_tokenize(headlines[i].lower()))
            tokens2 = set(word_tokenize(headlines[j].lower()))
            common_keywords = set(tokens1).intersection(set(tokens2))
            if common_keywords:
                G.add_edge(headlines[i], headlines[j], weight=len(common_keywords))
    return G

#----------------------------------------------------------------------------------#


#make 2D Graph
def create_graph(G):
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, font_size=8, node_size=300)
    plt.show()

    return G

#---------------------------------------------------------------------------------#

#inbetween centrality
def centralitics(G):
    between = nx.betweenness_centrality(G)
    Degree = nx.degree_centrality(G)
    close = nx.closeness_centrality(G)

    print("Key nodes based on betweenees Centrality:")
    for node1, centrality1 in sorted(between.items(), key=lambda x: x[1], reverse=True):
        print(node1, centrality1)
    print("Key nodes based on degree Centrality:")
    for node2, centrality2 in sorted(Degree.items(), key=lambda x: x[1], reverse=True):
        print(node2, centrality2)
    print("Key nodes based on Closeness Centrality:")
    for node3, centrality3 in sorted(close.items(), key=lambda x: x[1], reverse=True):
        print(node3, centrality3)

#---------------------------------------------------------------------------------#

#Da Heat
def heatmap_plot(G):
    edge_weights = nx.get_edge_attributes(G, 'weight')
    edge_list = [(edge[0], edge[1], weight) for edge, weight in edge_weights.items()]
    edge_labels = {(edge[0], edge[1]): weight for edge, weight in edge_weights.items()}

    nodes = list(G.nodes())
    adjacency_matrix = np.zeros((len(nodes), len(nodes)))

    for i in range(len(nodes)):
        for j in range(len(nodes)):
            if G.has_edge(nodes[i], nodes[j]):
                adjacency_matrix[i][j] = G[nodes[i]][nodes[j]]['weight']
            elif G.has_edge(nodes[j], nodes[i]):
                adjacency_matrix[j][i] = G[nodes[j]][nodes[i]]['weight']

    plt.figure(figsize=(8, 6))  # Adjust figure size as needed
    plt.title("Heatmap of Node Relationships")
    plt.xlabel("Node")
    plt.ylabel("Node")
    plt.show()

#---------------------------------------------------------------------------------#

#3D graph (its fun)
def thrd_graph(G):
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    pos = nx.spring_layout(G, dim=3)
    nodes = list(G.nodes())

    node_colors = {}
    for i, node in enumerate(nodes):
        node_colors[node] = plt.cm.tab20(i % 20)

    for node in nodes:
        x, y, z = pos[node]
        ax.scatter(x, y, z, c=node_colors[node], label=node)

    for u, v, d in G.edges(data=True):
        ax.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]], [pos[u][2], pos[v][2]], color='grey')

    ax.set_title('3D Network Graph')
    ax.legend()
    plt.show()


#---------------------------------------------------------------------------------#

query = SearchBar()

