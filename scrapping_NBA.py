import pandas as pd
import numpy as np
import requests as req
def team_wins(): #web scrapping to create dataframe containing wins from 2005-2018 season 
    year=np.arange(2005,2019)
    Team_Data=pd.DataFrame(columns=['Year','Team','W','PPG','PAG']) #intilaize dataframe
    for i in year:
        name_list=[] 
        temp=pd.DataFrame() #create temporary dataframe to append onto main df
        print(i)
        site_url="https://www.basketball-reference.com/leagues/NBA_" + str(i) +"_standings.html"
        res= req.get(site_url).text
        p_df=pd.read_html(res) #use method to extract tables from get request
        matrix=np.zeros((30,3))
        for x,df in enumerate(p_df[:2]): #loop through first 2 df (eastern and western conference) 
            pre_mat=df.as_matrix()
            ind_c=[0,1,5,6] #use numpy indexing to extract specific columns I am interested in  
            if i<2016:
                ind_r=[i for i in np.arange(0,18) if i not in [0,6,12]] #use numpy indexing to extract rows I am interested in 
            else:
                ind_r=np.arange(0,15) #use numpy indexing to extract rows I am interested in
            p_mat=pre_mat[ind_r,:] 
            mat=p_mat[:,ind_c] #use two lines to create matrix with the values I want to extract
            for c,q in enumerate(mat[:,0]):
                #loop through teams names to keep just the team name (and remove * and other symbols)
                for k,j in enumerate(q):
                    if j=='*':
                        name_list.append(q[:k].strip())
                        break
                    if j=='(' :
                        name_list.append(q[:k].strip())
                        break
            if x==0: #eastern conf.
                matrix[:15]=mat[:,1:]
            else: #western conf.
                matrix[15:]=mat[:,1:]
        #finally I will create my temporary data frame and append onto to my main dataframe
        temp['Team']=name_list
        matrix[:,1:]=matrix[:,1:]/np.mean(matrix[:,1:],axis=0)
        temp['W']=matrix[:,0]
        temp['PPG']=matrix[:,1]
        temp['PAG']=matrix[:,2]
        temp['Year']=i
        
        Team_Data=Team_Data.append(temp)
        Team_Data=Team_Data.replace('Seattle SuperSonics','Oklahoma City Thunder') # to keep my data consistent, I have decided to replace old team names with their modern names
        Team_Data=Team_Data.replace('New Orleans/Oklahoma City Hornets','New Orleans Hornets')

    return Team_Data
def team_stats(): #imported data from csv files to create database of team stats and a second dataframe of yearly averages across the league
    Team_Stats=pd.DataFrame(columns=['Year','Team', 'ORB', 'DRB', 'AST', 'STL','BLK', 'TOV','PTS','TS', 'aORB', 'aDRB', 'aAST', 'aSTL','aBLK', 'aTOV','aPTS','aTS']) #intialize df
    year=np.arange(2005,2018)
    year_matrix=np.zeros((len(year),17)) #created matrix which be used to create average dataframe
    for y,i in enumerate(year):
        year_matrix[y,0]=i #year
        print(i)
        temp=pd.DataFrame() #created temporary dataframe for team stats
        atemp=pd.DataFrame() #create temporary df for team stats (against, ex. points scored against, assists against)
        for c,v,b in zip(['s','a'],[temp,atemp],[0,8]): #create loop which will loop thru for and against stats seperatly 
            s=pd.read_csv('C:/Users/HP/Documents/WC/'+ c + str(i) + '.txt')
            ex_mat=s.as_matrix() #changed csv file into numpy matrix
            tsm=np.zeros((31,4)) #created matrix that will be used to calculate true shooting precentages (advanced stat)
            tsm[:,0]=s.iloc[:,5] #fga
            tsm[:,1]=s.iloc[:,14] #fta
            tsm[:,2]=s.iloc[:,-1] #pts
            tsm[:,3]=tsm[:,2]/(2*(tsm[:,0]+(.44*tsm[:,1]))) #calculation for true shooting percent
            tsm[:30]=(tsm[:30]-tsm[30])/np.std(tsm[:30],axis=0) #subtract by mean of that season and divide by standard deviation for that season
            ind=[16,17,19,20,21,22] #use numpy indexing to only extract stats I am interested in 
            matt=np.zeros((31,6)) #(team) ORB, DRB, AST, STL, BLK, TOV
            matt=ex_mat[:,ind]
            matt[:30]=(matt[:30]-np.mean(matt[:30],axis=0))/np.std(np.float64(matt[:30],axis=0)) #subtract stats by mean and divide by standard deviation of the year
            #print(matt[30])
            name_list=[]
            year_matrix[y,0]=i #year
            for c,q in enumerate(s['Team'][:30]):
                name_list.append(q)
                #loop through teams names to keep just the team name (and remove * and other symbols)
                for k,j in enumerate(q):
                    if j=='*':
                        name_list[c]=(q[:k].strip())
                        break
                    if j=='(' :
                        name_list[c]=(q[:k].strip())
                        break
            #add values to pandas teams stats dataframe
            v['Team']=name_list
            v['PTS']=tsm[:30,2]
            v['ORB']=matt[:30,0]
            v['DRB']=matt[:30,1]
            v['AST']=matt[:30,2]
            v['STL']=matt[:30,3]
            v['BLK']=matt[:30,4]
            v['TOV']=matt[:30,5]
            v['TS']=tsm[:30,3]
            v['Year']=i
            #add yearly averages to average dataframe
            year_matrix[y,1+b]=matt[30,0] #ORB
            year_matrix[y,2+b]=matt[30,1] #DRB
            year_matrix[y,3+b]=matt[30,2] #AST
            year_matrix[y,4+b]=matt[30,3] #STL
            year_matrix[y,5+b]=matt[30,4] #BLK
            year_matrix[y,6+b]=matt[30,5] #TOV
            year_matrix[y,7+b]=tsm[30,2] #PTS
            year_matrix[y,8+b]=tsm[30,3]  #TS
        atemp=atemp.rename(index=str,columns={'ORB':'aORB','DRB':'aDRB','AST':'aAST','STL':'aSTL','BLK':'aBLK','TOV':'aTOV','PTS':'aPTS','TS':'aTS'}) #rename values in against dataframe before merging for and agaisnt dataframe together
        #replace teams names in data to keep consistent across seasons
        temp=temp.replace('Seattle SuperSonics','Oklahoma City Thunder')
        atemp=atemp.replace('Seattle SuperSonics','Oklahoma City Thunder')
        atemp=atemp.replace('New Orleans/Oklahoma City Hornets','New Orleans Hornets')
        temp=temp.replace('New Orleans/Oklahoma City Hornets','New Orleans Hornets')
        temp=pd.merge(temp,atemp,how='outer', on=['Year','Team']) #merge atemp and temp dataframe before appending onto main df
        Team_Stats=Team_Stats.append(temp) #append dataframe
    
    col=['Year','ORB','DRB','AST','STL','BLK','TOV','PTS','TS','aORB','aDRB','aAST','aSTL','aBLK','aTOV','aPTS','aTS']
    data={}
    for i,j in zip(col,year_matrix.T): #create loop to create year average dataframe 
        data[i]=j
    Year_Ave=pd.DataFrame(data=data)
    return Team_Stats,Year_Ave

#all that is left to do is to merge the two dataframes together
a,c=team_stats()
b=team_wins()
a=a.merge(b,on=['Team','Year'],how='outer')
#a.to_csv('Team_Data.csv')
#c.to_csv('Year_Average.csv')