# Dont judge my code :cry:
# Our imports
import time
import os
import requests
from openai import OpenAI
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Just to make sure its actually running :winky:
print("Running...")

# Get .env and passes them as REAL variables
load_dotenv()


# our envs
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv('SLACK_APP_TOKEN')
OAI_KEY = os.getenv('OAI_KEY')
OAI_BASE_URL= os.getenv('OAI_BASE_URL')
LLM_MODEL = os.getenv('LLM_MODEL')
MODERATION_URL = os.getenv('MODERATION_URL')
MODERATION_KEY = os.getenv('MODERATION_KEY')
WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

#configure OAI 
chat_client = OpenAI(
            api_key=OAI_KEY,
            base_url=OAI_BASE_URL
        )
# configure moderation OAI
moderation_client = OpenAI(
    base_url=MODERATION_URL,
    api_key=MODERATION_KEY
)
# set bot token
app = App(token=SLACK_BOT_TOKEN)
# First slash cmd
@app.command("/catimage")
def cat_img(ack, say):
    ack()
    response = requests.get("https://api.thecatapi.com/v1/images/search")
    
    if response.status_code == 200:
        data = response.json()
        cat_url = data[0]['url']
        cat_id = data[0]['id']

        say(
            blocks=[{
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"Here is your cute kitty! :neocat_3c: (ID: {cat_id})", 
                        "emoji": True
                    }
                },
                {
                    "type": "image",
                    "image_url": cat_url, 
                    "alt_text": "Kitty!"
                }
            ],
            text=f"Here is a cat! (ID: {cat_id})" 
        )
    else:
        say("Sorry, no cats found right now.")

@app.command("/weather")
def weather_in_cat_city(ack, respond, command):
    ack
    city = command.get('text', '').strip() or 'Istanbul'

    try: 
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url)

        if response.status_code == 200:
         data = response.json()

        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        description = data['weather'][0]['description']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']

        blocks = [
            {
	
			"type": "section",
			"text": {
				"type": "plain_text",
				"text": "🌤️ Weather in {city.title()}",
				"emoji": True
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Temperature:* {temp}°C (feels like {feels_like}°C)\n*Condition:* {description.title()}\n*Humidity:* {humidity}%\n*Wind Speed:* {wind_speed} m/s"
			}
		}
	]
        respond(blocks=blocks)
    
    except Exception as e:
     print("Unable to send weather info. {e}")

@app.command("/help")
def bot_help(ack, respond):
    
    blocks=[{

		
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "KittenBot Help :neocat:",
				"emoji": True
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Available commands for you to use!"
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"fields": [
				{
					"type": "mrkdwn",
					"text": "*/catimage*\nGet a random cat picture."
				},
				{
					"type": "mrkdwn",
					"text": "*/catfact*\nGet a random cat fact."
				},
				{
					"type": "mrkdwn",
					"text": "*/catgif*\nGet a random cat GIF."
				},
				{
					"type": "mrkdwn",
					"text": "*/about*\nInfo about the creator."
				},
				{
					"type": "mrkdwn",
					"text": f"*@MeowBot [text]*\nMention me to chat with AI! Powered by {LLM_MODEL}!"
				}
			]
		}
	]
    respond(blocks=blocks)
@app.command("/catfact")
def cat_fact(ack, say):
    ack()
    response = requests.get("https://catfact.ninja/fact")

    if response.status_code == 200:
     data = response.json()
     fact = data['fact']

    say(
        blocks=[{
			"type": "section",
			"text": {
				"type": "plain_text",
				"text": "Your cat fact! :neocat:",
				"emoji": True
			}
		},
		{
			"type": "section",
			"text": {
				"type": "plain_text",
				"text": fact,
				"emoji": True
			}
		}
	]
    )

@app.command("/about")
def get_info(ack, respond):
    ack()
    blocks=[
        {
			"type": "section",
			"text": {
				"type": "plain_text",
				"text": "This bot was made by Alexander! (areallyawesomeusername) :heidi-paws: It was made for the Meow YSWS, because we like cats, right?",
				"emoji": True
			}
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Visit Repo",
						"emoji": True
					},
					"value": "click_me_123",
					"url": "https://github.com/Snowflake6413",
					"action_id": "actionId-1"
				}
			]
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Check out the Meow YSWS!",
						"emoji": True
					},
					"value": "click_me_123",
					"url": "https://meow.hackclub.com",
					"action_id": "actionId-2"
				}
			]
		}
	]

    respond(blocks=blocks)

@app.command("/catgif") 
def cat_gif(ack, respond):
    ack()
    cooley_gif = f"https://cataas.com/cat/gif?t={time.time()}"

    respond(
        response_type="in_channel",
        blocks=[
            
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Here is a kitty gif! :neocat:"
                }
            },  
            
            
            {
                "type": "image",
                "image_url": cooley_gif,
                "alt_text": "A random cat gif"
            }
        ]
    )

@app.event("app_mention")
def ai_mention(event, say, body, logger, client):
    logger.info("Moshi moshi! Got Message!")
    logger.info(body)
    user_msg= event['text']
    thread_ts = event.get("thread_ts", event["ts"])
    channel_id = event["channel"]
    message_ts = event["ts"]
    original_text=event['text']
    
    try:
        client.reactions_add(
            channel=channel_id,
            timestamp=message_ts,
            name="thought_balloon"
        )
    except Exception as e:
        print("Unable to add reaction")

    try:
        
        moderation = moderation_client.moderations.create(input=user_msg)
        if moderation.results[0].flagged:
            say(
                text=f"Meow! :sadcat: I am unable to respond due to your message containing flagged content! Please try again with a new message!", thread_ts=thread_ts
        ) 
            return
        
        
        memory = client.conversations_replies(
            channel=channel_id,
            ts=thread_ts,
            limit = 10
        )

        memory_data = memory['messages']

        conversation_context = [
            {"role": "system", "content":"Act as a helpful cat assistant. Be cute, use cat puns/sounds/emojis, address user as 'Hooman', and describe actions in italics (*purrs*). maintain persona while being useful."
}
        ]

        for msg in memory_data:
            text = msg.get("text")
            if "bot_id" in msg:
             conversation_context.append({"role": "assistant", "content": text})
            else:
               conversation_context.append({"role": "user", "content": text})

        response = chat_client.chat.completions.create(
            model=LLM_MODEL,
            messages=conversation_context,
            max_tokens=150
        )
         
        ai_reply= response.choices[0].message.content
        say(text=f"{ai_reply}", thread_ts=thread_ts)

    except Exception as e:
        say(text=f"Oops! Unable to get a response from OpenAI. {e}", thread_ts=thread_ts)
        
    finally:
        try:
            client.reactions_remove(
                channel=channel_id,
                timestamp=message_ts,
                name="thought_balloon"
            )
        except Exception as e:
            print("Unable to remove reaction")

  
# run it and hope for the best
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()