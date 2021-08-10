from django.shortcuts import render
from django.http import HttpResponse
from helper_score import Records
# Create your views here.
records = Records()
def home(request):
    context = {'matches': records.Matches}
    return render(request, 'Goti_Score/home.html',context)

def score_card(request,pk):
    

    
    match_selected = records.Matches[pk]
    score_board = match_selected.get_score_board()
    context = {
        'posts' : [
                    [match_selected.Inning[match_selected.team1].Batsman,
                    match_selected.Inning[match_selected.team2].Bowler] 
                    ,
                    [match_selected.Inning[match_selected.team2].Batsman,
                     match_selected.Inning[match_selected.team1].Bowler]
        ] 
    }
#   cric.Inning[cric.team1].Bowler,
#                     
    return render(request, 'Goti_Score/ScoreBoardTable.html',context)
