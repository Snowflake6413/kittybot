import os
import time
import requests
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
SLACK_APP_TOKEN = os.environ.get('SLACK_APP_TOKEN')

app = App(token=SLACK_BOT_TOKEN)

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
					"action_id": "actionId-0"
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
					"action_id": "actionId-0"
				}
			]
		}
	]

    respond(blocks=blocks)
@app.message("meow")
def hug_react(message,client):
    print("MEOW!")
    try:
        client.reactions_add(
            channel=message["channel"],
            timestamp=message["ts"],
            name="cat-okay"
        )
    except Exception as e:
        print(f"Something with wrong with the reacion. {e}")


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

    

if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()