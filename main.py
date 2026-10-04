import os
import base64
import requests
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("RODIUMAI_API_KEY")

BASE_URL = "https://api.rodiumai.io/v1"

CHAT_MODEL = "openai/gpt-4o"
IMAGE_MODEL = "openai/gpt-image-1"
VIDEO_MODEL = "google/veo-3.1"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}


def afficher_erreur(response):
    try:
        data = response.json()
        error = data.get("error", {})

        code = error.get("code", "unknown_error")
        message = error.get("message", "Erreur inconnue")

        print(f"Erreur RodiumAi")
        print(f"Code : {code}")
        print(f"Message : {message}")

    except Exception:
        print(f"Erreur HTTP : {response.status_code}")
        print(response.text)


def chat():
    while True:
        print("\n--- ETAPE 1 : CHAT ---")

        prompt = input("Votre question : ")

        data = {
            "model": CHAT_MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }

        try:
            response = requests.post(
                f"{BASE_URL}/chat/completions",
                headers=HEADERS,
                json=data,
                timeout=60
            )

            if response.status_code != 200:
                afficher_erreur(response)
                continue

            result = response.json()

            message = result["choices"][0]["message"]["content"]

            print("\nRéponse :")
            print(message)

            if "cost_rodi" in result:
                print(f"\nCoût : {result['cost_rodi']} RODI")

        except requests.RequestException as e:
            print(f"Erreur réseau : {e}")

        choix = input("\n[r] Répéter | [s] Suivant : ").lower()

        if choix == "s":
            return


def image():
    while True:
        print("\n--- ETAPE 2 : IMAGE ---")

        prompt = input("Description de l'image : ")

        data = {
            "model": "openai/gpt-image-1",
            "prompt": prompt,
            "n": 1,
            "size": "1024x1024",
            "quality": "medium"
        }

        try:
            response = requests.post(
                f"{BASE_URL}/images/generations",
                headers=HEADERS,
                json=data,
                timeout=120
            )

            if response.status_code != 200:
                afficher_erreur(response)
            else:
                result = response.json()

                image_data = result["data"][0]["b64_json"]

                image_bytes = base64.b64decode(image_data)

                with open("image.png", "wb") as file:
                    file.write(image_bytes)

                print("\nImage créée avec succès.")
                print("Fichier : image.png")

                if "cost_rodi" in result:
                    print(f"Coût : {result['cost_rodi']} RODI")

        except requests.RequestException as e:
            print(f"Erreur réseau : {e}")

        except KeyError:
            print("La réponse de l'API ne contient pas les données attendues.")
            print(response.text)

        choix = input(
            "\n[b] Retour | [r] Répéter | [s] Suivant : "
        ).lower()

        if choix == "b":
            return "back"

        if choix == "s":
            return "next"


def video():
    while True:
        print("\n--- ETAPE 3 : VIDEO ---")

        prompt = input("Description de la vidéo : ")

        data = {
            "model": VIDEO_MODEL,
            "prompt": prompt,
            "duration_seconds": 4
        }

        try:
            response = requests.post(
                f"{BASE_URL}/videos/generations",
                headers=HEADERS,
                json=data,
                timeout=150
            )

            if response.status_code != 200:
                afficher_erreur(response)
            else:
                result = response.json()

                video_data = result["data"][0]["b64_json"]

                video_bytes = base64.b64decode(video_data)

                with open("video.mp4", "wb") as file:
                    file.write(video_bytes)

                print("\nVidéo créée avec succès.")
                print("Fichier : video.mp4")

                if "cost_rodi" in result:
                    print(f"Coût : {result['cost_rodi']} RODI")

        except requests.RequestException as e:
            print(f"Erreur réseau : {e}")

        except KeyError:
            print("La réponse de l'API ne contient pas les données attendues.")
            print(response.text)

        choix = input(
            "\n[b] Retour | [r] Répéter | [q] Quitter : "
        ).lower()

        if choix == "b":
            return "back"

        if choix == "q":
            return "quit"


def main():
    if not API_KEY:
        print("Erreur : RODIUMAI_API_KEY n'est pas définie.")
        print("Vérifiez votre fichier .env.")
        return

    etape = 1

    while True:

        if etape == 1:
            chat()
            etape = 2

        elif etape == 2:
            resultat = image()

            if resultat == "back":
                etape = 1

            elif resultat == "next":
                etape = 3

        elif etape == 3:
            resultat = video()

            if resultat == "back":
                etape = 2

            elif resultat == "quit":
                print("\nProgramme terminé.")
                break


if __name__ == "__main__":
    main()