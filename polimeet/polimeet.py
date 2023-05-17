import json
from pyrogram import Client, emoji, filters, types, enums
from googletrans import Translator
import pyrogram
import datetime
import secrets
import re
import random
import matplotlib.pyplot as plt

admins = [167917398] #add in here users that will have admin access
storage_group = -979244505 #this is where messages will be forwarded (only WHEN REPORTED)


#Follow the tutorial at this link to get the information below:
#https://docs.pyrogram.org/start/auth
api_id = 0000000
api_hash = "API_HASH"
bot_token = "BOT_TOKEN"

#If turned on, bot will be put in maintenance, and users will have a little notification when they interact with the bot.
maintenance = False

#names of the json files in which user info and messages info will be stored.
storage_json = "storage.json"
messages_json = "messages.json"
conversations_json = "conversations.json"


translator = Translator(service_urls=['translate.googleapis.com'])
storage = {}

app = Client(
	"my_bot",
	api_id=api_id, api_hash=api_hash,
	bot_token=bot_token
	)


def t(text, target_language):
	try:
		if target_language is None:
			target_language = "en"
		return translator.translate(text, dest=target_language).text
	except:
		return text


def new_chat_button(lang):
	new_chat = types.InlineKeyboardButton(
		t(m["new_chat_button"],
		lang),
		callback_data="new_chat"
	)
	return new_chat

def settings_button(lang):
	settings = types.InlineKeyboardButton(
		t(m["settings_button"],
		lang),
		callback_data="settings"
	)
	return settings

def language_button(lang):
	language = types.InlineKeyboardButton(
		t(m["language_button"],
		lang),
		callback_data="language"
	)
	return language
	
def about_us_button(lang):
	about_us = types.InlineKeyboardButton(
		t(m["about_us_button"], lang),
		url=m["about_us_channel"]
	)
	return about_us
	
def support_button(lang):
	support = types.InlineKeyboardButton(
		t(m["support_button"], lang),
		url=m["support_bot"]
	)
	return support

def cancel_button(lang):
	cancel = types.InlineKeyboardButton(
		t(m["back_button"],
		lang),
		callback_data="cancel"
	)
	return cancel

def leave_button(lang):
	leave = types.InlineKeyboardButton(
		t(m["leave_chat_button"],
		lang),
		callback_data="leave"
	)
	return leave

def report_button(lang, cid):
	report = types.InlineKeyboardButton(
		t(m["report_button"],
		lang),
		callback_data=f"report.{cid}"
	)
	return report

def gender_button(lang):
	button	= types.InlineKeyboardButton(
		t(m["gender_button"],
		lang),
		callback_data="gender"
	)
	return button
	
def loc_button(lang):
	button	= types.InlineKeyboardButton(
		t(m["loc_button"],
		lang),
		callback_data="loc"
	)
	return button
	
def interests_button(lang):
	button	= types.InlineKeyboardButton(
		t(m["interests_button"],
		lang),
		callback_data="interests"
	)
	return button
	
def course_button(lang):
	button	= types.InlineKeyboardButton(
		t(m["course_button"],
		lang),
		callback_data="course"
	)
	return button

def gender_keyboard(lang):
	
	male = types.InlineKeyboardButton(t(m["m_gender_button"], lang), callback_data = "set.gender.male")
	
	female = types.InlineKeyboardButton(t(m["f_gender_button"], lang), callback_data = "set.gender.female")
	
	other = types.InlineKeyboardButton(t(m["o_gender_button"], lang), callback_data = "set.gender.other")
	
	none = types.InlineKeyboardButton(t(m["none_button"], lang), callback_data = "set.gender.none")
	
	
	kb = types.InlineKeyboardMarkup([
	
		[male, female, other],
		[none]
	
	])
	
	return kb

def loc_keyboard(lang):
	
	mcs = types.InlineKeyboardButton(t(m["mcs_loc_button"], lang), callback_data = "set.loc.Milano Città Studi")
	bovisa = types.InlineKeyboardButton(t(m["bovisa_loc_button"], lang), callback_data = "set.loc.Milano Bovisa")	
	none = types.InlineKeyboardButton(t(m["none_button"], lang), callback_data = "set.loc.none")
	
	kb = types.InlineKeyboardMarkup([
		[mcs],
		[bovisa],
		[none]
	])
	
	return kb

