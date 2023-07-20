from django.shortcuts import render
from django.http import HttpResponse
from .models import rtbHighScore

# Create your views here.
def index(request):
    return render(request, 'index.html')


def rtbstart(request):
    if request.method == 'POST':
        playername = request.POST["playername"]
        request.session["playername"] = playername
        message = True
        context = {"playername" : playername, "message" : message}
        return render(request, 'rtbstart.html', context)
    else:
        return render(request, 'rtbstart.html')




global toGoFor
global runningTotal


toGoFor = 1
runningTotal = 0

def rtb(request):
    playername = request.session["playername"]
    
    
    if request.method == 'POST':
        
        numbHit = int(request.POST["numberHit"])
        global toGoFor
        global runningTotal
        score = numbHit * toGoFor
        runningTotal += score
        toGoFor += 1
        if toGoFor == 21:
            bulls = "Bulls"
            dict = { "toGoFor" : bulls, "runningTotal" : runningTotal, "playername" : playername }
        else:
            dict = { "toGoFor" : toGoFor, "runningTotal" : runningTotal, "playername" : playername }
        if toGoFor == 5:
            gameover = True
            dict = {"runningTotal" : runningTotal, "gameover" : gameover}
            newEntry = rtbHighScore(name = playername, score = runningTotal)
            newEntry.save()
            return render(request, "rtb.html", dict)
        else:
            dict = { "toGoFor" : toGoFor, "runningTotal" : runningTotal, "playername" : playername }
            return render(request, 'rtb.html', dict)
    else: 
        
        toGoFor = 1
        runningTotal = 0
        
        dict = { "toGoFor" : toGoFor, "runningTotal" : runningTotal, "playername" : playername }
        return render(request, 'rtb.html', dict)
    
def rtbover(request):
    
    dict = {"runningTotal" : runningTotal}
    return (request, "rtbover.html", dict)


def finishes(request):
    return render(request, 'finishes.html')

def highscores(request):
    return render(request, 'highscores.html', {"scores" : rtbHighScore.objects.all().order_by('-score').values()})



