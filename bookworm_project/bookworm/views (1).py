from bookworm.models import Book

def index(request):
    pop_book_list = Book.objects.order_by('-views')[:5] #or ratings??
    rec_book_list = Book.objects.order_by('-views')[:5] #or ratings
    context_dict = {'popular': pop_book_list, 'recommended': rec_book_list}

    context_dict['visits'] = request.session['visits']

    response = render(request, 'bookworm/index.html', context=context_dict)
    return response