def course_keyboard(lang):
	
	inf = types.InlineKeyboardButton(t("Ing. Informatica", lang), callback_data="set.course.Ingegneria Informatica")
	elec = types.InlineKeyboardButton(t("Ing. Elettronica", lang), callback_data="set.course.Ingegneria Elettronica")
	math = types.InlineKeyboardButton(t("Ing. Matematica", lang), callback_data="set.course.Ingegneria Matematica")
	gest = types.InlineKeyboardButton(t("Ing. Gestionale", lang), callback_data="set.course.Ingegneria Gestionale")
	auto = types.InlineKeyboardButton(t("Ing. Meccanica", lang), callback_data="set.course.Ingegneria Meccanica")
	fis = types.InlineKeyboardButton(t("Ing. Fisica", lang), callback_data="set.course.Ingegneria Fisica")
	aero = types.InlineKeyboardButton(t("Ing. Aerospaziale", lang), callback_data="set.course.Ingegneria Aerospaziale")
	mate = types.InlineKeyboardButton(t("Ing. dei Materiali", lang), callback_data="set.course.Ingegneria dei Materiali")
	elec2 = types.InlineKeyboardButton(t("Ing. Elettrica", lang), callback_data="set.course.Ingegneria Elettrica")
	chim = types.InlineKeyboardButton(t("Ing. Chimica", lang), callback_data="set.course.Ingegneria Chimica")
	amb = types.InlineKeyboardButton(t("Ing. Ambientale", lang), callback_data="set.course.Ingegneria Ambientale")
	arch = types.InlineKeyboardButton(t("Ing. Edile-Architettura", lang), callback_data="set.course.Ingegneria Edile-Architettura")
	none = types.InlineKeyboardButton(t(m["none_button"], lang), callback_data = "set.course.none")
	
	
	
	kb = types.InlineKeyboardMarkup([
		[inf, gest],
		[elec, auto],
		[fis, aero],
		[mate, math],
		[elec2, chim],
		[amb, arch],
		[none]
	
	])
	
	return kb
		
def save_storage():
	global storage
	global conversations
	with open(storage_json, "w", encoding="utf-8") as f:		
		json.dump(storage, f, indent=4, ensure_ascii=False)
	print("storage has been saved.")
	with open(storage_json, encoding="utf-8") as jsonfile:
		storage = json.load(jsonfile)
		jsonfile.close()
	with open(conversations_json, "w", encoding="utf-8") as f:		
		json.dump(conversations, f, indent=4, ensure_ascii=False)
	print("conversations has been saved.")
	with open(conversations_json, encoding="utf-8") as jsonfile:
		conversations = json.load(jsonfile)
		jsonfile.close()

def initialize_storage():
	global storage
	if list(storage.keys()).count("initialized") == 0:
		print("storage initialized")
		storage = {
			"convo": 0,
			"initialized": True,
			"users": {},
			"searching": [],
			"stats": {
				"micro2": 0,
				"micro3": 0,
				"micro5": 0,
				"bacheca2": 0,
				"bacheca3": 0,
				"bagni": 0,
				"mensa": 0,
				"altro": 0,
				"agora": 0,
				"guardoni": 0
			}
		}

with open(storage_json, encoding="utf-8") as jsonfile:
	storage = json.load(jsonfile)
	initialize_storage()
	jsonfile.close()
	print("storage has been loaded.")
	
with open(messages_json, encoding="utf-8") as jsonfile:
	m = json.load(jsonfile)
	initialize_storage()
	jsonfile.close()
	print("messages has been loaded.")
	
with open(conversations_json, encoding="utf-8") as jsonfile:
	conversations = json.load(jsonfile)
	initialize_storage()
	jsonfile.close()
	print("conversations has been loaded.")
	
@app.on_message(filters.command("maintenance"))
async def send_maintenance(client, message):
	if message.from_user.id in admins:
		await broadcast_string("The bot will now be in maintenance. You will not be able to chat until some issues are solved. Sorry about this.")
		
