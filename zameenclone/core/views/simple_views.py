from django.http import JsonResponse
from ..models import AmenityOption

def get_amenity_options(request):
    amenity_id = request.GET.get('amenity_id')
    options = AmenityOption.objects.filter(amenity_id=amenity_id)
    options_html = '<option value="">Select Option</option>'
    for option in options:
        options_html += f'<option value="{option.id}">{option.option}</option>'
    return JsonResponse(options_html, safe=False)
