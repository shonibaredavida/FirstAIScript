import requests
import json
import os

banned_keywords = [ "hack", "bomb","kill",]
system_prompt ="You are to give clear, apt and gentle response, you are to act as an personal assistant and adviser"

def moderate_input(input_text):
    try:
        for keyword in banned_keywords:
            if keyword.lower() in input_text.lower():
                return False
        return True
    except Exception as e:
        print(f"Error in input moderation: {str(e)}")
        return False

def moderate_output(output_text):
    try:
        for keyword in banned_keywords:
            output_text = output_text.replace(keyword, "[REDACTED]")
            output_text = output_text.replace(keyword.capitalize(), "[REDACTED]")
            output_text = output_text.replace(keyword.upper(), "[REDACTED]")
        return output_text
    except Exception as e:
        print(f"Error in output moderation: {str(e)}")
        return output_text

def get_ai_response(user_prompt):
    try:
        api_url = "https://api.openai.com/v1/chat/completions"
        api_key =os.getenv("OPENAI_API_KEY")
        model = "gpt-3.5-turbo"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        data = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "max_tokens": 2040,
            "temperature": 0.6
        }


        response = requests.post(api_url, headers=headers, data=json.dumps(data))

        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
    except Exception as e:
        print(f"Error getting AI response: {str(e)}")
    return None

def main():
    try:
        user_prompt = input("Enter your prompt: ")

        if not moderate_input(user_prompt):
            print("Your input violated the moderation policy.")
            return
        ai_response = get_ai_response(user_prompt)
        if ai_response:
            moderated_response = moderate_output(ai_response)
            if moderated_response != ai_response:
                print("Your output violated the moderation policy.")
            print(moderated_response)
        else:
            print("Failed to get AI response.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()