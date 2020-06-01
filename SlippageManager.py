import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
from dateutil import parser
import fractions
import os.path
import urllib
import webbrowser

def grab_data_file(file_name):
	if (os.path.isfile(file_name)):
		if (os.path.splitext(file_name)[1] != 'csv'):
			raise Exception('File must be a csv')
		raise Exception('File does not exist')
	return pd.read_csv(file_name)

def format_data(df):
	df.set_index(['date'], inplace = True)
	df = df[['spread_name', 'quoting_logical_exch', 'n_neg_slip', 'sz_neg_slip','neg_slip','q_crej', 'h_crej','avg_neg_slip']]
	df.rename(columns = {'spread_name' : 'Name_of_Spread', 'quoting_logical_exch' : 'Exchange', 'n_neg_slip': 'Pairs_with_Negative_Edge', 'sz_neg_slip':'Size_of_Pairs_with_Negative_Edge','neg_slip' : 'Sum_of_Pairings_with_Slippage','q_crej' : 'Quote_Cancel_Rejects', 'h_crej' : 'Hedge_Cancel_Rejects','avg_neg_slip' : 'Average_Negative_Slippage'}, inplace = True)
	return df

def get_cancel_reject_ratio(df):
	df['%Ratio for Q/H'] = ((np.array(df['Quote_Cancel_Rejects']))/(np.array(df['Hedge_Cancel_Rejects']))* 100.0)
	return df

df = grab_data_file(file_path) 

#Correlation_NegDF.plot(kind ='bar')
def setGraph(ndf, exchange_name):
	if(all(ndf['Exchange'] != exchange_name)):
		print("The exchange you have type is not in this spread! Try changing your spread by using the add function")
		printGraphs()
	else:
		set_df = ndf[ndf['Exchange'] == exchange_name]
		plt.figure()
		plt.xlabel(exchange_name)
		plt.ylabel('Slippage')

		sumt = set_df['Average_Negative_Slippage'].sum(axis=1)
		sumh = set_df['Hedge_Cancel_Rejects'].sum(axis=1)
		sumq = set_df['Quote_Cancel_Rejects'].sum(axis=1)

		plt.text(20,-0.018,"Summation of Avg Negative Slippage: " + str(sumt), bbox={'facecolor':'blue', 'alpha':0.5, 'pad':10})

		##Average Negative Slippage
		df_test = set_df['Average_Negative_Slippage'].dropna()
		DateArgs = np.array(df_test.index)
		x = np.array([dt.datetime.strptime(d, '%Y-%m-%d').date() for d in DateArgs])
		y = np.array(df_test)
		plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
		plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval = 2))
		plt.plot(x,y)
		plt.gcf().autofmt_xdate()
		plt.grid()

		##Quote/Hedge Cancel Rejects
		plt.figure()
		plt.xlabel(exchange_name)
		plt.ylabel('Cancel Rejects')
		#Quote CRej Val
		yQ = np.array(set_df['Quote_Cancel_Rejects'])
		xQ = np.array(range(0,len(set_df['Quote_Cancel_Rejects'])))
		yH = np.array(set_df['Hedge_Cancel_Rejects'])
		xH = np.array(range(0,len(set_df['Hedge_Cancel_Rejects'])))

		coefficientsQ = np.polyfit(xQ,yQ, deg=1)
		polynomialQ = np.poly1d(coefficientsQ)
		ysQ = polynomialQ(xQ)
		plt.plot(xQ, ysQ, label = "Quote BestFit Line" + " f(x)=" + str(polynomialQ), color = 'red')
		coefficientsH = np.polyfit(xH,yH, deg=1)
		polynomialH = np.poly1d(coefficientsH)
		ysH = polynomialH(xH)
		plt.plot(xH, ysH, label = "Hedge BestFit Line " + "f(x)=" + str(polynomialH), color = 'blue')

		plt.plot(xQ,set_df['Quote_Cancel_Rejects'], label = "Quote Cancel Rejects, Total:" + str(sumq), color = 'red')
		plt.plot(xH,set_df['Hedge_Cancel_Rejects'], label = "Hedge Cancel Rejects, Total:" + str(sumh), color = 'blue')
		plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,ncol=2, mode="expand", borderaxespad=0.)

		plt.grid()

		FileString = exchange_name + "SlipData.html"
		if(os.path.isfile(FileString) == False):
			set_df.to_html(open(FileString, 'w'))
		htmlpage = urllib.urlopen(FileString).read()
		webbrowser.open_new_tab(FileString)
		plt.show()

########Print Different Graphs#############
########WORK IN PROGRESS###################
def printGraphs(df=None):
	graphName = input("Enter Command here: ")
	if("arca" in graphName):
		graphName = "Arca"
		setGraph(df,graphName)
	if("byx" in graphName):
		graphName = "BYX"
		setGraph(df,graphName)
	if("bloom" in graphName):
		graphName = "Bloomberg"
		setGraph(df,graphName)
	if("cbx" in graphName):
		graphName = "CBX"
		setGraph(df,graphName)
	if("cs" in graphName):
		graphName = "CS"
		setGraph(df,graphName)
	if("pool" in graphName):
		graphName = "CSLPool"
		setGraph(df,graphName)
	if("citi" in graphName):
		graphName = "CitiMatch"
		setGraph(df,graphName)
	if("dbp" in graphName):
		graphName = "DBPool"
		setGraph(df,graphName)
	if("ice" in graphName):
		graphName = "ICE"
		setGraph(df,graphName)
	if("iex" in graphName):
		graphName = "IEX"
		setGraph(df,graphName)
	if("isb" in graphName):
		graphName = "ISBX"
		setGraph(df,graphName)
	if("itg" in graphName):
		graphName = "ITG"
		setGraph(df,graphName)
	if("inet" in graphName):
		graphName = "Inet"
		setGraph(df,graphName)
	if("jpm" in graphName):
		graphName = "JPMX"
		setGraph(df,graphName)
	if("knight" in graphName):
		graphName = "KnightMatch"
		setGraph(df,graphName)
	if("lev" in graphName):
		graphName = "LEVEL"
		setGraph(df,graphName)
	if("lx" in graphName):
		graphName = "LX"
		setGraph(df,graphName)
	if("mlxn" in graphName):
		graphName = "MLXN"
		setGraph(df,graphName)
	if("ubs" in graphName):
		graphName = "UBS"
		setGraph(df,graphName)
	if("edgx" in graphName):
		graphName = "EDGX"
		setGraph(df,graphName)
	if("edga" in graphName):
		graphName = "EDGA"
		setGraph(df,graphName)
	if("nyse" in graphName):
		graphName = "NYSE"
		setGraph(df,graphName)
	if("gs" in graphName):
		graphName = "GS"
		setGraph(df,graphName)
	elif("exit" in graphName):
		raise SystemExit
	elif("add" in graphName):
		main(False)
	elif("help" in graphName):
		print("\nSimply type the name of an exchange in lowercase\nOther Commands include:\nadd = adds a new .csv file to look at \nexit = exits the program")
		main(False)
	else:
		print("Error! Type in help for list of commands")
		main(False)

def main(first_run):
	if (first_run):
		print('================================================')
		print('Slippage Manager v{}'.format('0.0.2')) # I'll add this to read in from a config file
		print('================================================')
	file_path = input("Enter path for CSV File: ")
	df = grab_data_file(file_path)
	format_data(df)
	get_cancel_reject_ratio(df)
	printGraphs(df)
if __name__ == "__main__":
	main(True)
	