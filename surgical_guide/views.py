from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from .forms import SurgicalGuideForm
from django.shortcuts import redirect
from xhtml2pdf import pisa
import io

# Create your views here.

# def surgical_guide(request):
#     if request.method == "POST":
#         form = SurgicalGuideForm(request.POST)

#         if form.is_valid():
#             form.save()
#             return redirect('surgical_guide')
#         else:
#             print(form.errors)
#     else:
#         form = SurgicalGuideForm()

#     return render(request, 'surgical_guide.html', {'form': form})

def surgical_guide(request):
    if request.method == "POST":
        form = SurgicalGuideForm(request.POST)

        if form.is_valid():
            instance = form.save()

            template = get_template('surgical_guide_pdf.html')
            html = template.render({'data': instance})

            result = io.BytesIO()
            pdf = pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), result)

            if not pdf.err:
                return HttpResponse(result.getvalue(), content_type='application/pdf')

            return HttpResponse("Error generating PDF", status=500)

    else:
        form = SurgicalGuideForm()

    return render(request, 'surgical_guide.html', {'form': form})