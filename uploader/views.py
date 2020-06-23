from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.views.generic import ListView, CreateView

from .models import Upload, Book
from .forms import BookForm


def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        # print(uploaded_file.name)
        # print(uploaded_file.size)
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
        print(context['url'])
    return render(request, 'uploader/upload.html', context)


def book_list(request):
    books = Book.objects.all()[::-1]
    return render(request, 'uploader/book_list.html', {'books': books})


def delete_book(request, pk):
    if request.method == 'POST':
        book = Book.objects.get(pk=pk)
        book.delete()
    return redirect('book_list')


def upload_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'uploader/upload_book.html', {'form': form})


class UploadView(CreateView):
    model = Upload
    fields = ['upload_file', ]
    success_url = reverse_lazy('fileupload')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['documents'] = Upload.objects.all()
        return context


class BookListView(ListView):
    model = Book
    template_name = 'uploader/class_book_list.html'
    context_object_name = 'books'


class UploadBookView(CreateView):
    model = Book
    form_class = BookForm
    # fields = ['title', 'author', 'pdf', 'cover']
    success_url = reverse_lazy('class_book_list')
    template_name = 'uploader/upload_book.html'
