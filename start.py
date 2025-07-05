from pyrogram import Client

api_id = 24044190
api_hash = "6bbc975b3f04e29513e4bd319044bf28"

app = Client("account1", api_id, api_hash,
             device_model="realmeRMX3363",
             system_version="SDK 34",
             app_version="11.3.3 (53962)",
             lang_pack="android",
             lang_code="jabka",
             sleep_threshold=30,
             skip_updates=False)

app.run()

