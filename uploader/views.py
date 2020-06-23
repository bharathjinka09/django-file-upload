from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.shortcuts import render

from .models import Upload


def upload(request):
	if request.method == 'POST':
		uploaded_file = request.FILES['document']
		print(uploaded_file.name)
		print(uploaded_file.size)
	return render(request, 'uploader/upload.html')

class UploadView(CreateView):
    model = Upload
    fields = ['upload_file', ]
    success_url = reverse_lazy('fileupload')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['documents'] = Upload.objects.all()
        return context
