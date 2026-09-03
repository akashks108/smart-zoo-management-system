from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from animals.models import Animal

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


    # No animal was found

    return JsonResponse({
        "reply":
            "🦁 I couldn't find an animal matching your question "
            "in our zoo database. Please check the animal's name "
            "and try again."
    })