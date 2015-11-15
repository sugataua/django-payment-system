# Create your views here.

#from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render_to_response, HttpResponseRedirect, HttpResponse
from django.http import HttpResponseNotFound
from Wallet import forms
from Wallet import models
from django.contrib.auth.models import User
import datetime
from django.core.context_processors import csrf
from django.template import RequestContext
from django.core.mail import send_mail
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import random
import string
import hashlib


def clientRegistrationForm(request):
    c = {}
    c.update(csrf(request))
    if request.method == 'POST':
        form = forms.ClientRegistrationForm(request.POST)
        if form.is_valid():
            cdata = form.cleaned_data
            p = models.Client(name = cdata['name'],
                              surname = cdata['surname'],
                              email = cdata['email'],
                              date_of_birth = cdata['date_of_birth'],
                              password = cdata['password'],
                              phone_number = cdata['phone_number']
            )
            p.save();
            print p.id
            print 'Data catched'
            """
            send_mail(
                'Confirm registration',
                'Hello. There is your code:',
                'sg.korvin@gmail.com',
                [cdata['email']]
                )
            """
            user_wallet = models.Wallet(
                balance = 0,
                date_opened = datetime.datetime.now(),
                pay_limit = 0
            )
            user_wallet.save()
            p.client_wallet = models.Wallet.objects.get(id=user_wallet.id)
            p.save()
            return HttpResponseRedirect('/ok/')
        else:
            print 'Not valid'
            return render_to_response('registration.html', {'form': form})
    else:
        form = forms.ClientRegistrationForm()
        return render_to_response('registration.html', {'form': form},c)


def ok(request):
    return HttpResponse("Ok!")

def nuts(request):
    return HttpResponse('<img src="http://img0.liveinternet.ru/images/attach/c/0//63/368/63368916_729448a49cd1.jpg"/>')


def loginForm(request):
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            print 'Data catched'
            return HttpResponseRedirect('/ok/')
        else:
            print 'Not valid'
            return render_to_response('login.html', {'form': form})
    else:
        form = forms.LoginForm()
        return render_to_response('login.html', {'form': form})


def userslist(request):
    p1 = models.Client.objects.all()
    print p1
    return render_to_response('userslist.html',{'item_list': p1})


def wallets_list(request):
    p1 = models.Wallet.objects.all()
    print p1
    return render_to_response('userslist.html',{'item_list': p1})


def register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/logout/")
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            print new_user.username
            return HttpResponseRedirect("/login/")
    else:
        form = UserCreationForm()
    return render_to_response("registration/register.html", {'form': form}, context_instance=RequestContext(request))
"""
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            return  HttpResponseRedirect("/logedin/")
"""
@login_required
def clientRegistration(request):
    if request.user.is_authenticated():
       # print(request.user.id)
        client = models.Client.objects.filter(user_id = request.user.id)

        if len(client) != 0:
            return HttpResponseRedirect('/')
        else:
            if request.method == 'POST':
                form = forms.ClientRegistration(request.POST)
                if form.is_valid():
                    user_wallet = models.Wallet(
                        balance = 0,
                        number = "no activation",
                        date_opened = datetime.datetime.now(),
                        pay_limit = 0
                    )
                    user_wallet.save()
                    user_wallet.number = "2000" + str(user_wallet.id) + str(random.randint(0,1000))
                    cdata = form.cleaned_data
                    user = User.objects.get(id=request.user.id)
                    user.email = cdata['email']
                    user.save()
                    new_client = models.Client(name = cdata['name'],
                                      surname = cdata['surname'],
                                      date_of_birth = cdata['date_of_birth'],
                                      phone_number = cdata['phone_number'],
                                      user_id = user,
                                      client_wallet = user_wallet
                    )
                    new_client.save()
                    #new_user = form.save()
                    ehash = hashlib.md5()
                    ehash.update(user.email)
                    print(ehash.hexdigest())
                    """
                  link_code =  'Hello. There is your code: http://127.0.0.1:8000/confirm' + ehash.hexdigest()
                  send_mail('Confirm email',
                          link_code,
                          'sg.korvin@gmail.com',
                          [cdata['email']]
                   )
                   """

                    print new_client.name
                    return HttpResponseRedirect('/ok/')
                    #return HttpResponseRedirect("/")
            else:
                form = forms.ClientRegistration()
            return render_to_response("registration/register.html",{'form': form,},context_instance=RequestContext(request))


