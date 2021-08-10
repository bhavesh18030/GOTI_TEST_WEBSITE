import urllib.request as lib, json, requests
from bs4 import BeautifulSoup
from bs2json import bs2json
import time
import sys

from requests.models import to_native_string


class Innings:
	def __init__(self,x):
		self.name = x
		self.Batsman = {}
		self.Bowler = {}

class Match:
	tot = 0
	def __init__(self, comm_url, sckrd_url):
		self.pk = Match.tot
		Match.tot +=1
		self.selected = []
		self.is_live = True
		self.url_comm = comm_url
		self.url = sckrd_url
		self.data_comm = requests.get(self.url_comm).text
		self.soup_comm = BeautifulSoup(self.data_comm,"html.parser")
		self.data = requests.get(self.url).text
		self.soup = BeautifulSoup(self.data,"html.parser")
		self.conv = bs2json()

		self.team1, self.team2 = self.get_team_name()

		self.Team = {self.team1:{},self.team2:{}}

		self.Inning =  {self.team1:Innings(self.team1),self.team2:Innings(self.team2)}

	def give_data_and_soup(self):
		self.data_comm = requests.get(self.url_comm).text
		self.soup_comm = BeautifulSoup(self.data_comm,"html.parser")
		self.data = requests.get(self.url).text
		self.soup = BeautifulSoup(self.data,"html.parser")

	def get_playing_11(self):
		curr_11 = ''

		lis = []
		for div in self.soup.findAll('div', attrs={'cb-col cb-col-73'}):
			curr_11 = self.conv.convert(div)
			lis.append(curr_11['div'])

		# print(lis)
		# print(lis)
		for i in range(11):
			name = lis[8]['a'][i]['text'].replace(' (c)','')
			name = name.replace(' (wk)','')
			self.Team[self.team1][name] = 0
		
		for i in range(11):
			name = lis[10]['a'][i]['text'].replace(' (c)','')
			name = name.replace(' (wk)','')
			self.Team[self.team2][name] = 0

	def get_team_name(self):
		div = self.soup_comm.find('div', attrs={'class':'cb-nav-main cb-col-100 cb-col cb-bg-white'})
		json = self.conv.convert(div)
		teams = str(json['div']['div'][0]['h1']['text'])
		team1, team2 = teams[0:teams.index('vs')-1], teams[teams.index('vs')+3:teams.index(',')]
		print("'"+team1+"'","'" +team2+"'")
		return team1,team2


	def get_curr_team_score(self):
		curr_team = ''
		for div in self.soup_comm.findAll('div', attrs={'class':'cb-min-bat-rw'}):
			curr_team = self.conv.convert(div)
		return curr_team['div']['span'][0]['text']

	def get_bats_for_bot(self):
		batball = []
		for div in self.soup_comm.findAll('div', attrs={'class':'cb-col cb-col-100 cb-min-itm-rw'}):
			json1 = self.conv.convert(div)
			batball.append(json1['div'])
		bat = batball[:2]
		bow = [batball[2]]
		ans = []
		dic = {}
		for i in range(2):
			dic['Batsman ' + str(i+1)] = (str(bat[i]['div'][0]['a']['text']), str(bat[i]['div'][1]['text']),str(bat[i]['div'][2]['text']))
			# ans.append('Batsman ' + str(i+1) +  ' : ' + str(bat[i]['div'][0]['a']['text'])+
			# 	'\nRuns : ' + str(bat[i]['div'][1]['text']) + '\nBalls : ' + str(bat[i]['div'][2]['text']))
		return dic

	def get_bowl_for_bot(self):
		batball = []
		for div in self.soup_comm.findAll('div', attrs={'class':'cb-col cb-col-100 cb-min-itm-rw'}):
			json1 = self.conv.convert(div)
			batball.append(json1['div'])
		bat = batball[:2]
		bow = [batball[2]]
		dic = {'name':str(bow[0]['div'][0]['a']['text']),'over':str(bow[0]['div'][1]['text']),
			'runs':str(bow[0]['div'][3]['text']),'wickets':str(bow[0]['div'][4]['text'])}
		return dic


	def get_playing_bats(self):
		batball = []
		for div in self.soup_comm.findAll('div', attrs={'class':'cb-col cb-col-100 cb-min-itm-rw'}):
			json1 = self.conv.convert(div)
			batball.append(json1['div'])
		bat = batball[:2]
		bow = [batball[2]]
		ans = []
		for i in range(2):
			ans.append('Batsman ' + str(i+1) +  ' : ' + str(bat[i]['div'][0]['a']['text'])+
				'\nRuns : ' + str(bat[i]['div'][1]['text']) + '\nBalls : ' + str(bat[i]['div'][2]['text']))
		return ans

	def get_playing_bowl(self):
		batball = []
		for div in self.soup_comm.findAll('div', attrs={'class':'cb-col cb-col-100 cb-min-itm-rw'}):
			json1 = self.conv.convert(div)
			batball.append(json1['div'])
		bat = batball[:2]
		bow = [batball[2]]
		return ('Bowler : ' + str(bow[0]['div'][0]['a']['text']) + 
		'\nOvers : ' + str(bow[0]['div'][1]['text']) + 
		'\nRuns : '+str(bow[0]['div'][3]['text'])+ 
		'\nWickets : ' + str(bow[0]['div'][4]['text']))

	def Update_Innings_stats(self):
		

		curr_team123 = self.conv.convert(self.soup.find('div', attrs={'id':'innings_2'}))
		x = str(curr_team123['div']['div'][0]['div'][0]['span'][0]['text'])
		curr_bat_name = x.replace(' Innings','')

		rows = len(curr_team123['div']['div'][0]['div']) - 2

		for j in range(2,rows):

			temp = curr_team123['div']['div'][0]['div'][j]['div'][0]
			
			if temp.get('a',-1)!=-1:
				name = curr_team123['div']['div'][0]['div'][j]['div'][0]['a']['text']
				# print(name)
				name = name.replace(" (c)","")
				name = name.replace(" (wk)","")
				
				dic = {}
				for i in range(2,7):
					dic[curr_team123['div']['div'][0]['div'][1]['div'][i-1]['text']] = curr_team123['div']['div'][0]['div'][j]['div'][i]['text']

				self.Inning[curr_bat_name].Batsman[name] = dic

			else:
				break
		
		
		rows = len(curr_team123['div']['div'][3]['div'])
		curr_bowl_name = self.team1
		if curr_bat_name == self.team1:
			curr_bowl_name = self.team2



		for j in range(1,rows):
			
			name = curr_team123['div']['div'][3]['div'][j]['div'][0]['a']['text']
			name = name.replace(" (c)","")
			name = name.replace(" (wk)","")
			
			dic = {}
			for i in range(1,8):
				dic[curr_team123['div']['div'][3]['div'][0]['div'][i]['text']] = curr_team123['div']['div'][3]['div'][j]['div'][i]['text']
			self.Inning[curr_bowl_name].Bowler[name] = dic

		for i in self.Inning[curr_bat_name].Batsman:
			r = int(self.Inning[curr_bat_name].Batsman[i]['R'])
			r += r//50
			self.Team[curr_bat_name][i] = r 
			
		for i in self.Inning[curr_bowl_name].Bowler:
			r = int(self.Inning[curr_bowl_name].Bowler[i]['W'])
			r = r*20
			self.Team[curr_bowl_name][i] = r




		curr_team123 = self.conv.convert(self.soup.find('div', attrs={'id':'innings_1'}))
		x = str(curr_team123['div']['div'][0]['div'][0]['span'][0]['text'])
		curr_bat_name = x.replace(' Innings','')

		rows = len(curr_team123['div']['div'][0]['div']) - 3
		for j in range(2,rows):

			name = curr_team123['div']['div'][0]['div'][j]['div'][0]['a']['text']
			name = name.replace(" (c)","")
			name = name.replace(" (wk)","")
			
			dic = {}
			for i in range(2,7):
				dic[curr_team123['div']['div'][0]['div'][1]['div'][i-1]['text']] = curr_team123['div']['div'][0]['div'][j]['div'][i]['text']

			self.Inning[curr_bat_name].Batsman[name] = dic

		
		rows = len(curr_team123['div']['div'][3]['div'])
		curr_bowl_name = self.team1
		if curr_bat_name == self.team1:
			curr_bowl_name = self.team2



		for j in range(1,rows):
			
			name = curr_team123['div']['div'][3]['div'][j]['div'][0]['a']['text']
			name = name.replace(" (c)","")
			name = name.replace(" (wk)","")
			
			dic = {}
			for i in range(1,8):
				dic[curr_team123['div']['div'][3]['div'][0]['div'][i]['text']] = curr_team123['div']['div'][3]['div'][j]['div'][i]['text']
			self.Inning[curr_bowl_name].Bowler[name] = dic

		for i in self.Inning[curr_bat_name].Batsman:
			r = int(self.Inning[curr_bat_name].Batsman[i]['R'])
			r += r//50
			self.Team[curr_bat_name][i] = r 
			
		for i in self.Inning[curr_bowl_name].Bowler:
			r = int(self.Inning[curr_bowl_name].Bowler[i]['W'])
			r = r*20
			self.Team[curr_bowl_name][i] = r





	def Update(self):
		# print(self.get_curr_team_score())
		# print(self.get_playing_bats())
		# print(self.get_playing_bowl())
		self.Update_Innings_stats()
		
		# print(self.pretty_print(self.Inning[self.team1].Batsman))
		# print(self.pretty_print(self.Inning[self.team1].Bowler))
		# print(self.pretty_print(self.Inning[self.team2].Batsman))
		# print(self.pretty_print(self.Inning[self.team2].Bowler))
		# self.print_fantasy_points()

	def get_score_board(self):
		a = self.pretty_print(self.Inning[self.team1].Batsman)
		b = self.pretty_print(self.Inning[self.team1].Bowler)
		c = self.pretty_print(self.Inning[self.team2].Batsman)
		d = self.pretty_print(self.Inning[self.team2].Bowler)
		return a + "\n" + b + "\n" + c + "\n" + d

	def pretty_print(self,dic):
		
		final = ""
		final += " "*29 
		if len(dic)>0:
			for i in dic:
				temp = ""
				for j in dic[i]:
					temp += j + " "*(5-len(j))  
				final += temp
				break
		final += "\n"	
		for i in dic:
			final += i + " "*(30-len(i))
			temp = ""
			for j in dic[i]:
				temp  += dic[i][j] + " "*(5-len(dic[i][j])) 
			final += temp + '\n'

		return final

	def print_fantasy_points(self):
		print()
		for i in self.Team:
			print(i,end=" "*(30-(len(i))))
			print()
			print()
			print("Player Name",end=" "*18)
			print("Points")
			for j in self.Team[i]:
				print(j,end = " "*(30-len(j)))
				print(self.Team[i][j], end=" "*(6-len(str(self.Team[i][j]))) )
				print()
			print()


class Records:
	def __init__(self):
		
		self.Matches = []
		links = open('Completed.txt','r')
		for i in links.readlines():
			url_comm , url = i.split()
			cric = Match(url_comm, url)
			cric.get_playing_11()
			cric.Update()
			self.Matches.append(cric)
	
# print(score_board)


