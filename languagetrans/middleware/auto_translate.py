# # languagetrans/middleware/auto_translate.py
# from bs4 import BeautifulSoup
# from django.utils.deprecation import MiddlewareMixin
# from langdetect import detect
# from deep_translator import GoogleTranslator

# def batch_translate_texts(texts, target_lang):
#     if not texts:
#         return texts

#     try:
#         # Rough detection
#         current_lang = detect(" ".join(texts))
#         if current_lang == target_lang:
#             return texts

#         translator = GoogleTranslator(source='auto', target=target_lang)

#         try:
#             # First try batch
#             translated_texts = translator.translate_batch(texts)
#             print("Batch translation result:", translated_texts)

#             if isinstance(translated_texts, str):
#                 translated_texts = [translated_texts] * len(texts)

#             # If nothing changed, fallback to per-item translation
#             if translated_texts == texts:
#                 print("Batch translation failed, falling back to per-item.")
#                 translated_texts = [translator.translate(t) for t in texts]

#         except Exception as e:
#             print("Batch translation error:", e)
#             translated_texts = [translator.translate(t) for t in texts]

#         return translated_texts

#     except Exception as e:
#         print("Language detection/translation failed:", e)
#         return texts


# class AutoTranslateMiddleware(MiddlewareMixin):
#     def process_response(self, request, response):
#         if not response.get("Content-Type", "").startswith("text/html"):
#             return response

#         user_lang = request.session.get("preferred_lang", "en")
#         print("User language:", user_lang)

#         try:
#             soup = BeautifulSoup(response.content, "html.parser")

#             # Collect only visible text inside <body>
#             text_nodes = []
#             original_texts = []
#             for element in soup.body.find_all(string=True):
#                 if element.parent.name in ["script", "style", "meta", "title", "[document]"]:
#                     continue
#                 stripped = element.strip()
#                 if stripped:
#                     text_nodes.append(element)
#                     original_texts.append(stripped)

#             print("Original texts:", original_texts[:5])

#             translated_texts = batch_translate_texts(original_texts, user_lang)
#             print("Translated texts:", translated_texts[:5])

#             # Replace visible text with translation
#             for element, translated in zip(text_nodes, translated_texts):
#                 if translated:  # skip None
#                     element.replace_with(translated)

#             # Encode response as UTF-8
#             response.content = str(soup).encode("utf-8")
#             response["Content-Type"] = "text/html; charset=utf-8"

#         except Exception as e:
#             print("Translation middleware error:", e)

#         return response


# middleware/auto_translate.py
# from bs4 import BeautifulSoup
# from django.utils.deprecation import MiddlewareMixin
# from langdetect import detect
# from googletrans import Translator

# # Create a single Translator instance for reuse
# translator = Translator()


# def batch_translate_texts(texts, target_lang):
#     """
#     Translates a list of texts at once using googletrans.
#     Includes detection, batch translation, and fallback per-item translation.
#     """
#     if not texts:
#         return texts

#     try:
#         # Rough detection of current language
#         current_lang = detect(" ".join(texts))
#         print("Detected language:", current_lang)

#         # Skip if already in target language
#         if current_lang == target_lang:
#             return texts

#         try:
#             # Try batch translation first
#             translated = translator.translate(texts, src=current_lang, dest=target_lang)
#             print("Batch translation result (sample):", [t.text for t in translated[:5]])

#             # googletrans returns a list of Translated objects
#             if isinstance(translated, list):
#                 translated_texts = [t.text for t in translated]
#             else:
#                 translated_texts = [translated.text for _ in texts]

#             # If batch result same as input → fallback
#             if translated_texts == texts:
#                 print("Batch translation failed or same, falling back to per-item translation.")
#                 translated_texts = [translator.translate(t, src=current_lang, dest=target_lang).text for t in texts]

#         except Exception as e:
#             print("Batch translation error:", e)
#             # fallback: translate one by one
#             translated_texts = [translator.translate(t, src='auto', dest=target_lang).text for t in texts]

#         return translated_texts

#     except Exception as e:
#         print("Language detection/translation failed:", e)
#         return texts


# class AutoTranslateMiddleware(MiddlewareMixin):
#     def process_response(self, request, response):
#         # Only process HTML pages
#         if not response.get("Content-Type", "").startswith("text/html"):
#             return response

#         user_lang = request.session.get("preferred_lang", "en")
#         print("User language:", user_lang)

#         try:
#             soup = BeautifulSoup(response.content, "html.parser")