def is_new_user(user: types.User):
	if list(storage["users"].keys()).count(f"{user.id}") == 0:
		print("new user")
		return True
	else:
		return False
	
def get_lang(user: types.User):
	if not is_new_user(user):
		return storage["users"][f"{user.id}"]["language"]
	else:
		return "en"
	
def save_user(user):
	if is_new_user(user):
		user_dic = {
			"language": f"{user.language_code}",
			"gender": None,
			"status": "idle",
			"course": None,
			"loc": None,
			"matched": None,
			"last_inline": None,
			"stopped": False,
			"interests": None,
		}
		storage["users"][f"{user.id}"] = user_dic
		save_storage()

def set_status(user, status):
	if not is_new_user(user):
		storage["users"][f"{user.id}"]["status"] = status
	else:
		save_user(user)

def is_stopped_id(userid):
	if userid in (storage["users"].keys()):
		return storage["users"][f"{userid}"]["stopped"]
	else:
		return True

def get_matched(user):
	if not is_new_user(user):
		return storage["users"][f"{user.id}"]["matched"]

def get_status(user):
	if not is_new_user(user):
		return storage["users"][f"{user.id}"]["status"]
	else:
		set_status(user, "idle")
		return "idle"

def get_course(user):
	if not is_new_user(user):
		if storage["users"][f"{user.id}"]["course"]:
			return storage["users"][f"{user.id}"]["course"]
		else:
			return "none"
	else:
		return "none"
		
def get_gender(user):
	if not is_new_user(user):
		if storage["users"][f"{user.id}"]["gender"]:
			return storage["users"][f"{user.id}"]["gender"]
		else:
			return "none"
	else:
		return "none"

def get_loc(user):
	if not is_new_user(user):
		if storage["users"][f"{user.id}"]["loc"]:
			return storage["users"][f"{user.id}"]["loc"]
		else:
			return "none"
	else:
		return "none"		

def get_interests(user):
	if not is_new_user(user):
		if "interests" in list(storage["users"][f"{user.id}"].keys()):
			if storage["users"][f"{user.id}"]["interests"]:
				return storage["users"][f"{user.id}"]["interests"]
			else:
				return "none"
		else:
			storage["users"][f"{user.id}"]["interests"] = "none"
			return "none"

def language_keyboard():


	en = types.InlineKeyboardButton("🇬🇧", callback_data="set.language.en")
	ru = types.InlineKeyboardButton("🇷🇺", callback_data="set.language.ru")
	it = types.InlineKeyboardButton("🇮🇹", callback_data="set.language.it")
	es = types.InlineKeyboardButton("🇪🇸", callback_data="set.language.es")
	de = types.InlineKeyboardButton("🇩🇪", callback_data="set.language.de")
	fr = types.InlineKeyboardButton("🇫🇷", callback_data="set.language.fr")
	kb = [[en, ru, it], [es, de, fr]]
	
	return(types.InlineKeyboardMarkup(kb))



async def stat_plot(userid):
	figure, grafico = plt.subplots()
	grafico.set_title("Grafico uso del chatbot")
	y_pos = range(0, len(list(storage["stats"].keys())))
	volantini = list(storage["stats"].keys())
	values = list(storage["stats"].values())
	grafico.barh(y_pos, width=values, align='center', color="red")
	grafico.set_xlabel("Utilizzi")
	grafico.set_yticks(y_pos, labels = volantini)
	plt.savefig('stats.png')
	plt.close()
	await app.send_photo(userid, "stats.png")
	
async def gender_plot(userid):
	figure, grafico = plt.subplots()
	grafico.set_title("Grafico uso del chatbot")
	
	data = {}
	for uid in list(storage["users"].keys()):
		if not storage["users"][uid]["gender"]:
			gender = "none"
		else:
			gender = storage["users"][uid]["gender"]
		if list(data.keys()).count(gender) == 0:
			data[gender] = 1
		else:
			data[gender] += 1
	
	y_pos = range(0, len(list(data.keys())))
	
	genders = list(data.keys())
	values = list(data.values())
	grafico.barh(y_pos, width=values, align='center', color="pink")
	grafico.set_xlabel("Utilizzi")
	grafico.set_yticks(y_pos, labels = genders)
	plt.savefig('genders.png')
	plt.close()
	await app.send_photo(userid, "genders.png")
	
