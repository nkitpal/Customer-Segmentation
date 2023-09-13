from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage

import os.path
from os import path

import warnings
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sb 
from mpl_toolkits.mplot3d import Axes3D 
from termcolor import colored as cl
from sklearn.preprocessing import StandardScaler 
from sklearn.cluster import KMeans 

loc='Cluster/static/images/'
loc_csv='Cluster/uploads/'
selected_file=None

warnings.filterwarnings("ignore")

def visualize(request):
        if(selected_file is not None):
                return HttpResponse('Visualize Successful')

def info(request):
        if(selected_file is not None):
                return HttpResponse('Info Successful')

def csv(request):
        if(selected_file is not None):
                return HttpResponse('Csv Successful')

def home(request):
    
    global selected_file
    selected_file=None

    myfile = request.FILES['myfile'] if 'myfile' in request.FILES else False
    
    if(request.method=='POST' and myfile!=False):

        if(path.exists(loc_csv+myfile.name)):
            os.remove(loc_csv+myfile.name)

        selected_file=myfile.name

        fs = FileSystemStorage(location=loc_csv)
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

        #ML Code

        if(selected_file is not None):
                plt.rcParams['figure.figsize'] = (20, 10)
                sb.set_style('whitegrid')

                df = pd.read_csv(loc_csv+selected_file)
                df.drop('Unnamed: 0', axis = 1, inplace = True)
                df.set_index('Customer Id', inplace = True)
                
                sb.histplot(df['Age'], 
                        color = 'orange')
                plt.title('AGE DISTRIBUTION', 
                        fontsize = 18)
                plt.xlabel('Age', 
                        fontsize = 16)
                plt.ylabel('Frequency', 
                        fontsize = 16)
                plt.xticks(fontsize = 14)
                plt.yticks(fontsize = 14)

                plt.savefig(loc+'age_distribution.png',dpi=300, bbox_inches='tight')

                plt.clf()
                plt.cla()
                plt.cla()


                sb.countplot(x=df['Defaulted'], 
                        palette = ['coral', 'deepskyblue'], 
                        edgecolor = 'darkgrey')
                plt.title('Credit card default cases(1) and non-default cases(0)', 
                        fontsize = 18)
                plt.xlabel('Default value', 
                        fontsize = 16)
                plt.ylabel('Number of People', 
                        fontsize = 16)
                plt.xticks(fontsize = 14)
                plt.yticks(fontsize = 14)

                plt.savefig(loc+'default_cases.png',dpi=300,bbox_inches='tight')

                sb.scatterplot(x='Age',y='Income', 
                        data = df, 
                        color = 'deepskyblue', 
                        s = 150, 
                        alpha = 0.6, 
                        edgecolor = 'b')
                plt.title('AGE / INCOME', 
                        fontsize = 18)
                plt.xlabel('Age', 
                        fontsize = 16)
                plt.ylabel('Income', 
                        fontsize = 16)
                plt.xticks(fontsize = 14)
                plt.yticks(fontsize = 14)

                plt.savefig(loc+'age_income.png',dpi=300,bbox_inches='tight')

                plt.clf()
                plt.cla()
                sb.scatterplot(x='Years Employed',y='Income', 
                        data = df, 
                        s = 150,
                        alpha = 0.6, 
                        edgecolor = 'white', 
                        hue = 'Defaulted', 
                        palette = 'spring')

                plt.title('YEARS EMPLOYED / INCOME', 
                        fontsize = 18)
                plt.xlabel('Years Employed', 
                        fontsize = 16)
                plt.ylabel('Income', 
                        fontsize = 16)
                plt.xticks(fontsize = 14)
                plt.yticks(fontsize = 14)
                plt.legend(loc = 'upper left', fontsize = 14)

                plt.savefig(loc+'y_income.png',dpi=300,bbox_inches='tight')

                plt.clf()
                plt.cla()
                X = df.values
                X = np.nan_to_num(X)

                sc = StandardScaler()

                cluster_data = sc.fit_transform(X)
        
                clusters = 3
                model = KMeans(init = 'k-means++', 
                        n_clusters = clusters, 
                        n_init = 12)
                model.fit(X)

                labels = model.labels_

                df['cluster_num'] = labels

                area = np.pi*(df.Edu)**4

                sb.scatterplot(x='Age', y='Income', 
                        data = df, 
                        s = area, 
                        hue = 'cluster_num', 
                        palette = 'spring', 
                        alpha = 0.6, 
                        edgecolor = 'darkgrey')
                plt.title('AGE / INCOME (CLUSTERED)', 
                        fontsize = 18)
                plt.xlabel('Age', 
                        fontsize = 16)
                plt.ylabel('Income', 
                        fontsize = 16)
                plt.xticks(fontsize = 14)
                plt.yticks(fontsize = 14)
                plt.legend(loc = 'upper left', fontsize = 14)

                plt.savefig(loc+'c_age_income.png', dpi=300, bbox_inches='tight')

                fig = plt.figure(1)
                plt.clf()
                ax = Axes3D(fig, 
                        rect = [0, 0, .95, 1], 
                        elev = 48, 
                        azim = 134,
                        auto_add_to_figure=False)
                fig.add_axes(ax)

                plt.cla()
                ax.scatter(df['Edu'], df['Age'], df['Income'], 
                        c = df['cluster_num'], 
                        s = 200, 
                        cmap = 'spring', 
                        alpha = 0.5, 
                        edgecolor = 'darkgrey')
                ax.set_xlabel('Education', 
                        fontsize = 16)
                ax.set_ylabel('Age', 
                        fontsize = 16)
                ax.set_zlabel('Income', 
                        fontsize = 16)

                plt.savefig(loc+'3d_plot.png',dpi=300,bbox_inches='tight')

        #ML Code Ends
                data1=df.head()
                data1=data1.to_html()
                print(cl(df.head(), attrs = ['bold']))
                print()

                data2=df['Age'].describe()
                print(cl(df['Age'].describe(), attrs = ['bold']))
                print()

                data3=cluster_data[:5]
                print(cl('Cluster data samples : ', attrs = ['bold']), cluster_data[:5])
                print()
                
                data4=labels[:100]
                print(cl(labels[:100], attrs = ['bold']))
                print()

                data5=df.head()
                data5=data5.to_html()
                print(cl(df.head(), attrs = ['bold']))
                print()

                data6=df.groupby('cluster_num').mean()
                data6=data6.to_html()
                print(cl(df.groupby('cluster_num').mean(), attrs = ['bold']))

                csv=df.to_html()

        return render(request, 'index.html', {
            'uploaded_file_url': uploaded_file_url,
            'selected':selected_file,
            'data1':data1,
            'data2':data2,
            'data3':data3,
            'data4':data4,
            'data5':data5,
            'data6':data6,
            'csv':csv
        })

    return render(request,'index.html',{'selected':selected_file})