#             # Collect visible text nodes inside <body>
#             text_nodes = []
#             original_texts = []
#             if soup.body:
#                 for element in soup.body.find_all(string=True):
#                     if element.parent.name in ["script", "style", "meta", "title", "[document]"]:
#                         continue
#                     stripped = element.strip()
#                     if stripped:
#                         text_nodes.append(element)
#                         original_texts.append(stripped)

#             print("Original texts (sample):", original_texts[:5])

#             # Translate all visible text nodes
#             translated_texts = batch_translate_texts(original_texts, user_lang)
#             print("Translated texts (sample):", translated_texts[:5])

#             # Replace text nodes with translations
#             for element, translated in zip(text_nodes, translated_texts):
#                 if translated:
#                     element.replace_with(translated)

#             # Ensure correct encoding for Unicode output
#             response.content = str(soup).encode("utf-8")
#             response["Content-Type"] = "text/html; charset=utf-8"

#         except Exception as e:
#             print("Translation middleware error:", e)

#         return response

from bs4 import BeautifulSoup
from django.utils.deprecation import MiddlewareMixin
from langdetect import detect
from googletrans import Translator
import hashlib
import urllib.parse
import json

translator = Translator()

def batch_translate_texts(texts, target_lang):
    """
    Translates a list of texts at once using googletrans.
    Includes detection, batch translation, and fallback per-item translation.
    """
    if not texts:
        return texts

    try:
        # Detect current language
        current_lang = detect(" ".join(texts))
        print("Detected language:", current_lang)

        if current_lang == target_lang:
            return texts

        try:
            # Batch translation
            translated = translator.translate(texts, src=current_lang, dest=target_lang)
            if isinstance(translated, list):
                translated_texts = [t.text for t in translated]
            else:
                translated_texts = [translated.text for _ in texts]

            # Fallback per-item if identical
            if translated_texts == texts:
                translated_texts = [translator.translate(t, src=current_lang, dest=target_lang).text for t in texts]

        except Exception as e:
            print("Batch translation error:", e)
            translated_texts = [translator.translate(t, src='auto', dest=target_lang).text for t in texts]

        return translated_texts

    except Exception as e:
        print("Language detection/translation failed:", e)
        return texts


class AutoTranslateMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Skip non-200 responses
        if getattr(response, 'status_code', 200) != 200:
            return response

        content_type = response.get("Content-Type", "")
        # Only process HTML pages
        if not content_type.startswith("text/html"):
            return response

        # Skip static/media and common asset paths
        path = request.path or ""
        if (
            path.startswith("/static/") or
            path.startswith("/media/") or
            path.endswith(('.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.webp', '.mp4', '.mp3', '.woff', '.woff2', '.eot', '.ttf'))
        ):
            return response

        user_lang = request.session.get("preferred_lang", "en")
        default_lang = "en"

        # If user did not select another language → do nothing
        if user_lang == default_lang:
            return response

        # Create unique cache key for this page and language
        page_key = hashlib.md5(f"{request.path}_{user_lang}".encode()).hexdigest()
        cookie_key = f"translated_{page_key}"

        # Check if page translation is already stored in cookies
        cached_translation = request.COOKIES.get(cookie_key)
        if cached_translation:
            print(f"✅ Using cached translation for {request.path} [{user_lang}]")
            try:
                decoded_html = urllib.parse.unquote(cached_translation)
                response.content = decoded_html.encode("utf-8")
                response["Content-Type"] = "text/html; charset=utf-8"
                return response
            except Exception as e:
                print("Cookie decode failed:", e)

        print(f"🌐 Translating page: {request.path} → {user_lang}")

        try:
            soup = BeautifulSoup(response.content, "html.parser")

            # Collect text nodes
            text_nodes = []
            original_texts = []
            if soup.body:
                for element in soup.body.find_all(string=True):
                    if element.parent and element.parent.name in ["script", "style", "meta", "title", "[document]"]:
                        continue
                    stripped = element.strip()
                    if stripped:
                        text_nodes.append(element)
                        original_texts.append(stripped)
            else:
                return response

            # Translate texts
            translated_texts = batch_translate_texts(original_texts, user_lang)

            # Replace texts
            for element, translated in zip(text_nodes, translated_texts):
                if translated:
                    element.replace_with(translated)

            # Final HTML
            translated_html = str(soup)
            response.content = translated_html.encode("utf-8")
            response["Content-Type"] = "text/html; charset=utf-8"

            # Encode HTML for cookie (URL-safe)
            encoded_html = urllib.parse.quote(translated_html)

            # Store in cookie (expires when browser closes)
            response.set_cookie(cookie_key, encoded_html, httponly=False, samesite='Lax')

            print(f"✅ Page translated and cached under cookie key: {cookie_key}")

        except Exception as e:
            print("Translation middleware error:", e)

        return response