def mainpage(request):

    if request.user.is_authenticated():
       # request.
        print(request.user.id)
        client = models.Client.objects.filter(user_id = request.user.id)

        if len(client) == 0:
            return HttpResponseRedirect('/registration/')
        else:
            trans_list = models.Transaction.objects.filter(Q(from_user = client)| Q(to_wallet = client[0].client_wallet)).order_by('-end_time')[0:3]
        # if request.method == 'POST':
        #     form = forms.AddMoney(request.POST)
        #     if form.is_valid():
        #         client[0].client_wallet.balance += form.cleaned_data['money']
        #         client[0].client_wallet.save()
        #         new_trans = models.Transaction(
        #             title = "bonus",
        #             from_user = client[0],
        #             to_wallet = client[0].client_wallet,
        #             money = form.cleaned_data['money'],
        #             start_time = datetime.datetime.now(),
        #             end_time = datetime.datetime.now(),
        #             )
        #         new_trans.save()
        #         #account.save()
        #         return HttpResponseRedirect('/nuts/')
        # else:
        #     form = forms.AddMoney()


    else:
        return HttpResponseRedirect('/login/')
    return render_to_response('mainpage.html',{'user_name':request.user.username,
                                               'balance':str(client[0].client_wallet.balance),
                                               #'form':form,
                                               'item_list':trans_list,
                                               'account_number':client[0].client_wallet.number},
                              context_instance=RequestContext(request))
# @login_required
# def money_transfer(request):
#     if request.method == 'POST':
#         form = forms.MoneyTransaction(request.POST)
#         if form.is_valid():
#             cdata = form.cleaned_data
#
#             current_client = models.Client.objects.get(user_id = request.user)
#             print cdata['money']
#             print current_client.client_wallet.balance
#             dest_wallet = models.Wallet.objects.get(number = cdata['account_number'])
#
#             if cdata['money'] <= current_client.client_wallet.balance:
#                 new_trans = models.Transaction(
#                     title = "transfer",
#                     from_user = models.Client.objects.get(user_id = request.user),
#                     to_wallet = cdata['to_wallet'], #= dest_wallet.id
#                     money = cdata['money'],
#                     start_time = datetime.datetime.now(),
#                 )
#                 if new_trans.from_user.client_wallet == new_trans.to_wallet:
#                     return render_to_response("transfer_money.html",{'form': form,},context_instance=RequestContext(request))
#                 new_trans.save()
#
#                 new_confirm = models.Confirmation(
#                     title = "transfer",
#                     client = new_trans.from_user,
#                     transaction = new_trans,
#                     confirm_code =''.join(random.choice(string.digits) for x in range(6)),
#                     conf_date = datetime.datetime.now(),
#                     confirmed = False
#                 )
#                 new_confirm.save()
#                 print(new_confirm.confirm_code)
#                 # next operations after confirmation!
#                 """
#                 new_trans.from_user.client_wallet.balance -= new_trans.money
#                 new_trans.from_user.client_wallet.save()
#                 print new_trans.to_wallet_id
#                 new_trans.to_wallet.balance += new_trans.money
#                 new_trans.to_wallet.save()
#                 new_trans.end_time = datetime.datetime.now()
#                 new_trans.save()
#                 #new_user = form.save()
#                 """
#
#                 return HttpResponseRedirect('/confirm/')
#                 #return HttpResponseRedirect("/")
#             else:
#                 error_text = 'You cannot transfer bore money then you have! Your balance:' + str(current_client.client_wallet.balance)
#                 return render_to_response("transfer_money.html",{'form': form, 'error_text': error_text}, context_instance=RequestContext(request))
#     else:
#         form = forms.MoneyTransaction()
#     return render_to_response("transfer_money.html",{'form': form,},context_instance=RequestContext(request))



