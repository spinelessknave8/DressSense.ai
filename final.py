import base64
import requests
import os
import psycopg2
import json
from openai import OpenAI

# Assuming you have set your API keys and database credentials as environment variables in the Lambda function
api_key = os.environ.get('api_key')
api_key1 = os.environ.get('api_key1')
weather_api = os.environ.get('weather_api')
db_host = os.environ.get('db_host')
db_user = os.environ.get('db_user')
db_password = os.environ.get('db_password')

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def insert_image_description(description_to_save, connection_info):
    # Connect using the connection_info parameters
    with psycopg2.connect(**connection_info) as conn:
        with conn.cursor() as cur:
            cur.execute("CREATE TABLE IF NOT EXISTS image_descriptions (description VARCHAR(700))")
            cur.execute("INSERT INTO image_descriptions (description) VALUES (%s)", (description_to_save,))
            conn.commit()
def fetch_weather(api_key):
    lat = "1.3521"
    lon = "103.8198"
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        data1 = response.json()
        try:
            main_weather = data1['weather'][0]['main']
            temperature = data1['main']['temp']
            
            if "Rain" in main_weather or "Drizzle" in main_weather or "Thunderstorm" in main_weather:
                weather_condition = "Rainy"
            elif temperature > 25:
                weather_condition = "Warm"
            else:
                weather_condition = "Cold"
            
            return weather_condition
        except KeyError:
            print(f"KeyError: Missing expected data in the response: {data1}")
            return None
    else:
        print(f"Failed to fetch weather data. Status Code: {response.status_code}, Response Text: {response.text}")
        return None

def insert_image_description(description_to_save, db_params):
    # Use db_params to establish database connection and execute queries
    with psycopg2.connect(**db_params) as conn:
        with conn.cursor() as cur:
            cur.execute("CREATE TABLE IF NOT EXISTS image_descriptions (description VARCHAR(700))")
            cur.execute("INSERT INTO image_descriptions (description) VALUES (%s)", (description_to_save,))
            cur.execute("truncate table image_descriptions")
            conn.commit()


def fetch_all_clothing_items():
    conn = psycopg2.connect(
        dbname='postgres',
        user=db_user,
        password=db_password,
        host=db_host
    )
    items = []
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT distinct description FROM image_descriptions;")
            items = cur.fetchall()
    except Exception as e:
        print(f"Error fetching items: {e}")
    finally:
        conn.close()
    return items

def generate_outfit_recommendations(items,weather_condition):
    descriptions = [item[0] for item in items] 
    descriptions_str = " ".join(descriptions)
    payload = {
        "model":"gpt-3.5-turbo-instruct",
        "prompt": f"Given these clothing items: {descriptions_str} and the weather conditon :{weather_condition} Suggest exactly three different outfits make sure to only use clothes given in the descriptions with their exact colors and styles and not anything else while taking into account clothes that would suit the weather conditions and numbered as 1. then 2. then 3. .",
        "temperature": 0.5,
        "max_tokens": 150
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key1}"  # Ensure this is the correct key
    }

    response = requests.post("https://api.openai.com/v1/completions", headers=headers, json=payload)
    
    if response.status_code == 200:
        response_data = response.json()
        try:
            return response_data['choices'][0]['text']
        except KeyError:
            print(f"KeyError: 'choices' not found in the response. Here's the response data: {response_data}")
            return None
    else:
        print(f"Failed to get a successful response from the API. Status Code: {response.status_code}, Response Text: {response.text}")
        return None

def split_reccomendation(recommendations):
    result = []
    split_string = [s.strip() for s in recommendations.split('\n') if s.strip().startswith(('1.', '2.', '3.'))]
    if len(split_string) >= 3:
        outfit_1 = split_string[0]
        outfit_2 = split_string[1]
        outfit_3 = split_string[2]
        result.append(outfit_1)
        result.append(outfit_2)
        result.append(outfit_3)
        return result

    else:
        print("Not enough outfit recommendations found.")
        return None

def lambda_handler(event, context):
    client = OpenAI(api_key=os.environ.get('api_key'))

    weather_condition = fetch_weather(os.environ.get('weather_api'))
    connection_info = {
        'dbname': os.environ.get('DB_NAME'),
        'user': os.environ.get('DB_USER'),
        'password': os.environ.get('DB_PASSWORD'),
        'host': os.environ.get('DB_HOST')
    }
    image_url = event.get('image_url')
    if not image_url:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'No image URL provided'})
        }

    # Encode the image
    response = requests.get(image_url)
    if response.status_code == 200:
        base64_image = base64.b64encode(response.content).decode('utf-8')
    else:
        return {
            'statusCode': response.status_code,
            'body': json.dumps({'message': 'Failed to fetch image'})
        }
    image_path = encode_image(image_url)
    headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {api_key}"
    }
    
    payload = {
      "model": "gpt-4-vision-preview",
      "messages": [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "describe the features in the clothing in this image in the format description: color : design : type: extra features: ? try to as specific as possible with the design if any"
            },
            {
              "type": "image_url",
              "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
              }
            }
          ]
        }
      ],
      "max_tokens": 300
    }
    
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    data = response.json()
    description_data = data['choices'][0]['message']['content']
    insert_image_description(description_data,connection_info)
    weather_condition = fetch_weather(weather_api)
    items = fetch_all_clothing_items(connection_info)
    recommendations = generate_outfit_recommendations(items, weather_condition)
    result = split_reccomendation(recommendations)

    urls = []
    if len(result) == 3:
        for i, description in enumerate(result):
            response = client.images.generate(
                model="dall-e-3",
                prompt=description + " put these clothes on a mannequin exactly as given in the description",
                size="1024x1024",
                quality="standard",
                n=1
            )
            urls.append(response.data[0].url)

    return {
        'statusCode': 200,
        'body': json.dumps({
            'urls': urls
        }),
        'headers': {
            'Content-Type': 'application/json'
        }
    }


if __name__ == "__main__":
    test_event = {} 
    test_context = {}  
    print(lambda_handler(test_event, test_context))


