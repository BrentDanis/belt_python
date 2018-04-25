from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
	# Nailed it !! Stay positive
	return render(request, 'belt_practice_app/index.html')

def register(request):
    # Got another small win
    results = User.objects.basic_validator(request.POST)
    if results['status']:
        request.session['id']= results['newUser'].id
        return redirect('/success')
    else:
        for tag, error in results['errors'].items():
            messages.error(request, error)
        return redirect('/')
    return redirect('/')

def login(request):
    results = User.objects.login_validator(request.POST)
    if results['status']:
        request.session['id'] = results['user'].id
    else:
        for tag, error in results['errors'].items():
            messages.error(request, error)
        return redirect('/')
    return redirect('/success')


# ************** Registration and Login is ^ above this line *****************

# ************** Quotes and Likes below this line ****************************


def success(request):
    our_id = request.session['id']
    user = User.objects.filter(id = our_id)
    client = user[0]
    print(client.first_name)
    like = Quote.objects.filter(faved_by = our_id)
    drop = Quote.objects.exclude(faved_by = our_id)
    context = {
        "quotes": drop,
        "fave_quotes": like,
        "name": client.first_name
    }
    return render(request, 'belt_practice_app/success.html', context)

def show_user(request, id):
	#print "\n##################\n" hit show user "\n##################\n"
    if 'id' not in request.session:
        return redirect('/')
    else:
        quotes = Quote.objects.filter(posted_by = id)
        #count = Quotes.objects.filter(id=user.id) AAAAHHHHHHH!!!!!! Fuck!!!
        #print(quotes) <-- got that to show
        context = {
            'user': User.objects.get(id = id),
            'quotes': quotes
        }

        return render(request, 'belt_practice_app/user.html', context)
#user to input here
def user_create(request):
	#print "############## we hit user create ###########"
    if 'id' not in request.session:
        return redirect('/')
    else:
        user = User.objects.get(id = request.session['id'])
        id = user.id
        quote = Quote.objects.quote_validator(id, request.POST)
        if quote['status'] == False:
            for tag, error in quote['errors'].items():
                messages.error(request, error)
        return redirect('/success')

# here will use the favQuote to like the quote on front end
def like_btn(request):
    id = request.session['id']
    set = Quote.objects.faveQuote(id, request.POST)
    print(set)
    return redirect('/success')

#just like the fave and unfave
def drop_btn(request):
    id = request.session['id']
    unset = Quote.objects.unfaveQuote(id, request.POST)
    return redirect('/success')

def logout(request):
    request.session['id'] = None
    return redirect('/')

