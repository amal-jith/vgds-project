import json
from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse
from django.core.paginator import Paginator

from django.shortcuts import render
from .models import FAQ, Testimonials, Order, Work
from django.core.files.base import ContentFile


# Create your views here.


def home(request):

    faqs = FAQ.objects.all()[:5]

    context = {
        "faqs":faqs,
    }

    return render(request, "home.html", context)

def ourWorks(request):

    works = Work.objects.all()

    context = {
        "works": works,
    }
    return render(request, "our-works.html", context)

def faq_list(request):
    page = int(request.GET.get('page', 1))
    per_page = 5
    faqs = FAQ.objects.all()
    paginator = Paginator(faqs, per_page)

    if page > paginator.num_pages:
        return JsonResponse({'faqs': [], 'has_next': False})

    current_page = paginator.page(page)
    data = [
        {
            'question': faq.question,
            'answer': faq.answer,
        }
        for faq in current_page
    ]

    return JsonResponse({'faqs': data, 'has_next': current_page.has_next()})

def services(request):
    return render(request, "services.html")

def presentation_design(request):

    faqs = FAQ.objects.all()[:5]

    context = {
        "faqs": faqs,
    }

    return render(request, "presentation-design.html", context)

def graphics(request):

    faqs = FAQ.objects.all()[:5]

    context = {
        "faqs": faqs,
    }

    return render(request, "graphics.html", context)

def otherServices(request):

    faqs = FAQ.objects.all()[:5]

    context = {
        "faqs": faqs,
    }

    return render(request, "other-services.html", context)


def solutions(request):
    return render(request, "solutions.html")

def testimonials(request):

    testimonials = Testimonials.objects.all()

    context = {
        "testimonials": testimonials
    }
    return render(request, "testimonials.html", context)

def pricing(request):
    return render(request, "pricing.html")

def orderFlow(request):
    return render(request, "order-flow.html")


@csrf_exempt
def submit_order(request):
    if request.method == "POST":
        try:
            # Get JSON application data
            application_data = json.loads(request.POST.get("application", "{}"))

            # Get individual sections
            treatment = application_data.get("treatment", {})
            style = application_data.get("style", {})
            delivery = application_data.get("delivery", {})
            filesDetails = application_data.get("filesDetails", {})
            payment = application_data.get("payment", {})

            # Create new Order object (adjust field names as per your model)
            order = Order.objects.create(
                treatment_name=treatment.get("name"),
                treatment_price=treatment.get("price"),

                style_name=style.get("name"),
                delivery_date=delivery.get("date"),
                delivery_rate=delivery.get("rate"),
                delivery_slides=delivery.get("slides"),
                delivery_option=delivery.get("option"),
                delivery_option_price=delivery.get("optionPrice"),
                estimated_price_range=delivery.get("estimatedText"),

                full_name=payment.get("fullName"),
                email=payment.get("email"),
                phone=payment.get("phone"),
                promo_code=payment.get("promoCode"),
                agreed_to_terms=payment.get("agreedToTerms"),
                marketing_opt_in=payment.get("receiveMarketingEmails"),
                google_link=filesDetails.get("textareaValue"),
                google_checkbox=filesDetails.get("checkboxChecked", False),
            )

            # Handle uploaded files
            style_file = request.FILES.get("style_file")
            if style_file:
                order.style_file.save(style_file.name, style_file)

            presentation_file = request.FILES.get("presentation_file")
            if presentation_file:
                order.presentation_file.save(presentation_file.name, presentation_file)

            order.save()

            return JsonResponse({"status": "success"})

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({"status": "invalid request"}, status=405)


















def orderNow(request):
    return render(request, "order-modal.html")

def order(request):
    return render(request, "order-now.html")