@login_required
def money_transfer(request):
    if request.method == 'POST':
        form = forms.MoneyTransfer(request.POST)
        if form.is_valid():
            cdata = form.cleaned_data

            current_client = models.Client.objects.get(user_id = request.user)
            print cdata['amount']
            print current_client.client_wallet.balance
            dest_wallet = models.Wallet.objects.get(number = cdata['account_number'])

            if cdata['amount'] <= current_client.client_wallet.balance:
                new_trans = models.Transaction(
                    title = "transfer",
                    from_user = models.Client.objects.get(user_id = request.user),
                    to_wallet = dest_wallet,
                    money = cdata['amount'],
                    start_time = datetime.datetime.now(),
                    #message = cdata['message']
                    )
                if new_trans.from_user.client_wallet == new_trans.to_wallet:
                    return render_to_response("transfer_money.html",{'form': form,},context_instance=RequestContext(request))
                new_trans.save()

                new_confirm = models.Confirmation(
                    title = "transfer",
                    client = new_trans.from_user,
                    transaction = new_trans,
                    confirm_code =''.join(random.choice(string.digits) for x in range(6)),
                    conf_date = datetime.datetime.now(),
                    confirmed = False
                )
                new_confirm.save()
                print(new_confirm.confirm_code)
                # next operations after confirmation!
                """
                new_trans.from_user.client_wallet.balance -= new_trans.money
                new_trans.from_user.client_wallet.save()
                print new_trans.to_wallet_id
                new_trans.to_wallet.balance += new_trans.money
                new_trans.to_wallet.save()
                new_trans.end_time = datetime.datetime.now()
                new_trans.save()
                #new_user = form.save()
                """

                return HttpResponseRedirect('/confirm/')
                #return HttpResponseRedirect("/")
            else:
                error_text = 'You can not transfer more money then you have!'
                balance = 'Your balance: ' + str(current_client.client_wallet.balance)
                return render_to_response("transfer_money.html",{'form': form,
                                                                 'error_text': error_text,
                                                                 'balance': balance}, context_instance=RequestContext(request))
    else:
        form = forms.MoneyTransfer()
    return render_to_response("transfer_money.html",{'form': form,},context_instance=RequestContext(request))





@login_required
def bonus(request):
    client = models.Client.objects.filter(user_id = request.user.id)
    if request.method == 'POST':
        form = forms.AddMoney(request.POST)
        if form.is_valid():
            account = client[0].client_wallet
            print("acc before ",  account.balance)
            account.balance += form.cleaned_data['money']
            account.save()
            print("acc after ",  account.balance)
            #client[0].save()
            new_trans = models.Transaction(
                title = "bonus",
                from_user = client[0],
                to_wallet = client[0].client_wallet,
                money = form.cleaned_data['money'],
                start_time = datetime.datetime.now(),
                end_time = datetime.datetime.now(),
                )
            new_trans.save()
            #account.save()
            return HttpResponseRedirect('/')
    else:
        form = forms.AddMoney()
    return render_to_response('bonus.html',{          'form':form,
                                                      'page_title':'Bonus page',
                                                      'form_title':'Take bonus'},
                              context_instance=RequestContext(request))

@login_required
def confirm(request):
    active_client = models.Client.objects.filter(user_id = request.user.id)
    active_transactions = models.Transaction.objects.filter(from_user = active_client, end_time = None).order_by("-start_time")
    if len(active_transactions) == 0:
        return HttpResponseNotFound('Page not found')
    active_trans = active_transactions[0]
    if request.method == 'POST':
        form = forms.ConfirmForm(request.POST)
        if form.is_valid():
            active_confirm = models.Confirmation.objects.get(client = active_client, confirmed = False)
            if active_confirm.confirm_code == form.cleaned_data['code']:
                 active_trans.from_user.client_wallet.balance -= active_trans.money
                 active_trans.from_user.client_wallet.save()
                 print active_trans.to_wallet_id
                 active_trans.to_wallet.balance += active_trans.money
                 active_trans.to_wallet.save()
                 active_trans.end_time = datetime.datetime.now()
                 active_trans.save()
                 active_confirm.confirmed = True
                 active_confirm.save()



            """
            client[0].client_wallet.balance += form.cleaned_data['money']
            client[0].client_wallet.save()
            new_trans = models.Transaction(
                title = "bonus",
                from_user = client[0],
                to_wallet = client[0].client_wallet,
                money = form.cleaned_data['money'],
                start_time = datetime.datetime.now(),
                end_time = datetime.datetime.now(),
                )
            new_trans.save()
            #account.save()
            """
            return HttpResponseRedirect('/')
    else:
        form = forms.ConfirmForm()
    return render_to_response('bonus.html',{'form':form,
                                            'traa': active_trans,
                                            'page_title':'Confirmation page',
                                            'form_title':'Confirm transaction'},
                              context_instance=RequestContext(request))

@login_required
def email_confirm(request, confirm_code):
    ehash = hashlib.md5()
    ehash.update(request.user.email)
    if confirm_code == ehash.hexdigest():
        active_client = models.Client.objects.get(user_id = request.user.id)
        if active_client.email_verified == True:
            return HttpResponse("Email has been activated already")
        active_client.email_verified = True
        active_client.save()
        active_client.client_wallet.number = "2000" + str(active_client.client_wallet.id) + str(random.randint(0,1000))
        active_client.client_wallet.save()
    else:
        return HttpResponseNotFound()
    return HttpResponseRedirect('/ok/')
#32d52fd2983dadbbced6f75f474f8461