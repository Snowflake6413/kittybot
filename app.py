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
# ALLOWED_CHANNEL_ID = os.getenv("ALLOWED_CHANNEL_ID")

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
#gate keeper, remove # if needed.
#@app.use 
# def gatekeeper(context, next, ack, say):
   # current_channel = context.get("channel_id")
   # if current_channel and current_channel != ALLOWED_CHANNEL_ID:
     # try:
       #  ack()
        # say(
            # f"Meow! :sadcat: I am restricted to run only in <#{ALLOWED_CHANNEL_ID}>!",
            #ephemeral=True
        # )
      #except Exception:
       #  pass
      
      #return
   
  # next()
      
# First slash cmd
@app.command("/catimage")
def cat_img(ack, say, command):
    ack()
    user_id = command["user_id"]
    
    try:
        response = requests.get("https://api.thecatapi.com/v1/images/search", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            cat_url = data[0]['url']
            cat_id = data[0]['id']

            say(
                blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Here is your cute kitty, <@{user_id}>! :neocat_3c: (ID: {cat_id})"
                }
            },
            {
                "type": "image",
                "title": {
                    "type": "plain_text",
                    "text": "KITTY!!",
                    "emoji": True
                },
                "image_url": cat_url,
                "alt_text": "KITTTTY!!!"
            }
        ]
            )
        else:
            say(
                text=f"Meow! :sadcat: I couldn't fetch a cat image right now (status {response.status_code}). Please try again later!"
            )
    except requests.exceptions.Timeout:
        say(
            text=f"Meow! :sadcat: The cat API is taking too long to respond. Please try again later!"
        )
    except requests.exceptions.RequestException:
        say(
            text=f"Meow! :sadcat: I encountered an error while fetching a cat image. Please try again later!"
        )


@app.command("/help")
def bot_help(ack, respond):
    ack()
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
def cat_fact(ack, say, command):
    ack()
    user_id = command["user_id"]
    
    try:
        response = requests.get("https://catfact.ninja/fact", timeout=10)

        if response.status_code == 200:
            data = response.json()
            fact = data['fact']

            say(
                blocks=[{
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"Here is your cat fact, <@{user_id}>! :neocat:",
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
        else:
            say(
                text=f"Meow! :sadcat: I couldn't fetch a cat fact right now (status {response.status_code}). Please try again later!"
            )
    except requests.exceptions.Timeout:
        say(
            text=f"Meow! :sadcat: The cat fact API is taking too long to respond. Please try again later!"
        )
    except requests.exceptions.RequestException:
        say(
            text=f"Meow! :sadcat: I encountered an error while fetching a cat fact. Please try again later!"
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
					"url": "https://github.com/Snowflake6413/kittenbot",
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
def cat_gif(ack, say, command):
    ack()
    user_id = command["user_id"]
    cooley_gif = f"https://cataas.com/cat/gif?t={time.time()}"

    say(
        response_type="in_channel",
        blocks=[
            
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Here is a kitty gif, <@{user_id}>! :neocat:"
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
def ai_mention(event, say, body, logger, client, respond):
    logger.info("Moshi moshi! Got Message!")
    logger.info(body)
    user_msg= event['text']
    thread_ts = event.get("thread_ts", event["ts"])
    channel_id = event["channel"]
    message_ts = event["ts"]
    
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
        
        conversation_context = [
            {"role": "system", "content":"Act as a helpful cat assistant. Be cute, use cat puns/sounds/emojis, address user as 'Hooman', and describe actions in italics (*purrs*). maintain persona while being useful."
}
        ]
        
        # Only fetch thread history if this is actually a thread (not the first message)
        if thread_ts != message_ts:
            memory = client.conversations_replies(
                channel=channel_id,
                ts=thread_ts,
                limit = 10
            )

            memory_data = memory['messages']
            current_msg_included = False

            for msg in memory_data:
                text = msg.get("text")
                if text:  # Only process messages with text
                    # Check if this is the current message
                    if msg.get("ts") == message_ts:
                        current_msg_included = True
                    
                    if "bot_id" in msg:
                        conversation_context.append({"role": "assistant", "content": text})
                    else:
                        conversation_context.append({"role": "user", "content": text})
            
            # If current message wasn't in the thread history, add it
            if not current_msg_included:
                conversation_context.append({"role": "user", "content": user_msg})
        else:
            # First message in thread, just add the current user message
            conversation_context.append({"role": "user", "content": user_msg})

        response = chat_client.chat.completions.create(
            model=LLM_MODEL,
            messages=conversation_context,
            max_tokens=500
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