async def loc_plot(userid):
	figure, grafico = plt.subplots()
	grafico.set_title("Grafico uso del chatbot")
	
	data = {}
	for uid in list(storage["users"].keys()):
		if not storage["users"][uid]["loc"]:
			loc = "none"
		else:
			loc = storage["users"][uid]["loc"]
		if list(data.keys()).count(loc) == 0:
			data[loc] = 1
		else:
			data[loc] += 1
	
	y_pos = range(0, len(list(data.keys())))
	
	locs = list(data.keys())
	values = list(data.values())
	grafico.barh(y_pos, width=values, align='center', color="yellow")
	grafico.set_xlabel("Utilizzi")
	grafico.set_yticks(y_pos, labels = locs)
	plt.savefig('locs.png')
	plt.close()
	await app.send_photo(userid, "locs.png")

async def course_plot(userid):
	figure, grafico = plt.subplots()
	grafico.set_title("Grafico uso del chatbot")
	
	data = {}
	for uid in list(storage["users"].keys()):
		course = "none"
		if storage["users"][uid]["course"]:
			course = storage["users"][uid]["course"]
		if list(data.keys()).count(course) == 0:
			data[course] = 1
		else:
			data[course] += 1
	y_pos = range(0, len(list(data.keys())))
	
	courses = list(data.keys())
	values = list(data.values())
	grafico.barh(y_pos, width=values, align='center', color="green")
	grafico.set_xlabel("Utilizzi")
	grafico.set_yticks(y_pos, labels = courses)
	plt.savefig('courses.png')
	plt.close()
	await app.send_photo(userid, "courses.png")


@app.on_message(filters.command("stats"))
async def send_stats(client, message):
	user = message.from_user
	if user.id in admins:
		await gender_plot(user.id)
		await loc_plot(user.id)
		await course_plot(user.id)
		await stat_plot(user.id)
		total = len(list(storage["users"].keys()))
		stopped = 0
		for uid in list(storage["users"].keys()):
			if storage["users"][uid]["stopped"] == True:
				stopped += 1
		
		await message.reply(f"👥 Total users: {total}\n🚫 Blocked: {stopped}\n✅ Active: {total-stopped}")	
		
		
async def switch_lang(user: types.User, message: types.Message):
	inline_keyboard = language_keyboard()
	await message.edit_text(t(m["change_lang"].format(get_lang(user)), get_lang(user)), reply_markup=inline_keyboard)


async def notify_admins(string):
	for uid in admins:
		try:
			await app.send_message(uid, string)
		except:
			print(f"Could not contact admin {uid}")	
	
async def broadcast_string(string):
	for uid in list(storage["users"].keys()):
		if is_stopped_id(uid) is False:
			try:
				await app.send_message(int(uid), string)
			except:
				storage["users"][uid]["stopped"] = True
				
async def broadcast_copy(message: types.Message):
	for uid in list(storage["users"].keys()):
		if is_stopped_id(uid) is False:
			try:
				await message.copy(int(uid))
			except:
				storage["users"][uid]["stopped"] = True

async def welcome(user: types.User, message: types.Message):
	lang = get_lang(user)
	kb = types.InlineKeyboardMarkup(
		[[new_chat_button(lang)],
		[settings_button(lang), about_us_button(lang)],
		[language_button(lang), support_button(lang)]]
	)
	msg = await message.edit_text(
		t(m["welcome"], get_lang(user)),
		reply_markup=kb
	)
	
	await save_inline(user, msg)

