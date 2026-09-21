from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from animals.models import Animal
from tickets.models import Booking

from google import genai
from django.conf import settings

client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)

def visitor_home(request):

    total_animals = Animal.objects.count()

    context = {
        "total_animals": total_animals,
    }

    return render(
        request,
        "visitors/home.html",
        context
    )
def animal_gallery(request):

    search = request.GET.get("search", "")
    category = request.GET.get("category", "")

    animals = Animal.objects.all()

    # Search
    if search:
        animals = animals.filter(
            name__icontains=search
        ) | animals.filter(
            species__icontains=search
        ) | animals.filter(
            category__icontains=search
        )

    # Category filter
    if category:
        animals = animals.filter(
            category=category
        )

    categories = Animal.objects.values_list(
        "category",
        flat=True
    ).distinct()

    context = {
        "animals": animals,
        "search": search,
        "category": category,
        "categories": categories,
    }

    return render(
        request,
        "visitors/animal_gallery.html",
        context
    )
def animal_detail(request, animal_id):

    animal = get_object_or_404(
        Animal,
        id=animal_id
    )

    context = {
        "animal": animal,
    }

    return render(
        request,
        "visitors/animal_detail.html",
        context
    )

@require_POST
def chatbot(request):

    message = request.POST.get("message", "").strip()

    if not message:
        return JsonResponse({
            "reply": "Please enter a question."
        })


    # Get all animals currently in the database

    animals = Animal.objects.all()


    # Find animals mentioned in the visitor's question

    found_animals = []

    message_lower = message.lower()

    for animal in animals:

        animal_name = (animal.name or "").lower()
        species_name = (animal.species or "").lower()
        scientific_name = (animal.scientific_name or "").lower()

        # Check the complete name/species
        if (
            animal_name in message_lower
            or species_name in message_lower
            or scientific_name in message_lower
        ):
            found_animals.append(animal)
            continue

        # Check individual words in the species
        species_words = (
            species_name
            .replace("-", " ")
            .split()
        )

        for word in species_words:

            if len(word) >= 3 and word in message_lower:
                found_animals.append(animal)
                break


    # Check if the visitor is asking about tickets

    ticket_keywords = [
        "ticket",
        "tickets",
        "booking",
        "book",
        "price",
        "cost",
        "adult",
        "child",
        "children",
        "entry fee",
        "admission",
        "visit"
    ]

    is_ticket_question = any(
        keyword in message_lower
        for keyword in ticket_keywords
    )

    if is_ticket_question:

        ticket_information = """
Adult Ticket Price: ₹200
Child Ticket Price: ₹100

Booking process:
1. Visitor must be logged in.
2. Visitor selects the visit date.
3. Visitor selects the number of adult tickets.
4. Visitor selects the number of child tickets.
5. The total amount is calculated.
6. Visitor proceeds to the payment page.
7. After payment, the booking is created.
"""

        prompt = f"""
You are the friendly AI assistant for our zoo.

The visitor asked:
"{message}"

Here is the official ticket information from our zoo system:

{ticket_information}

Answer the visitor's question naturally and conversationally.

IMPORTANT RULES:
- Use only the ticket information provided above.
- Do not invent ticket prices, discounts, opening hours, or other booking information.
- If the visitor asks something that the provided information does not answer, clearly say that the information is not available.
- Explain the information in simple, natural sentences.
- Keep the answer concise and friendly.
"""

        try:

            response = client.interactions.create(
                model="gemini-3.6-flash",
                input=prompt
            )

            return JsonResponse({
                "reply": response.output_text
            })

        except Exception as e:

            print("Gemini error:", e)

            return JsonResponse({
                "reply":
                    "Sorry, I'm having trouble connecting "
                    "to the AI assistant right now."
            })

    
    # If an animal was found, give its information to Gemini

    if found_animals:

        animal = found_animals[0]

        animal_information = f"""
Animal Name: {animal.name}
Species: {animal.species}
Scientific Name: {animal.scientific_name or "Not available"}
Age: {animal.age} years
Habitat: {animal.habitat}
Category: {animal.category or "Not available"}
Diet: {animal.diet or "Not available"}
Health Status: {animal.health_status}
Description: {animal.description or "Not available"}
"""


        prompt = f"""
You are the friendly AI assistant for our zoo.

The visitor asked:
"{message}"

Here is the information about the animal from our zoo database:

{animal_information}

Answer the visitor's question naturally and conversationally.

IMPORTANT RULES:
- Use only the information provided above.
- Do not invent facts about the animal.
- Do not make up information that is not in the database.
- If the visitor asks something that the database information does not answer, clearly say that the information is not available.
- Do not simply list the database fields.
- Turn the information into natural, easy-to-read sentences.
- Keep the answer concise and friendly.
- You may use the animal's name naturally in the response.
"""


        try:

            response = client.interactions.create(
                model="gemini-3.6-flash",
                input=prompt
            )

            return JsonResponse({
                "reply": response.output_text
            })


        except Exception as e:

            print("Gemini error:", e)

            return JsonResponse({
                "reply":
                    "Sorry, I'm having trouble connecting "
                    "to the AI assistant right now."
            })

     # Check if the visitor is asking about the zoo
    
        zoo_keywords = [
            "zoo",
            "about",
            "animal care",
            "care",
            "staff",
            "visitor",
            "visitors",
            "facilities",
            "management"
        ]
    
        is_zoo_question = any(
            keyword in message_lower
            for keyword in zoo_keywords
        )
    
        if is_zoo_question:
    
            zoo_information = f"""
    Our zoo currently has {animals.count()} animals registered in the system.
    
    The zoo management system handles:
    - Animal information
    - Animal health records
    - Feeding schedules
    - Staff management
    - Ticket booking
    - Visitor feedback
    
    The system also includes an AI assistant to help visitors with:
    - Animal-related questions
    - Zoo-related questions
    - Ticket booking information
    """
    
            prompt = f"""
    You are the friendly AI assistant for our zoo.
    
    The visitor asked:
    "{message}"
    
    Here is the official zoo information available in our system:
    
    {zoo_information}
    
    Answer the visitor's question naturally and conversationally.
    
    IMPORTANT RULES:
    - Use only the zoo information provided above.
    - Do not invent opening hours, location, contact details, ticket discounts, facilities, or services that are not listed.
    - If the visitor asks something that is not available in the provided information, clearly say that the information is not available.
    - Keep the answer simple, concise, and friendly.
    """
    
            try:
    
                response = client.interactions.create(
                    model="gemini-3.6-flash",
                    input=prompt
                )
    
                return JsonResponse({
                    "reply": response.output_text
                })
    
            except Exception as e:
    
                print("Gemini error:", e)
    
                return JsonResponse({
                    "reply":
                        "Sorry, I'm having trouble connecting "
                        "to the AI assistant right now."
                })
            
    # No animal was found

    return JsonResponse({
        "reply":
            "🦁 I couldn't find an animal matching your question "
            "in our zoo database. Please check the animal's name "
            "and try again."
    })