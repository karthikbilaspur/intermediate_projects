from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..forms.forms import ImageUploadForm, DocumentForm
from ..model.models import UploadedImage, Document
import pytesseract
from PIL import Image
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from pdf2image import convert_from_path
from pdfkit import from_string
import fpdf

@login_required
def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = request.user
            image.save()
            img = Image.open(image.image)
            text = pytesseract.image_to_string(img)
            image.extracted_text = text
            image.save()
            return redirect('display_text', pk=image.pk)
    else:
        form = ImageUploadForm()
    return render(request, 'upload_image.html', {'form': form})

@login_required
def display_text(request, pk):
    image = UploadedImage.objects.get(pk=pk)
    return render(request, 'display_text.html', {'image': image})

@login_required
def edit_text(request, pk):
    image = UploadedImage.objects.get(pk=pk)
    if request.method == 'POST':
        form = DocumentForm(request.POST, instance=image)
        if form.is_valid():
            form.save()
            return redirect('display_text', pk=pk)
    else:
        form = DocumentForm(instance=image)
    return render(request, 'edit_text.html', {'form': form})

@login_required
def history(request):
    images = UploadedImage.objects.filter(user=request.user)
    return render(request, 'history.html', {'images': images})

@login_required
def download_pdf(request, pk):
    image = UploadedImage.objects.get(pk=pk)
    pdf = fpdf.FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=15)
    pdf.cell(200, 10, txt=image.extracted_text, ln=True, align='L')
    response = HttpResponse(pdf.output(dest='S').encode('latin-1'), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="document.pdf"'
    return response

@login_required
def create_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST)
        if form.is_valid():
            document = form.save(commit=False)
            document.user = request.user
            document.save()
            return redirect('history')
    else:
        form = DocumentForm()
    return render(request, 'create_document.html', {'form': form})