import streamlit as st
import os
from PIL import Image
import io
import base64
import requests
from openai import OpenAI
import psycopg2
import aws_cdk as cdk

db_host = os.environ['DB_HOST']
db_user = os.environ['DB_USER']
db_password = os.environ['DB_PASSWORD']

api_key = "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"
weather_api = "0be641e1bbc1e83e986d8bb183d6a10c"

client = OpenAI(api_key=api_key)

def encode_image(image):
    buffered = io.BytesIO()
    if image.mode in ("RGBA", "LA"):
        background = Image.new(image.mode[:-1], image.size, (255, 255, 255))
        background.paste(image, image.split()[-1])  # Paste the image using the alpha channel as a mask
        image = background.convert("RGB")
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str


def outfit_creator_page():
    st.subheader("Outfit Creator")
    # Placeholder for outfit creation functionality
    st.write("Outfit creator functionality will be implemented here.")

def insert_image_description(description_to_save):
    conn = psycopg2.connect(
        dbname='postgres',
        user=db_user,
        password=db_password,
        host=db_host
    )

    try:
        with conn.cursor() as cur:
            cur.execute("create table if not exists image_descriptions (description varchar(700))")
            cur.execute("INSERT INTO image_descriptions (description) VALUES (%s)", (description_to_save,))
            conn.commit()
            print("Image description saved successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        conn.close()


def outfit_rater_page():
    st.subheader("Outfit Rater")
    # Placeholder for outfit rater functionality
    uploaded_file = st.file_uploader("Upload an image of your outfit for review", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
    try:
        base64_image = encode_image(image)
    except:
        return 
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
                        "text": "can you rate this outfit for all occasions  and maybe suggest changes to this outfit to make it look better "
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
    st.image(image, caption='Uploaded Image', use_column_width=True)
    st.write(description_data)


def insert_image_description(description_to_save):
    conn = psycopg2.connect(
        dbname='postgres',
        user=db_user,
        password=db_password,
        host=db_host
    )

    try:
        with conn.cursor() as cur:
            cur.execute("create table if not exists image_descriptions (description varchar(700))")
            cur.execute("INSERT INTO image_descriptions (description) VALUES (%s)", (description_to_save,))
            conn.commit()
            print("Image description saved successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        conn.close()

def add_to_your_closet_page():
    st.subheader("Add to Your Closet")
    uploaded_file = st.file_uploader("Upload an image of the clothing item", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        # To display the uploaded image
        image = Image.open(uploaded_file)
        st.image(uploaded_file, caption="Uploaded Clothing Item.")
        base64_image = encode_image(image)
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
        insert_image_description(description_data)
        st.write("Image upload functionality implemented.")
        




def display_values():
    conn = psycopg2.connect(
        dbname='postgres',
        user=db_user,
        password=db_password,
        host=db_host
    )

    try:
        with conn.cursor() as cur:
            cur.execute("select * from image_descriptions")
            x = cur.fetchall()
            return x
            conn.commit()
    except Exception as e:
        return f"An error occurred: {e}"
        conn.rollback()
    finally:
        conn.close()
def view_closet_page():
    st.subheader("View Closet")
    closet_items = display_values()
    
    if closet_items:
        for item in closet_items:
            # Assuming item is a tuple with a single string (description)
            description = item[0]
            
            # Splitting the description into parts based on newlines
            parts = description.split('\n')
            
            # Formatting with markdown for better presentation
            try:
                st.markdown(f"""
                **Description:**
                - **Color:** {parts[1].split(': ')[1]}
                - **Design:** {parts[2].split(': ')[1]}
                - **Type:** {parts[3].split(': ')[1]}
                - **Extra Features:** {parts[4].split(': ')[1]}
                """, unsafe_allow_html=True)
                st.markdown("---")  # Horizontal line for separation between items
            except:
                st.markdown(parts)
    else:
        st.write("Your closet is currently empty.")
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

def generate_outfit_recommendations(items, weather_condition):
    descriptions = [item[0] for item in items]
    descriptions_str = " ".join(descriptions)
    payload = {
        "model": "gpt-3.5-turbo-instruct",
        "prompt": f"Given these clothing items: {descriptions_str} and the weather conditon :{weather_condition} Suggest exactly three different outfits make sure to only use clothes given in the descriptions with their exact colors and styles and not anything else while taking into account clothes that would suit the weather conditions and numbered as 1. then 2. then 3. .",
        "temperature": 0.5,
        "max_tokens": 150
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"  # Ensure this is the correct key
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
        print(
            f"Failed to get a successful response from the API. Status Code: {response.status_code}, Response Text: {response.text}")
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
custom_css = """
<style>
input[type="text"]::placeholder {
    color: white;
    opacity: 1; /* Firefox */
}

input[type="text"] {
    color: white;
}
</style>
"""

def local_css(file_name):
    with open(file_name, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)

def colored_text_input(placeholder, key, color="white"):
    st.markdown(
        f"""
        <style>
            input[data-testid="stTextInput"]::placeholder {{
                color: {color};
            }}
            input[data-testid="stTextInput"] {{
                color: {color};
            }}
        </style>
        """, unsafe_allow_html=True
    )
    value = st.text_input("", placeholder=placeholder, key=key)
    return value
# Define your CSS
custom_css = """
<style>
/* Add your custom CSS styles here */
body, .stApp, .css-1d391kg, .css-18e3th9, .css-1e5imcs, .main .block-container {
    background-color: white !important;
    color: black !important;
}
/* Other styles... */
</style>
"""

# Use the function to inject CSS into the app
st.markdown(custom_css, unsafe_allow_html=True)

def outfit_creator_page():
    st.subheader("Outfit Creator")
    # Inject custom CSS with unsafe_allow_html
    st.markdown(custom_css, unsafe_allow_html=True)
    
    # Use the text input now with the custom CSS applied
    color_pref = st.text_input("Enter Color Preferences", key="color_pref")
    occasion = st.text_input("Enter Occasion", key="occasion")
    other_comments = st.text_input("Enter Any Other Comments", key="other_comments")
    if color_pref and occasion and other_comments:

        weather_condition = fetch_weather(weather_api)
        items = fetch_all_clothing_items()
        if items:
            recommendations = generate_outfit_recommendations(items, weather_condition)
            st.write(recommendations)
        else:
            st.write("Wardrobe needs more clothes")
        try:
            result = split_reccomendation(recommendations)
        except:
            result = []
        urls = []
    
        if len(result) == 3:
            for i in result:
                response = client.images.generate(
                    model="dall-e-3",
                    prompt=i + "put these clothes on a fully shown maneuqin exactly as given in the description",
                    size="1024x1024",
                    quality="standard",
                    n=1,
                )
                urls.append(response.data[0].url)
            if urls:
            
                cols = st.columns(len(urls), gap="small")
                for idx, url in enumerate(urls):
                    with cols[idx]:
                        st.image(url, use_column_width=True)
            
            else:
                st.write("No outfit recommendations to display.")
        else:
            st.write("Wardrobe needs more clothes")

# Function to create a page layout
def page_layout(page_name):
    if page_name == "Outfit Creator":
        outfit_creator_page()
    elif page_name == "Outfit Rater":
        outfit_rater_page()
    elif page_name == "Add to your Closet":
        add_to_your_closet_page()
    elif page_name == "View Closet":
        view_closet_page()

# Define your pages here
pages = {
    "Outfit Creator": "Please",
    "Outfit Rater": "Explore the latest fashion trends.",
    "Add to your Closet": "Get personalized wardrobe advice.",
    "View Closet": "Discover outfit ideas for any occasion.",
}

# Initialize session state for page navigation
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = "Home"

# Get the absolute path to the directory where this script is located
script_directory = os.path.dirname(os.path.abspath(__file__))

# Define the CSS file name
css_file_name = "styles.css"

# Construct the full path to the CSS file
css_file_path = os.path.join(script_directory, css_file_name)

# Import the custom CSS file
with open(css_file_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# App main title and header
st.title('DressSense.ai')
st.header("Your Clothes, Our Creativity, Your Elegance")

# Display buttons in a grid layout for navigation
cols = st.columns(2)  # Adjust the number of columns based on your layout needs
for index, (page_name, page_content) in enumerate(pages.items()):
    with cols[index % 2]:  # Adjust based on the number of columns
        if st.button(page_name):
            st.session_state['current_page'] = page_name

# Display the current page based on the button clicked
if st.session_state['current_page'] == "Home":
    st.title("Welcome to DressSense.ai")
    st.write("Select a feature to explore.")
else:
    page_layout(st.session_state['current_page'])
