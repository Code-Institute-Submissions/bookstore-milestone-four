from django.shortcuts import render, get_object_or_404
from books.models import Books
from authors.models import Author
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponseRedirect
from reviews.forms import ReviewForm
from reviews.models import Review
# Create your views here.


def books(request):
    '''
    Return all books in collection
    Paginated to 6 books per page
    '''
    books = Books.objects.order_by("-list_date").filter(is_published=True)
    paginator = Paginator(books, 6)
    page = request.GET.get("page")
    paged_books = paginator.get_page(page)

    context = {"books": paged_books, "books_all": books}
    return render(request, "books/books.html", context)


def book(request, book_id):
    '''
    Returns the view for a single book
    '''
    book = get_object_or_404(Books, pk=book_id)
    reviews = Review.objects.filter(book_id=book_id).order_by("pub_date")
    authors = book.author
    author = Author.objects.all().filter(name=True)
    if request.method == "POST":
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    else:
        form = ReviewForm()
    context = {"book": book, "author": "author", "reviews": reviews, "form": form}
    return render(request, "books/book.html", context)


def search(request):
    '''
    Search function allowing the user to search by title, author, category
    '''
    queryset_list = Books.objects.order_by("-list_date")

    # Search by title
    if "title" in request.GET:
        title = request.GET["title"]
        if title:
            queryset_list = queryset_list.filter(title__icontains=title)

    # Search by author
    if "author" in request.GET:
        author = request.GET["author"]
        if author:
            queryset_list = queryset_list.filter(author__name__exact=author)

    # Search by category
    if "category_name" in request.GET:
        category_name = request.GET["category_name"]
        if category_name:
            queryset_list = queryset_list.filter(category_name__icontains=category_name)

    context = {"books": queryset_list, "values": request.GET}
    return render(request, "books/search.html", context)
