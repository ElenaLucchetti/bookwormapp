from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from Bookworm.models import *
from Bookworm.forms import *
from Bookworm.bing_search import run_query
from django.shortcuts import render_to_response


# Create your views here.

def encode_url(str):
    return str.replace(' ', '_')

def get_book_list(max_results=0, starts_with=''):
    book_list = []
    if starts_with:
        book_list = Book.objects.filter(name__startswith=starts_with)
    else:
        book_list = Book.objects.all()

    if max_results > 0:
        if (len(book_list) > max_results):
            book_list = book_list[:max_results]

    for book in book_list:
        book.url = encode_url(book.title)

    return book_list

def home(request):
    context_dict = {}
    context_dict['genres'] = Genre.objects.order_by('genre_name')
    context_dict['popular'] = Book.objects.order_by('rate__rating')
    response = render(request, 'Bookworm/home.html', context=context_dict)

    return response

def show_book(request):
    context_dict = {}

    return render(request, 'Bookworm/book.html', context=context_dict)

def show_genre(request):
    context_dict = {}
    return render(request, 'Bookworm/genres.html',context=context_dict)

def search_results(request):
    context_dict = {}
    return render(request, 'Bookworm/searchresults.html',context=context_dict)

def userpage(request):
    context_dict = {}
    return render(request, 'Bookworm/userprofile.html',context=context_dict)

def recommendations(request):
    context_dict = {}
    return render(request, 'Bookworm/recommendations.html',context=context_dict)

def base(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('base'))
            else:
                return HttpResponse("Your Bookworm account is disabled.")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'Bookworm/base.html', {})

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

def search(request):
    context = RequestContext(request)

    book_list = get_book_list()
    context_dict = {}
    context_dict['book_list'] = book_list

    result_list = []

    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            # Run our Bing function to get the results list!
            result_list = run_query(query)

    context_dict['result_list'] = result_list
    return render_to_response('rango/search.html', context_dict, context)