async def try_match(user: types.User, message: types.Message):
	lang = get_lang(user)
	if (len(storage["searching"]) == 0) or (user.id in admins):
		kb = types.InlineKeyboardMarkup([
			[cancel_button(lang)]
		])
		storage["searching"].append(f"{user.id}")
		set_status(user, "searching")
		await message.edit_text(t(m["now_searching"], lang), reply_markup = kb)
	else:
		matched_id = storage["searching"][0] #---------- SWITCH TO RANDOM AT SOME POINT?
		
		matched = await app.get_users(int(matched_id))
		
		storage["convo"] += 1
		convo = storage["convo"]
		
		conversations[f"{convo}"] = {
			"messages": [],
			"users": [user.id, matched.id],
			"reported": False
		}
		
		storage["searching"].remove(matched_id)
		await match(user, matched, convo)
		await match(matched, user, convo)
		
async def match(user, matched, convo):
	set_status(user, f"matched.{convo}")
	storage["users"][f"{user.id}"]["matched"] = matched.id
	lang = get_lang(user)
	kb = types.InlineKeyboardMarkup([[leave_button(lang), report_button(lang, convo)]])
	
	text = "\n"
	if get_course(matched) != "none":
		text += f"\n👨‍🎓 Course: {get_course(matched)}"
	if get_gender(matched) != "none":
		text += f"\nℹ️ Gender: {get_gender(matched)}"
	if get_loc(matched) != "none":
		text += f"\n📍 Loc: {get_loc(matched)}"
	if get_interests(matched) != "none":
		text += f"\n🧩 Interests: {get_interests(matched)}"
	msg = await app.send_message(user.id, t(m["new_match"], lang).format(f"{text}\n"), reply_markup = kb)	
	await save_inline(user, msg)
	
		
async def force_leave(user: types.User):
	status = get_status(user)
	if "matched" in status:
		lang = get_lang(user)
		convo = get_status(user).split(".")[1]
		set_status(user, "idle")
		storage["users"][f"{user.id}"]["matched"] = None
		
		kb = types.InlineKeyboardMarkup([[cancel_button(lang), new_chat_button(lang)]])
		text = ""
		if get_course(user) == "none" or get_loc(user) == "none" or get_gender(user) == "none" or get_interests(user) == "none":
			text = "\n\n📝 Remember to setup your profile infos and interests 🧩!\n\n⚙️ You can do it from the settings"
			kb = types.InlineKeyboardMarkup([[settings_button(lang), new_chat_button(lang)]])
		
		msg = await app.send_message(user.id, t(m["chat_forceclosed"]+text, lang), reply_markup=kb)
		await save_inline(user, msg)
		if(list(conversations.keys()).count(convo) != 0):
			if (conversations[convo]["reported"] == True):
				i = -1
				for data in conversations[convo]["messages"]:
					i += 1
					try:
						forwarded = await app.forward_messages(storage_group, data["chat_id"], data["message_id"])
						new_data = {
							"message_id": forwarded.id,
							"chat_id": storage_group
						}
						conversations[convo]["messages"][i] = new_data
					except Exception as e:
						print(f"Could not forward messages of reported chat: {e}")
						
				
				
		
async def remove_inline(chatid, messageid):
	try:
		await app.edit_message_reply_markup(int(chatid), int(messageid))
	except Exception as e:
		print(f"Error removing inlinekeyboard: {e}")
		
async def save_inline(user, message):
	if not is_new_user(user):
		if storage["users"][f"{user.id}"]["last_inline"] and storage["users"][f"{user.id}"]["last_inline"] != f"{message.id}":
			await remove_inline(user.id, storage["users"][f"{user.id}"]["last_inline"])
		storage["users"][f"{user.id}"]["last_inline"] = f"{message.id}"
	
async def leave_chat(user, reported=False):
	matched_id = get_matched(user)
	matched = await app.get_users(matched_id)
	
	set_status(user, "idle")
	storage["users"][f"{user.id}"]["matched"] = None
	lang = get_lang(user)
	notice = "⬆️ CONVERSATION ENDED ⬆️"
	if reported == True:
		notice += "\n\n⚠️ This conversation has been reported.\n🆘 If you wish to contact us, use: @PoliMeetSupportBot."
	
	await app.send_message(user.id, t(notice, lang))
	
	text = ""
	kb = types.InlineKeyboardMarkup([[cancel_button(lang), new_chat_button(lang)]])
	if get_course(user) == "none" or get_loc(user) == "none" or get_gender(user) == "none" or get_interests(user) == "none":
		text = "\n\n📝 Remember to setup your profile infos and interests 🧩!\n\n⚙️ You can do it from the settings"
		kb = types.InlineKeyboardMarkup([[settings_button(lang), new_chat_button(lang)]])
	msg = await app.send_message(user.id, t(m["chat_left"]+text, lang), reply_markup=kb)
		
	await save_inline(user, msg)
	await force_leave(matched)

