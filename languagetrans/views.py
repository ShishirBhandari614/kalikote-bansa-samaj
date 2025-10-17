from django.shortcuts import render
import json
from django.http import JsonResponse
from bs4 import BeautifulSoup, Comment
from langdetect import detect
from googletrans import Translator

translator = Translator()

def translate_page(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=400)

    try:
        data = json.loads(request.body)
        html_content = data.get("html", "")
        target_lang = request.GET.get("lang", "en")

        print("Received HTML content (first 100 chars):", html_content[:100])
        print("Target language:", target_lang)

        if not html_content:
            print("No HTML content received.")
            return JsonResponse({"error": "No HTML content provided"}, status=400)

        soup = BeautifulSoup(html_content, "html.parser")

# Extract visible text nodes directly from the soup, ignoring scripts/styles/comments
        text_nodes = []
        original_texts = []

        for element in soup.find_all(string=True):
            if element.parent.name in ["script", "style", "meta", "title", "head", "link"]:
                continue
            if isinstance(element, Comment):
                continue
            stripped = element.strip()
            if stripped:
                text_nodes.append(element)
                original_texts.append(stripped)

        print("Original texts before filtering:", original_texts)

        if not original_texts:
            print("No translatable text found.")
            return JsonResponse({"translated_html": str(soup)})

        translated_texts = []
        for text in original_texts:
            try:
                # Detect language of this text
                src_lang = detect(text)
                print(f"Detected language for '{text}': {src_lang}")

                # Translate only if source language differs from target
                if src_lang != target_lang:
                    translated = translator.translate(text, dest=target_lang).text
                    print(f"Translated '{text}' -> '{translated}'")
                    translated_texts.append(translated)
                else:
                    print(f"No translation needed for '{text}'")
                    translated_texts.append(text)
            except Exception as e:
                print(f"Translation failed for text '{text}': {e}")
                translated_texts.append(text)

        # Replace text nodes with translations
        for node, translated in zip(text_nodes, translated_texts):
            print(f"Replacing '{node}' with '{translated}'")
            node.replace_with(translated)

        translated_html = str(soup)
        print("Translated HTML content (first 100 chars):", translated_html[:100])

        return JsonResponse({"translated_html": translated_html})

    except Exception as e:
        print("Error in translation view:", e)
        return JsonResponse({"error": str(e)}, status=500)


def home(request):
    return render(request, "home.html")