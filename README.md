# PoliMeet
a TelegramBot that allows users to talk anonymously with each others.

# Setup
The next steps will show you how to deploy your version of this bot.

1: Clone this repository. You can simply do
```git clone https://github.com/DereWah/PoliMeet```
2: Access the folder "polimeet". In there you'll find the bot itself and some data files in which user information will be stored.
3: Install the following dependencies:
  - pyrogram (https://docs.pyrogram.org/intro/install)
  - google trans 3.1.0a0 (You need this specific version! https://stackoverflow.com/questions/52455774/googletrans-stopped-working-with-error-nonetype-object-has-no-attribute-group)
  - matplotlib
4: Open polimeet.py and customize the commented parts of the code to fit your needs. Add your userid to the admins, add a storage group ip and setup your authorization info.
5: If you want to customize stuff such as links and messages, you can edit messages.json. You can write in there in any language, as it will be then translated to the language a user uses. Obviously do not change the {} brackets, as those are needed in the code for formatting.
6: Run the bot and you're ready to go! Here are some of the commands you can run as an admin:
  - /stats | The bots sends images with statistics about the usage of the bot. The statistic is about what users put in settings, so gender, location, and study course. Then, sends a message about how many total/active/blocked users there are.
  - /forward | By sending this command in reply to a message, that message will be broadcasted to every active bot user. If you do so, always add in the end of the message (or as another broadcast) a message saying "do /start to use the bot". This is because the user might lose sight of the buttons to use the actual chatbot.
  - /get_blocks | Sends a ping to every user in the database, and immediately deletes it. This is to check if the user blocked the bot or not. Then, sends a message about how many total/active/blocked users there are. You shouldn't use this as bot blocks are already tracked and counted, so you can just do /stats.
  - /clear_conversations | Loops through all the saved conversation IDs in the database. If the amount of messages are less than 5, those are deleted.