async def settings(user: types.User, msg: types.Message):
	lang = get_lang(user)
	
	kb = types.InlineKeyboardMarkup([
		[gender_button(lang), loc_button(lang)],
		[course_button(lang), interests_button(lang)],
		[cancel_button(lang)]
	])
	
	await msg.edit_text(t(m["settings_message"], lang), reply_markup=kb)

async def settings_loc(user: types.User, msg: types.Message):
	lang = get_lang(user)
	
	kb = loc_keyboard(lang)
	
	await msg.edit_text(t(m["loc_message"], lang).format(get_loc(user)), reply_markup=kb)
	
async def settings_gender(user: types.User, msg: types.Message):
	lang = get_lang(user)
	
	kb = gender_keyboard(lang)
	
	await msg.edit_text(t(m["gender_message"], lang).format(get_gender(user)), reply_markup=kb)

async def settings_course(user: types.User, msg: types.Message):
	lang = get_lang(user)
	
	kb = course_keyboard(lang)
	
	await msg.edit_text(t(m["course_message"], lang).format(get_course(user)), reply_markup=kb)


@app.on_message(filters.command("start"))
async def send_start(client, message):
	user = message.from_user
	save_user(message.from_user)

	ref = "none"
	if len(message.command) == 2:
		ref = message.command[1]
		if ref in storage["stats"].keys():
			storage["stats"][ref] += 1

	await notify_admins(f"User {user.mention} started the bot with ref {ref}.")
	
	if maintenance == True:
		await message.reply("Hi Guys we’re sorry but the bot will need some maintenance, we we’ll notify you as soon as it works again 🫶🏻 lots of love")
	else:
		if get_matched(user):
			await leave_chat(user)
		else:
			if get_status(user) == "searching":
				if f"{user.id}" in storage["searching"]:
					storage["searching"].remove(f"{user.id}")
					set_status(user, "idle")
			elif get_status(user) == "setting_interest":
				set_status(user, "idle")
			msg = await message.reply("starting...")
			await welcome(user, msg)


@app.on_message(filters.command("forward"))	
async def forward_reply(client, message):
	user = message.from_user
	if user.id in admins:
		if message.reply_to_message_id:
			content = await app.get_messages(user.id, message.reply_to_message_id)
			await broadcast_copy(content)
		else:
			await message.reply("Errore:\nInvia questo comando in risposta all'annuncio da inviare a tutti gli utenti!")
	
async def save_message(convo, message):
#	mess = repr(message)
#	Instead of storing the txt repr of the message, there are 2 ways to store the messages more cleanly:
#	1 - Saving the ID of the message in the conversation of a user and the bot. This is the best way privacy-wise, as a user can delete their chat with the bot and clean their data from the database.
#	2 - Forwarding a message to a private group the bot only has access to (and another user), and store the ID of that forwarded message. Doing so, messages can't be deleted from the database from users.
#	Currently, a mix of 1 and 2 is used: normal conversations are stored by IDs in their private chat, but when a conversation is reported the messages are forwarded to a group so that those are saved and admins can decide on whether to ban a user or not.
	saved = message
	data = {
		"message_id": saved.id,
		"chat_id": saved.from_user.id
	}
	if convo in list(conversations.keys()):
		conversations[convo]["messages"].append(data)
	else:
		conversations[f"{convo}"] = {
			"messages": [data],
			"users": [message.from_user.id, get_matched(message.from_user)],
			"reported": False
		}
		
	
