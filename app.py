import openai
from flask import Flask, render_template, request

app = Flask(__name__)

# Replace 'your_api_key_here' with your actual OpenAI API key
api_key = 'YOUR_OPENAI_KEY'

# Initialize OpenAI API client
openai.api_key = api_key

def predict_emotion(text):
    response = None
    try:
        # Make an API call to OpenAI's engine to generate a response
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"Analyze the emotion in the following text'{text}'",
            max_tokens=50,  # Adjust max tokens based on your needs
            temperature=0.7,  # Adjust temperature for randomness
            stop=None  # You can specify stopping conditions if needed
        )
        
        # Extract the generated text from the response
        generated_text = response.choices[0].text.strip()

        # Return the generated text as the predicted emotion
        return generated_text

    except Exception as e:
        print(f"Error occurred: {e}")
        if response:
            print(f"Response: {response}")
        return None

def get_emotion_class(emotion, response_text):
    emotion_keywords = {
        "happy": ["happy", "joyful", "ecstatic"],
        "sad": ["sad", "melancholic", "depressed"],
        "angry": ["angry", "irritated", "frustrated"],
        "neutral": ["neutral", "calm", "indifferent"],
        # Define more emotions and their corresponding keywords as needed
    }
    
    for emotion_key, keywords in emotion_keywords.items():
        for keyword in keywords:
            if keyword in response_text.lower():
                return f"{emotion_key}-emotion"
    
    return "default-emotion"


@app.route('/', methods=['GET', 'POST'])
def index():
    emotion = None
    emotion_class = None
    if request.method == 'POST':
        text_snippet = request.form['text_snippet']
        emotion = predict_emotion(text_snippet)
        emotion_class = get_emotion_class(emotion, text_snippet)  # Pass both emotion and response text

    return render_template('index.html', emotion=emotion, emotion_class=emotion_class)


if __name__ == '__main__':
    app.run(debug=True)