@app.on_message(filters.command("get_blocks"))
async def get_blocks(client, message):
	if message.from_user.id in admins:
		total = len(list(storage["users"].keys()))
		blocked = 0
		for userid in list(storage["users"].keys()):
			try:
				msg = await app.send_message(int(userid), "ping")
				await msg.delete()
				storage["users"][userid]["stopped"] = False
			except:
				blocked += 1
				storage["users"][userid]["stopped"] = True		
		await message.reply(f"👥 Total users: {total}\n🚫 Blocked: {blocked}\n✅ Active: {total-blocked}")		
	
@app.on_message(filters.command("admin"))
async def admin(client, message):
	user = message.from_user
	if user.id in admins:
		msg = await message.reply("starting...")
		await list_conversations(user, msg, "0")
		
		
@app.on_message(filters.command("clear_conversations"))
async def clear_conversations(client, message):
	user = message.from_user
	if user.id in admins:
		count = 0
		deleted = []
		msg = await message.reply("🧹 Cleaning up conversations...")
		for convo in list(conversations.keys()):
			if len(conversations[convo]["messages"]) <= 5:
				count += 1
				deleted.append(convo)
		for id in deleted:
			if id in list(conversations.keys()):
				conversations.pop(id)			
		await msg.edit_text(f"🧹 Cleaned {count} conversations.")
	
@app.on_message()
async def on_message(client, message):
	if maintenance == True:
		await message.reply("Hi Guys we’re sorry but the bot will need some maintenance, we we’ll notify you as soon as it works again 🫶🏻 lots of love")
	else:
		user = message.from_user
		status = get_status(user)
		if "matched" in status:
			convo = status.split(".")[1]
			matched = get_matched(user)
			try:
				await app.copy_message(int(matched), message.from_user.id, message.id)
				await save_message(convo, message)
			except Exception as e:
				print(f"Error copying message: {e}")
				await force_leave(user)
		elif status == "setting_interest":
			lang = get_lang(message.from_user)
			if message.text and len(message.text) <= 100 and not message.entities:
				content = message.text
				storage["users"][f"{message.from_user.id}"]["interests"] = content
				set_status(message.from_user, "idle")
				await message.reply(t("✅ Interests set! ✅", lang))
				msg = await message.reply("starting...")
				await settings(message.from_user, msg)
				await save_inline(message.from_user, msg)
			else:
				await message.reply(t("🚫 Error: make sure your message follows these requirements:\n\n📣 No advertising (no links or tags)\n🔎 Short (less than 100 characters)\n📝 Text only (no media attached)\n\nSend now your interests.", lang))
	

@app.on_callback_query()
async def query_handler(client, call):
	user = call.from_user
	status = get_status(user)
	msg = call.message
	if call.data == "new_chat":
		await try_match(user, call.message)
	elif call.data == "cancel":
		if status == "idle":
			await welcome(user, call.message)
		elif status == "searching":
			storage["searching"].remove(f"{user.id}")
			set_status(user, "idle")
			await welcome(user, call.message)
		elif "matched" in status:
			await leave_chat(user)
		elif "setting_interest" in status:
			set_status(user, "idle")
			await welcome(user, call.message)
	elif call.data == "leave":
		if "matched" in status:
			await leave_chat(user)
	elif "report" in call.data:
		if "matched" in status:
			convo = call.data.split(".")[1]
			conversations[convo]["reported"] = True
			await notify_admins(f"⚠️ Conversation {convo} has been reported.")
			await leave_chat(user, True)
	elif call.data == "settings" and status == "idle":
		await settings(user, msg)
	elif call.data == "gender" and status == "idle":
		await settings_gender(user, msg)
	elif call.data == "course" and status == "idle":
		await settings_course(user, msg)
	elif call.data == "loc" and status == "idle":
		await settings_loc(user, msg)
	elif call.data == "language" and status == "idle":
		await switch_lang(user, msg)
	elif "set" in call.data and status == "idle":
		args = call.data.split(".")
		try:
			storage["users"][f"{user.id}"][f"{args[1]}"] = args[2]
			if args[1] != "language":
				await settings(user, msg)
			else:
				await welcome(user, msg)
		except Exception as e:
			print(f"Could not set field {args[1]} of {user.id} to {args[2]} ({e})")
	elif "list_conversation" in call.data and status == "idle":
		convo = call.data.split(".")[1]
		await list_conversations(user, msg, convo)
	elif "show_conversation" in call.data and status == "idle":
		convo = call.data.split(".")[1]
		await msg.delete()
		await show_conversation(user, convo)
	elif "delete_conversation" in call.data and status == "idle":
		convo = call.data.split(".")[1]
		await msg.delete()
		await delete_conversation(user, convo)
	elif call.data == "interests" and status == "idle":
		set_status(user, "setting_interest")
		await set_interests(user, msg)
	
	

async def set_interests(user: types.User, msg: types.Message):
	lang = get_lang(user)
	kb = types.InlineKeyboardMarkup([[cancel_button(lang)]])
	await msg.edit_text(t(m["interests_message"], lang).format(get_interests(user)), reply_markup=kb)
	
	
def split_list(lst, max_len=200):
	return [lst[i:i+max_len] for i in range(0, len(lst), max_len)]
	
async def show_conversation(user: types.User, id):
	if conversations[id]["reported"] == True:
			
		for msg in conversations[id]["messages"]:
			try:
				await app.forward_messages(user.id, msg["chat_id"], msg["message_id"])
			except Exception as e:
				await app.send_message(user.id, "A message in this conversation could not be found")
				print(f"Could not find message {e}")
	else:
		await app.send_message(user.id, "🚫 ERRORE\nQuesta conversazione non è stata ⚠️ segnalata, quindi non può essere vista.")
	msg = await app.send_message(user.id, "starting...")
	await list_conversations(user, msg, id)
	
async def delete_conversation(user: types.User, id):

	if id in list(conversations.keys()):
		conversations.pop(id)
	msg = await app.send_message(user.id, "starting...")
	await list_conversations(user, msg, "0")
	
	
async def list_conversations(user: types.User, msg: types.Message, id):
	total = storage["convo"]
	id = str(id)
	if total == 0 or len(list(conversations.keys())) == 0:
		await msg.edit_text("No conversations avaiable.")
	else:
		conv_keys = list(conversations.keys())
		if id in conv_keys:
			pos = conv_keys.index(id)
		else:
			pos = 0
			id = conv_keys[0]
			
		if pos == 0:
			prev_id = conv_keys[len(conv_keys)-1]
		else:
			prev_id = conv_keys[pos-1]
			
			
		if pos == len(conv_keys)-1:
			succ_id = conv_keys[0]
		else:
			succ_id = conv_keys[pos+1]
		
		try:
			user1 = await app.get_users(conversations[id]["users"][0])
			user1 = user1.mention
		except:
			user1 = conversations[id]["users"][0]
			
		try:
			user2 = await app.get_users(conversations[id]["users"][1])
			user2 = user2.mention
		except:
			user2 = conversations[id]["users"][1]


		kb = types.InlineKeyboardMarkup([
			[
				types.InlineKeyboardButton("👁 MOSTRA 👁", callback_data = f"show_conversation.{id}"),
				types.InlineKeyboardButton("🚫 ELIMINA 🚫", callback_data = f"delete_conversation.{id}")
			
			],
			[
				types.InlineKeyboardButton(f"{prev_id} ◀️", callback_data = f"list_conversation.{prev_id}"),
				types.InlineKeyboardButton(f"▶️ {succ_id}", callback_data = f"list_conversation.{succ_id}")
			]
		])
		reported = conversations[id]["reported"]
		await msg.edit_text(f"Conversation ID: {id}\n{user1} and {user2}\n⚠️ Reported: {reported}", reply_markup = kb)
	



	
@app.on_raw_update()
async def update_handler(client, update, users, chats):
	if (type(update) == pyrogram.raw.types.UpdateBotStopped):
		storage["users"][f"{update.user_id}"]["stopped"] = update.stopped
		if update.stopped == True:
			user = await app.get_users(update.user_id)
			await notify_admins(f"User {user.mention} has stopped the bot ):")





app.stop = save_storage
	
app.run()
	
	
	
