from telethon import events, TelegramClient
from telethon.tl.functions.messages import GetMessagesRequest, DeleteMessagesRequest
from telethon.tl.functions.contacts import BlockRequest, UnblockRequest
from telethon.tl.functions.account import UpdateProfileRequest, CreateBusinessChatLinkRequest, GetBusinessChatLinksRequest, DeleteBusinessChatLinkRequest
from telethon.tl.functions.photos import DeletePhotosRequest, UploadProfilePhotoRequest
from telethon.tl.functions.channels import (CreateForumTopicRequest, GetForumTopicsByIDRequest, DeleteTopicHistoryRequest)
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument, PeerUser, ChannelParticipantsKicked, InputPhoto, InputBusinessChatLink, MessageEntityTextUrl, MessageEntityBold, MessageEntityItalic, MessageEntityCustomEmoji
import asyncio, json, sqlite3, os, uuid, random, requests, unicodedata, pickle
from logging import basicConfig, ERROR
import re as preg
from telethon.extensions import html
from telethon import types

shugarch = '@ls_kl'
autoSendCH = '@ls_kl'
admins = (703859331, )
spy_ch = -1002346803926
shugars = ('Girlwhats','Girlwhatone','haiwo1','Lpsiiw','Fantokw','YupIalja','Ghowowq','Vbmmo','Jaolpw','Hjlao0w','FAtyops','Banopas','Golionsk','Xxnspiw','GoliHo','FAsiGirlp','GodGirlp','erioksk', )
myid = 0
groupid = -1001857101549
convturn = False
wlcturn = False
sending_turn = False

client = TelegramClient(
    "session",
    2530547,
    "064b65866cd134e579424153177701dd"
)
botclient = TelegramClient(
    "botsession",
    2530547,
    "064b65866cd134e579424153177701dd"
)

try:
    open('.lastid.txt','x').close()
    open('.notice_time.txt','x').close()
    open('.notice_msg.txt','x').close()
    open('wlc.txt','x').close()
    os.mkdir('voices')
except FileExistsError:
    pass

sql_connect = sqlite3.connect("myboard.session")
my_cursor = sql_connect.cursor()
my_cursor.execute("""CREATE TABLE IF NOT EXISTS `msgreplies`(
`id` INTEGER PRIMARY KEY AUTOINCREMENT,
`text` TEXT NOT NULL,
`reply` TEXT NOT NULL,
`type` TEXT NOT NULL,
`obj` BLOB
)""")
my_cursor.execute("""CREATE TABLE IF NOT EXISTS `business_links`(
`id` INTEGER PRIMARY KEY AUTOINCREMENT,
`target` TEXT NOT NULL,
`title` TEXT NOT NULL,
`message` TEXT NOT NULL
)""")
my_cursor.execute("""CREATE TABLE IF NOT EXISTS `voicereplies`(
`id` INTEGER PRIMARY KEY AUTOINCREMENT,
`text` TEXT NOT NULL,
`voice` TEXT NOT NULL,
`caption` TEXT
)""")
#my_cursor.execute("DROP TABLE `users_conv`")
my_cursor.execute("""CREATE TABLE IF NOT EXISTS `users_conv`(
`id` INTEGER PRIMARY KEY AUTOINCREMENT,
`userid` BIGINT NOT NULL,
`chat_id` BIGINT NOT NULL,
`pv_msgid` INT NOT NULL,
`gp_msgid` INT NOT NULL,
`tpid` INT DEFAULT 0,
`in_conv` BOOLEAN DEFAULT 1
)""")
my_cursor.execute("""CREATE TABLE IF NOT EXISTS `msgreplies_media`(
`id` INTEGER PRIMARY KEY AUTOINCREMENT,
`text` TEXT NOT NULL,
`sendor_id` BIGINT NOT NULL,
`reply_id` TEXT NOT NULL,
`timer` INT NOT NULL
)""")
my_cursor.execute("""CREATE TABLE IF NOT EXISTS `pv_locks`(
`id` INTEGER PRIMARY KEY AUTOINCREMENT,
`user` BIGINT NOT NULL,
`is_lock` TEXT NOT NULL
)""")
my_cursor.execute("""CREATE TABLE IF NOT EXISTS `welcomes`(
`id` INTEGER PRIMARY KEY AUTOINCREMENT,
`user` BIGINT NOT NULL
)""")
sql_connect.commit()

# Logging
basicConfig(
    level=ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='./Telethon.log'
)

async def checkUserWlc(user):
    getuser = my_cursor.execute(f"SELECT * FROM `pv_locks` WHERE `user` = {user}").fetchone()
    if getuser == None:
        return False
    else:
        return True


async def convertNums(text):
    text = text.replace('۰', '0')
    text = text.replace('۱', '1')
    text = text.replace('۲', '2')
    text = text.replace('۳', '3')
    text = text.replace('۴', '4')
    text = text.replace('۵', '5')
    text = text.replace('۶', '6')
    text = text.replace('۷', '7')
    text = text.replace('۸', '8')
    text = text.replace('۹', '9')

    return text

async def setShugar(user):
    getf = open('shugar.txt', 'w')
    getf.write(user)
    getf.close()

    return

async def getShugar():
    getf = open('shugar.txt', 'r')
    getsh = getf.read()
    getf.close()

    return getsh

async def setNot(msg):
    getf = open('.notice_msg.txt', 'w')
    getf.write(msg)
    getf.close()

    return

async def getNot():
    getf = open('.notice_msg.txt', 'r')
    getsh = getf.read()
    getf.close()

    return getsh

async def setNotTimer(timer):
    getf = open('.notice_time.txt', 'w')
    getf.write(timer)
    getf.close()

    return

async def getNotTimer():
    getf = open('.notice_time.txt', 'r')
    getsh = getf.read()
    getf.close()

    return getsh

async def setLastMsgID(ID):
    getf = open('.lastid.txt', 'w')
    getf.write(ID)
    getf.close()

    return

async def getLastMsgID():
    getf = open('.lastid.txt', 'r')
    getsh = getf.read()
    getf.close()

    return getsh

async def addToUsers(user):
    getuser = my_cursor.execute(f"SELECT * FROM `pv_locks` WHERE `user` = {user}").fetchone()
    if getuser == None:
        my_cursor.execute(f"INSERT INTO `pv_locks` (`user`, `is_lock`) VALUES ({user}, 'no')")
        sql_connect.commit()

async def checkUser(user):
    getuser = my_cursor.execute(f"SELECT * FROM `pv_locks` WHERE `user` = {user}").fetchone()
    if getuser != None:
        return getuser[2]

async def lockUser(user):
    getuser = my_cursor.execute(f"SELECT * FROM `pv_locks` WHERE `user` = {user} AND `is_lock` = 'no'").fetchone()
    if getuser != None:
        my_cursor.execute(f"UPDATE `pv_locks` SET `is_lock` = 'yes' WHERE `user` = {user}")
        sql_connect.commit()
        return True
    else:
        return False

async def unlockUser(user):
    getuser = my_cursor.execute(f"SELECT * FROM `pv_locks` WHERE `user` = {user} AND `is_lock` = 'yes'").fetchone()
    if getuser != None:
        my_cursor.execute(f"UPDATE `pv_locks` SET `is_lock` = 'no' WHERE `user` = {user}")
        sql_connect.commit()
        return True
    else:
        return False
    
async def addToSendMedia(msg, from_me, replyid, timer):
    my_cursor.execute(f"INSERT INTO `msgreplies_media` (`text`, `sendor_id`, `reply_id`, `timer`) VALUES ('{msg}', {from_me}, '{replyid}', {timer})")
    sql_connect.commit()
    return True

async def checkSendMedia(msg):
    getword = my_cursor.execute(f"SELECT * FROM `msgreplies_media`").fetchall()
    getword = my_cursor.execute(f"SELECT * FROM `msgreplies_media` WHERE `text` = '{msg}'").fetchall()
    if len(getword) != 0:
        return getword
    else:
        return False

async def RemoveToSendsMedia(msg, repid):
    additional_str = ''
    if repid != None:
        additional_str = f" AND `reply_id` = '{repid}'"
    getword = my_cursor.execute(f"SELECT * FROM `msgreplies_media` WHERE `text` = '{msg}'{additional_str}").fetchone()
    if getword == None:
        return False
    else:
        my_cursor.execute(f"DELETE FROM `msgreplies_media` WHERE `text` = '{msg}'{additional_str}")
        sql_connect.commit()
        return True

async def addToSends(msg, reply, obj):
    getword = my_cursor.execute(f"SELECT * FROM `msgreplies` WHERE `text` = '{msg}' AND `type` = 'send'").fetchone()
    if getword == None:
        obj = pickle.dumps(obj)
        my_cursor.execute(f"INSERT INTO `msgreplies` (`text`, `reply`, `type`, `obj`) VALUES (?, ?, ?, ?)", (msg, reply, 'send', obj))
        sql_connect.commit()
        return True
    else:
        return False

async def checkSends(msg):
    getword = my_cursor.execute(f"SELECT * FROM `msgreplies` WHERE `text` = '{msg}' AND `type` = 'send'").fetchone()
    if getword != None:
        return [getword[2], getword[4]]
    else:
        return False

async def RemoveToSends(msg):
    getword = my_cursor.execute(f"SELECT * FROM `msgreplies` WHERE `text` = '{msg}' AND `type` = 'send'").fetchone()
    if getword == None:
        return False
    else:
        my_cursor.execute(f"DELETE FROM `msgreplies` WHERE `text` = '{msg}' AND `type` = 'send'")
        sql_connect.commit()
        return True

async def addToEdits(msg, reply, obj):
    getword = my_cursor.execute(f"SELECT * FROM `msgreplies` WHERE `text` = '{msg}' AND `type` = 'edit'").fetchone()
    if getword == None:
        obj = pickle.dumps(obj)
        my_cursor.execute(f"INSERT INTO `msgreplies` (`text`, `reply`, `type`, `obj`) VALUES (?, ?, ?, ?)", (msg, reply, 'edit', obj))
        sql_connect.commit()
        return True
    else:
        return False

async def checkEdits(msg):
    getword = my_cursor.execute(f"SELECT * FROM `msgreplies` WHERE `text` = '{msg}' AND `type` = 'edit'").fetchone()
    if getword != None:
        return [getword[2], getword[4]]
    else:
        return False

async def RemoveToEdits(msg):
    getword = my_cursor.execute(f"SELECT * FROM `msgreplies` WHERE `text` = '{msg}' AND `type` = 'edit'").fetchone()
    if getword == None:
        return False
    else:
        my_cursor.execute(f"DELETE FROM `msgreplies` WHERE `text` = '{msg}' AND `type` = 'edit'")
        sql_connect.commit()
        return True

async def unbanUsers(event, chatt):
    nums = 0
    try:
        async for user in client.iter_participants(chatt, filter=ChannelParticipantsKicked):
            await client.edit_permissions(chatt, user.id)
            nums += 1
            await asyncio.sleep(2)
    except Exception as exx:
        await client.send_message('me', f"error in unban func:  {exx}")

    await event.edit(f'آنبن {nums} کاربر با موفقیت انجام شد')
    return

async def autoSendToChannel():
    while True:

        if globals()['sending_turn'] == False:
            break

        getsleep = await getNotTimer()
        getsleep = int(getsleep)
        getnot = await getNot()

        getlast = await getLastMsgID()
        if getlast.isnumeric():
            getlast = int(getlast)
            await client.delete_messages(autoSendCH, getlast)

        gett = await client.send_message(autoSendCH, getnot)
        await setLastMsgID(str(gett.id))

        await asyncio.sleep(getsleep)

@client.on(events.MessageDeleted(func = lambda ev: ev.is_private))
async def userDeleteHandler(event):
    print(event)
    
@client.on(events.NewMessage(func = lambda ev: ev.is_channel))
async def groupHandler(event):
    #print(event)
    text = event.text
    is_out = event.message.out
    chat_id = event.chat_id
    if groupid == chat_id and globals()['convturn'] == True:
        if text.lower() == '/end':
            gett = await client(
                GetForumTopicsByIDRequest(event.input_chat, [event.reply_to_msg_id])
            )
            topic_name = gett.topics[0].title
            topicuser = topic_name.split('-')[-1]
            my_cursor.execute(f"UPDATE `users_conv` SET `in_conv` = 0 WHERE `chat_id` = {chat_id} AND `userid` = '{topicuser}'")
            sql_connect.commit()
            await client(
                DeleteTopicHistoryRequest(event.input_chat, event.reply_to_msg_id)
            )
        elif text.lower() == '/block':
            await client.send_message(chat_id, message = "کاربر با موفقیت بلاک شد", reply_to=event.id)
            repid = event.reply_to_msg_id
            gett = await client(
                GetForumTopicsByIDRequest(event.input_chat, [repid])
            )
            topic_name = gett.topics[0].title
            topicuser = topic_name.split('-')[-1]
            getuserchat = my_cursor.execute(f"SELECT * FROM `users_conv` WHERE `userid` = {topicuser} AND `tpid` = {repid} AND `chat_id` = {chat_id} AND `in_conv` = 1 AND `tpid` != 0").fetchone()
            await client(
                BlockRequest(getuserchat[1], )
            )
        elif text.lower() == '/unblock':
            await client.send_message(chat_id, message = "کاربر با موفقیت آنبلاک شد", reply_to=event.id)
            repid = event.reply_to_msg_id
            gett = await client(
                GetForumTopicsByIDRequest(event.input_chat, [repid])
            )
            topic_name = gett.topics[0].title
            topicuser = topic_name.split('-')[-1]
            getuserchat = my_cursor.execute(f"SELECT * FROM `users_conv` WHERE `userid` = {topicuser} AND `tpid` = {repid} AND `chat_id` = {chat_id} AND `in_conv` = 1 AND `tpid` != 0").fetchone()
            await client(
                UnblockRequest(getuserchat[1], )
            )
        elif is_out == False:
            repid = event.reply_to_msg_id
            gett = await client(
                GetForumTopicsByIDRequest(event.input_chat, [repid])
            )
            if hasattr(gett.topics[0], 'title'):
                topic_name = gett.topics[0].title
                topicuser = topic_name.split('-')[-1]
                getuserchat = my_cursor.execute(f"SELECT * FROM `users_conv` WHERE `userid` = {topicuser} AND `tpid` = {repid} AND `chat_id` = {chat_id} AND `in_conv` = 1 AND `tpid` != 0").fetchone()
                if event.media == None:
                    await client.send_message(getuserchat[1], message = text)
                else:
                    try:
                        await client.send_file(getuserchat[1], file = event.media, caption=text)
                    except TypeError:
                        await client.send_message(getuserchat[1], message = text)
            else:
                await client.send_message(chat_id, message = "لطفا پیام مورد نظر را به صورت خام بفرستید و روی پیام خاصی ریپلی نکنید.", reply_to=event.id)


    else:
        
        busis = my_cursor.execute(f"SELECT * FROM `business_links`").fetchall()

        for link in busis:
            if link[1] in text:
                getcode = text.split("\n")[2].replace('کد','').replace('کد ', '')
                target = link[1]
                title = link[2]
                message = link[3].replace('#code', getcode)

                createBusiness = await client(
                    CreateBusinessChatLinkRequest(
                        link = InputBusinessChatLink(
                            title = title,
                            message = message
                        )
                    )
                )       

                getlink = createBusiness.link
                chatt = chat_id
                msg_id = event.id
                entities = event.entities
                message = text

                offset = message.index(target)+len(target)
                length = len(target)
                
                for ent, txt in event.get_entities_text():
                    if txt == target:
                        offset = ent.offset
                        length = ent.length

                        break

                new_obj = MessageEntityTextUrl(
                    offset = offset,
                    length = length,
                    url = getlink
                )
                entities.append(new_obj)

                await client.edit_message(chatt, msg_id, message, formatting_entities=entities)

                break


@client.on(events.MessageEdited(func = lambda ev: ev.is_private))
async def userEditHandler(event):
    msgid = event.id
    text = event.text
    user_id = event.chat_id
    if event.text:
        getuserchat = my_cursor.execute(f"SELECT * FROM `users_conv` WHERE `userid` = {user_id} AND  `pv_msgid` = {msgid} AND `in_conv` = 1 AND `tpid` != 0").fetchone()
        if getuserchat != None:
            await client.edit_message(getuserchat[2], message = getuserchat[4], text=text)

@client.on(events.NewMessage(func = lambda ev: ev.is_private))
async def userHandler(event):
    text = event.text
    getwords = my_cursor.execute(f"SELECT * FROM `voicereplies` WHERE `text` = '{text}' LIMIT 1").fetchone()
    msgid = event.id
    user_id = event.chat_id
    is_out = event.message.out
    fromwho = event.sender_id
    replyid = event.reply_to_msg_id
    myid = globals()['myid']
    getuser = await client.get_entity(fromwho)

    if event.photo != None:
        await client.download_media(event.photo, open(f"./photo.jpg", 'wb'))
        try:
            await botclient.send_file(spy_ch, await botclient.upload_file(f'./photo.jpg'), caption=f"From User ==> {getuser.first_name} - {user_id}\n\n{text}")
        except Exception as ex:
            print(f'error: {ex}')
        os.system(f"rm -rf ./photo.jpg")
    elif text != None:
        try:
            await botclient.send_message(spy_ch, f"From User ==> {getuser.first_name} - {user_id}\n\n{text}")
        except Exception as ex:
            print(f'error: {ex}')

    if myid == 0:
        getme = await client.get_me()
        globals()['myid'] = getme.id
        return

    if myid != fromwho:
        if globals()['wlcturn'] == True:
            chkwlc = await checkUserWlc(fromwho)
            if chkwlc == False:
                getff = open('wlc.txt', 'r')
                getwlc = getff.read()
                getff.close()
                try:
                    await event.reply(getwlc)
                except:
                    pass

        await addToUsers(fromwho)
        getuser = await checkUser(fromwho)
        if getuser == 'yes':
            await event.delete()

        sending = await checkSends(text)
        if sending != False:
            deserialized_list = pickle.loads(sending[1])
            await event.reply(sending[0], formatting_entities=deserialized_list)

    if user_id in admins:

        if preg.search("^\/set_bio\s(.{1,70})$", text):
            getbio = preg.search("^\/set_bio\s(.{1,70})$", text)[1]
            await client(
                UpdateProfileRequest(about=getbio)
            )
            await client.send_message(user_id, "ok, BioGraphy is Done.")

        elif preg.search("^\/set_name\s(.{1,70})$", text):
            getname = preg.search("^\/set_name\s(.{1,70})$", text)[1]
            await client(
                UpdateProfileRequest(first_name=getname)
            )
            await client.send_message(user_id, "ok, FirstName is Done.")

        elif preg.search("^\/set_profile$", text) and event.photo != None:
            await client.download_media(event.photo, open(f"./photo.jpg", 'wb'))
            photos = await client.get_profile_photos('me')
            ids = []
            for p in photos:
                ids.append(InputPhoto(
                    id=p.id,
                    access_hash=p.access_hash,
                    file_reference=p.file_reference
                ))
            await client(DeletePhotosRequest(
                id=ids
            ))
            await client(UploadProfilePhotoRequest(
                file = await client.upload_file('./photo.jpg')
            ))
            os.system(f"rm -rf ./photo.jpg")
        
    elif event.photo != None and user_id not in admins:
        getuser = await client.get_entity(user_id)
        await client.download_media(event.photo, open(f"./photo.jpg", 'wb'))
        await botclient.send_file(-1001963133549, await botclient.upload_file(f'./photo.jpg'), caption=f"From User ==> {getuser.username} - {user_id}")
        os.system(f"rm -rf ./photo.jpg")

    if event and globals()['convturn'] == True and is_out == False:
        getconv = my_cursor.execute(f"SELECT * FROM `users_conv` WHERE `chat_id` = {groupid} AND `userid` = {user_id} LIMIT 1").fetchone()
        getconv2 = my_cursor.execute(f"SELECT * FROM `users_conv` WHERE `chat_id` = {groupid} AND `userid` = {user_id} AND `in_conv` = 1 LIMIT 1").fetchone()
        if getconv == None or getconv2 == None:
            getuser = await event.get_sender()
            getgpconv = await client(
                CreateForumTopicRequest(groupid, f"{getuser.first_name}-{user_id}", random_id=user_id)
            )
            if event.media == None:
                getmsg = await client.send_message(groupid, message = text, reply_to=getgpconv.updates[0].id)
            else:
                getmsg = await client.send_file(groupid, file = event.media, reply_to=getgpconv.updates[0].id, caption=text)
            my_cursor.execute(f"INSERT INTO `users_conv` (`userid`, `chat_id`, `gp_msgid`, `pv_msgid`, `tpid`) VALUES ({user_id}, {groupid}, {getmsg.id}, {msgid}, {getgpconv.updates[0].id})")
            sql_connect.commit()
        else:
            getlastchat = my_cursor.execute(f"SELECT * FROM `users_conv` WHERE `userid` = {user_id} AND `chat_id` = {groupid} AND `in_conv` = 1 AND `tpid` != 0").fetchone()
            if event.media == None:
                getmsg = await client.send_message(groupid, message = text, reply_to=getlastchat[5])
            else:
                getmsg = await client.send_file(groupid, file = event.media, reply_to=getlastchat[5], caption=text)
            my_cursor.execute(f"INSERT INTO `users_conv` (`userid`, `chat_id`, `gp_msgid`, `pv_msgid`, `tpid`) VALUES ({user_id}, {groupid}, {getmsg.id}, {msgid}, {getlastchat[5]})")
            sql_connect.commit()
            
    elif text == 'نگاه کنم بهتون خبر میدم':
        await asyncio.sleep(120)
        await event.respond('منتظرم')

    elif preg.search('^\#\w+$', text):
        getuser = await client.get_entity(user_id)
        await event.delete()
        await client.send_message('me', f"چت فیک برای کاربر حاضر شد اسکرین بگیرید {text} در پیوی : @{getuser.username}", parse_mode='html')

    if is_out == True:

        editing = await checkEdits(text)
        sending2 = await checkSendMedia(text)

        if sending2 != False:
            for row in sending2:
                getmenow = await client(
                    GetMessagesRequest(id=[int(row[3]), ])
                )
                await client.send_file(user_id, file = getmenow.messages[0].media, caption= getmenow.messages[0].message, ttl=int(row[4]))
    
        elif text.lower() == "/ping":
            await event.edit("**Pong**")
    

        elif text.lower() == "/help":
            await event.edit('''راهنمای استفاده از ربات:

تست روشن بودن ربات:
/ping

دیدن راهنمای دستورات:
/help

حذف متن ست شده برای ادیت:
/del_editor {msg}

افزودن متن برای ادیت:
/set_editor {msg} {edit}

حذف متن ست شده برای پاسخ خودکار:
/del_sendor {msg}

افزودن متن برای پاسخ خودکار:
/set_sendor {msg} {ریپلی روی پاسخ}

حذف متن ست شده به همراه عکس های پاسخی ارسال به صورت عادی باعث حذف همه رسانها و ارسال به صورت ریپلی روی رسانه فقط اون رسانه از لیست دستورات این کلمه حذف میشود:
/del_pictext  {txt}

افزودن متن با پاسخ تصویری به همراه تایمر ریپلی روی رسانه مورد نظر:
/set_pictext {txt} {timer_second}

لیست متن پاسخ خودکار ها:
/sendor_list

لیست متن ادیت خودکار ها:
/editor_list

قفل پیوی کاربر:
/lock

بازکردن پیوی کاربر:
/unlock

ثبت ویس برای پاسخ، ریپلی کنید:
/setvoice userText
                             
حذف پاسخ های ثبت شده به عنوان ویس برای یک کلمه:
/delvoice userText

لیست ویس ها:
/voice_list
                             
حذف پیام های تکراری:
/delall {msg}

پاسخ پیام ها در گروه:
/convgp off|on

پاسخ اولیه:
/wlcmsg off|on

تنظیم متن ورود کاربر به پیوی:
/set_welcome yourtext

f ۲۱
سرچ در چنل یا چت مورد نظر با کد مشخص جای here از یوزرنیم چت استفاده کنید

ثبت نوتیف
/set_notice minute msg

خاموش روشن کردن نوتیف
/notice (on|off)
                             
/unban 182828282
انبن کاربران یک چت

افزودن فرمت لینک
/setlink target_id title message

حذف فرمت لینک             
/dellink title
                             
نمایش لینک ها
/link_formats                       
                                             
کنترل خارج از اکانت:

/set_bio تنظیم بیوگرافی

/set_name تنظیم نام
                             
/set_profile ارسال یک عکس و گذاشتن این دستور در کپشن ان

Developer: ''')

        elif editing != False:
            textt = editing[0]
            entities = pickle.loads(editing[1])
            await event.edit(textt, formatting_entities=entities)

        elif getwords != None:
            await event.delete()
            capt = getwords[3] if getwords[3] != '' else None
            await client.send_file(user_id, await client.upload_file(f'voices/{getwords[2]}'), caption=capt)


        elif text.lower() == '/link_formats':
            busis = my_cursor.execute(f"SELECT * FROM `business_links`").fetchall()

            strr = ""
            for link in busis:
                strr += f"target: {link[1]} | title: {link[2]} | message: {link[3]}\n"

            await event.edit(f"لیست لینک ها\n\n{strr}")


        elif preg.search("^\/[Dd][Ee][Ll][Ll][Ii][Nn][Kk]\s(\w+)$", text):
            srr = preg.sub("^\/[Dd][Ee][Ll][Ll][Ii][Nn][Kk]\s", '', text)

            busis = my_cursor.execute(f"SELECT * FROM `business_links` WHERE `title` = '{srr}' LIMIT 1").fetchone()

            if busis != None:
                my_cursor.execute(f"DELETE FROM `business_links` WHERE `title` = '{srr}'")

                await event.edit('با موفقیت حذف شد')

            else:

                await event.edit("یافت نشد")

        elif preg.search("^\/[Ss][Ee][Tt][Ll][Ii][Nn][Kk]\s(\@\w+)\s(\w+)\s(.+)", text, preg.DOTALL):
            srr = preg.search("^\/[Ss][Ee][Tt][Ll][Ii][Nn][Kk]\s(\@\w+)\s(\w+)\s(.+)", text, preg.DOTALL)
            target = srr[1]
            title = srr[2]
            message = srr[3]

            getBusiness = await client(GetBusinessChatLinksRequest())
            
            for link in getBusiness.links:
                if link.title == title:
                    await client(
                        DeleteBusinessChatLinkRequest(
                            slug = link.link
                        )
                    )

                    my_cursor.execute(f"DELETE FROM `business_links` WHERE `title` = '{title}'")
            

            my_cursor.execute(f"DELETE FROM `business_links` WHERE `target` = '{target}'")

            my_cursor.execute(f"INSERT INTO `business_links` (`target`, `title`, `message`) VALUES ('{target}', '{title}', '{message}')")
            sql_connect.commit()

            await event.edit("با موفقیت ثبت شد.")


        elif preg.search("^\/[Ee][Dd][Ii][Tt]\s(\d{1,3})\s(.+)", text, preg.DOTALL) and replyid != None:
            srr = preg.search("^\/[Ee][Dd][Ii][Tt]\s(\d{1,3})\s(.+)", text, preg.DOTALL)
            line = int(srr[1])-1
            new_msg = srr[2]

            getmsg = await client(GetMessagesRequest(
                id = [replyid,],
            ))
            getmsg = getmsg.messages[0].message
            getmsg = getmsg.split("\n")

            getmsg[line] = new_msg
            finall_msg = "\n".join(getmsg)

            await client.edit_message(user_id, replyid, finall_msg)


        elif preg.search("^\/[Nn][Oo][Tt][Ii][Cc][Ee]\s(on|off)", text):
            ftx = preg.search("^\/[Nn][Oo][Tt][Ii][Cc][Ee]\s(on|off)", text)
            turn = ftx[1]
            getturn = globals()['sending_turn']
            if turn == 'on':
                if getturn == False:
                    globals()['sending_turn'] = True
                    asyncio.create_task(autoSendToChannel())
                    await event.edit("روشن شد")
                else:
                    await event.edit("درحال حاضر روشن است")
            else:
                if getturn == True:
                    globals()['sending_turn'] = False
                    await event.edit("خاموش شد")
                else:
                    await event.edit("درحال حاضر خاموش است")

        elif preg.search("^\/[Ss][Ee][Tt]_[Nn][Oo][Tt][Ii][Cc][Ee]\s(\d{1,2})\s(.+)", text, preg.DOTALL):
            ftx = preg.search("^\/[Ss][Ee][Tt]_[Nn][Oo][Tt][Ii][Cc][Ee]\s(\d{1,2})\s(.+)", text, preg.DOTALL)
            await setNotTimer(ftx[1]*60)
            await setNot(ftx[2])

            await event.edit('ثبت شد')

        elif preg.search("^\/[Uu][Nn][Bb][Aa][Nn]\s(\d+)$", text):
            getsr = int(preg.search("^\/[Uu][Nn][Bb][Aa][Nn]\s(\d+)$", text)[1])

            await event.edit('in progress....')
            await unbanUsers(event, getsr)


        elif preg.search("^f\s(.+)$", text):
            sr = preg.search("^f\s(.+)$", text)
            chat = shugarch
            getcode = sr[1]
            arabic = '۰۱۲۳۴۵۶۷۸۹'
            english = '0123456789'
            translation_table = str.maketrans(english, arabic)
            translated_num = getcode.translate(translation_table)
            isfind = False

            async for msg in client.iter_messages(chat, search=getcode):
                if f"#کد_{getcode}" in msg.message:
                    await event.edit(msg.message)
                    isfind = True
                    break

            if isfind == False:
                async for msg in client.iter_messages(chat, search=translated_num):
                    if f"#کد_{translated_num}" in msg.message:
                        await event.edit(msg.message)
                        isfind = True
                        break

            if isfind == False:
                await event.edit("not found")


        elif text == 'ا':
            shuffles = sorted(shugars, key=lambda x: random.random())
            seted = False
            for randshugar in shuffles:
                async with client.conversation(randshugar) as conv:
                    await conv.send_message("injob?")
                    getmsg = await conv.get_response()
                    if getmsg.text == 'no':
                        seted = True
                        await setShugar(randshugar)
                        await event.delete()
                        await conv.cancel()
                        break
                    else:
                        await conv.cancel()
                        continue

            if seted == False:
                await event.edit("خطایی رخ داده است!")

        elif text == 'ت' and event.reply_to_msg_id != None:
            randshugar = await getShugar()
            try:
                await client.forward_messages(randshugar, [replyid, ], user_id)
            except Exception as exx:
                await event.edit(f'{exx}')
                return

        elif text == 'ب' and event.reply_to_msg_id != None:
            randshugar = await getShugar()
            try:
                word_site = "https://www.mit.edu/~ecprice/wordlist.10000"
                response = requests.get(word_site)
                txt = response.text
                my_words = txt.splitlines()
                myword = my_words[random.randint(0, (len(my_words)-1))]
                await client.send_message(randshugar, f"#{myword}")
                await client.forward_messages(randshugar, [replyid, ], user_id)
                await client.send_message(randshugar, 'سلام خانم این اقا داخل کانال فرم شمارو انتخاب کردند میخوان با شما اشنا بشن نظرتون چیه؟')
                await event.edit(f"مشخصاتتون ارسال شد\nآیدی شما: #{myword}")
            except Exception as exx:
                await event.edit(f'رسانه باید عکس باشد =>> {exx}')
                return


        elif preg.search(r"^\/[Cc][Oo][Nn][Vv][Gg][Pp]\s(off|on)$", text):
            ftext = preg.search(r"^\/[Cc][Oo][Nn][Vv][Gg][Pp]\s(off|on)$", text)[1]
            if ftext == 'on':
                if globals()['convturn'] == True:
                    await event.edit("درحال حاضر فعال است")
                else:
                    await event.edit("فعال شد")
                globals()['convturn'] = True
            else:
                if globals()['convturn'] == False:
                    await event.edit("درحال حاضر غیرفعال است")
                else:
                    await event.edit("غیرفعال شد")
                globals()['convturn'] = False

        elif preg.search(r"^\/[Ww][Ll][Cc][Mm][Ss][Gg]\s(off|on)$", text):
            ftext = preg.search(r"^\/[Ww][Ll][Cc][Mm][Ss][Gg]\s(off|on)$", text)[1]
            if ftext == 'on':
                if globals()['wlcturn'] == True:
                    await event.edit("درحال حاضر فعال است")
                else:
                    await event.edit("فعال شد")
                globals()['wlcturn'] = True
            else:
                if globals()['wlcturn'] == False:
                    await event.edit("درحال حاضر غیرفعال است")
                else:
                    await event.edit("غیرفعال شد")
                globals()['wlcturn'] = False

        elif preg.search(r"^\/[Ss][Ee][Tt][Vv][Oo][Ii][Cc][Ee]\s(.+)", text, preg.DOTALL) and event.reply_to_msg_id != None:
            repid = event.reply_to_msg_id
            ftext = preg.search(r"^\/[Ss][Ee][Tt][Vv][Oo][Ii][Cc][Ee]\s(.+)", text, preg.DOTALL)[1]
            getmsg = await client(GetMessagesRequest(
                id = [repid, ],
            ))
            getmsg = getmsg.messages[0]
            if getmsg.voice != None:
                getwords = my_cursor.execute(f"SELECT * FROM `voicereplies` WHERE `text` = '{ftext}' LIMIT 1")
                if getwords.fetchone() != None:
                    await event.edit("این متن پاسخ دارد لطفا متن دیگری انتخاب کنید")
                    return
                voicename = f"{uuid.uuid4()}.ogg"
                await client.download_media(getmsg.media, open(f"voices/{voicename}", 'wb'))
                capt = getmsg.message if getmsg.message != None else ''
                my_cursor.execute(f"INSERT INTO `voicereplies` (`text`, `voice`, `caption`) VALUES ('{ftext}', '{voicename}', '{capt}')")
                sql_connect.commit()
                await event.edit("ثبت شد")

        elif preg.search(r"^\/[Dd][Ee][Ll][Vv][Oo][Ii][Cc][Ee]\s(.+)", text, preg.DOTALL):
            repid = event.reply_to_msg_id
            ftext = preg.search(r"^\/[Dd][Ee][Ll][Vv][Oo][Ii][Cc][Ee]\s(.+)", text, preg.DOTALL)[1]
            
            getwords = my_cursor.execute(f"SELECT * FROM `voicereplies` WHERE `text` = '{ftext}' LIMIT 1").fetchone()
            if getwords == None:
                await event.edit("این متن پاسخ ندارد لطفا متن دیگری که در دیتابیس است را انتخاب کنید")
                return
            os.system(f"rm -rf voices/{getwords[2]}")
            my_cursor.execute(f"DELETE FROM `voicereplies` WHERE `text` = '{ftext}'")
            sql_connect.commit()
            await event.edit("حذف شد")

        elif text.lower() == "/voice_list":
            getwords = my_cursor.execute(f"SELECT * FROM `voicereplies`")
            if getwords.fetchone() == None:
                await event.edit("هیچ ویس ای برای این بخش ست نشده است")
            else:
                strr = ""
                getwords = my_cursor.execute(f"SELECT * FROM `voicereplies`")
                for word in getwords.fetchall():
                    strr = f"{strr}متن: {word[1]} ویس: {word[2]} کپشن: {word[3]}\n"
                await event.edit(f"لیست کلمات این بخش\n\n{strr}")

        elif preg.search(r"^\/[Dd][Ee][Ll][Aa][Ll][Ll]\s\{(.+)\}$", text):
            ftext = preg.search(r"^\/[Dd][Ee][Ll][Aa][Ll][Ll]\s\{(.+)\}$", text)
            getchats = client.iter_messages(entity=0, search=ftext[1], filter=None)
            ids = []
            async for chat in getchats:
                if isinstance(chat.peer_id, (PeerUser)):
                    ids.append(chat.id)
            getlen = len(ids)
            
            await client(
                DeleteMessagesRequest(id = ids, revoke = True)
            )
            await event.reply(f"تعداد {getlen} پیام با موفقیت از پیوی ها حذف شد")

        elif preg.search(r"^\/[Ss][Ee][Tt]_[Pp][Ii][Cc][Tt][Ee][Xx][Tt]\s\{(.+)\}\s\{(\d{1,2})\}$", text) and replyid != None:
            ftext = preg.search(r"^\/[Ss][Ee][Tt]_[Pp][Ii][Cc][Tt][Ee][Xx][Tt]\s\{(.+)\}\s\{(\d{1,2})\}$", text)
            getmenow = await client(
                GetMessagesRequest([replyid, ])
            )
            if getmenow.messages[0].media == None:
                await event.edit("فقط روی رسانه ریپلی کنید نه محتوای متنی")
                return
            if not isinstance(getmenow.messages[0].media, (MessageMediaPhoto, MessageMediaDocument)):
                await event.edit("فقط روی رسانه ویدیو یا عکسی ریپلی کنید نه محتوای متنی")
                return
            if isinstance(getmenow.messages[0].media, (MessageMediaDocument, )):
                if 'video/' not in getmenow.messages[0].media.document.mime_type:
                    await event.edit("فقط روی رسانه ویدیو یا عکسی ریپلی کنید نه محتوای متنی")
                    return
            if int(ftext[2]) < 1 or int(ftext[2]) > 60:
                await event.reply("تایمر نباید از 60 ثانیه بیشتر و از 1 ثانیه کمتر باشد")
                return
            await addToSendMedia(ftext[1], fromwho, replyid, ftext[2])
            await event.edit(f"کلمه {ftext[1]} با موفقیت به لیست کلمات اضافه شد")

        elif preg.search(r"^\/[Dd][Ee][Ll]_[Pp][Ii][Cc][Tt][Ee][Xx][Tt]\s\{(.+)\}$", text):
            ftext = preg.search(r"^\/[Dd][Ee][Ll]_[Pp][Ii][Cc][Tt][Ee][Xx][Tt]\s\{(.+)\}$", text)
            addtorows = await RemoveToSendsMedia(ftext[1], replyid)
            if addtorows == False:
                await event.edit(f"این کلمه درحال حاضر در لیست کلمات موجود نیست")
            else:
                await event.edit(f"کلمه {ftext[1]} با موفقیت از لیست کلمات حذف شد")

        elif text.lower() == "/sendor_list":
            getwords = my_cursor.execute(f"SELECT * FROM `msgreplies` WHERE `type` = 'send'")
            if getwords.fetchone() == None:
                await event.edit("هیچ کلمه ای برای این بخش ست نشده است")
            else:
                strr = ""
                getwords = my_cursor.execute(f"SELECT * FROM `msgreplies` WHERE `type` = 'send'")
                for word in getwords.fetchall():
                    strr = f"{strr}متن: {word[1]} پاسخ: {word[2]}\n"
                await event.edit(f"لیست کلمات این بخش\n\n{strr}")

        elif text.lower() == "/editor_list":
            getwords = my_cursor.execute(f"SELECT * FROM `msgreplies` WHERE `type` = 'edit'")
            if getwords.fetchone() == None:
                await event.edit("هیچ کلمه ای برای این بخش ست نشده است")
            else:
                strr = ""
                getwords = my_cursor.execute(f"SELECT * FROM `msgreplies` WHERE `type` = 'edit'")
                for word in getwords.fetchall():
                    strr += f"متن: {word[1]} ادیت به: {word[2]}\n"
                await event.edit(f"لیست کلمات این بخش\n\n{strr}")

        elif preg.search(r"^\/[Ss][Ee][Tt]_[Ww][Ee][Ll][Cc][Oo][Mm][Ee]\s(.+)", text, preg.DOTALL):
            ftext = preg.search(r"^\/[Ss][Ee][Tt]_[Ww][Ee][Ll][Cc][Oo][Mm][Ee]\s(.+)", text, preg.DOTALL)[1]
            ffile = open('wlc.txt', 'w')
            ffile.write(ftext)
            ffile.close()
            await event.edit("با موفقیت ثبت شد")

        elif preg.search(r"^\/[Ss][Ee][Tt]_[Ss][Ee][Nn][Dd][Oo][Rr]\s\{(.+)\}$", text, preg.DOTALL) and replyid != None:
            getmenow = await client(
                GetMessagesRequest([replyid, ])
            )
            msgg = getmenow.messages[0].message
            entities = getmenow.messages[0].entities
            ftext = preg.search(r"^\/[Ss][Ee][Tt]_[Ss][Ee][Nn][Dd][Oo][Rr]\s\{(.+)\}$", text, preg.DOTALL)
            addtorows = await addToSends(ftext[1], msgg, entities)
            if addtorows == False:
                await event.edit(f"این کلمه درحال حاضر در لیست کلمات موجود است")
            else:
                await event.edit(f"کلمه {ftext[1]} با موفقیت به لیست کلمات اضافه شد")

        elif preg.search(r"^\/[Dd][Ee][Ll]_[Ss][Ee][Nn][Dd][Oo][Rr]\s\{(.+)\}$", text, preg.DOTALL):
            ftext = preg.search(r"^\/[Dd][Ee][Ll]_[Ss][Ee][Nn][Dd][Oo][Rr]\s\{(.+)\}$", text, preg.DOTALL)
            addtorows = await RemoveToSends(ftext[1])
            if addtorows == False:
                await event.edit(f"این کلمه درحال حاضر در لیست کلمات موجود نیست")
            else:
                await event.edit(f"کلمه {ftext[1]} با موفقیت از لیست کلمات حذف شد")

        elif preg.search(r"^\/[Ss][Ee][Tt]_[Ee][Dd][Ii][Tt][Oo][Rr]\s\{(.+)\}$", text, preg.DOTALL) and replyid != None:
            getmenow = await client(
                GetMessagesRequest([replyid, ])
            )
            msgg = getmenow.messages[0].message
            entities = getmenow.messages[0].entities
            ftext = preg.search(r"^\/[Ss][Ee][Tt]_[Ee][Dd][Ii][Tt][Oo][Rr]\s\{(.+)\}$", text, preg.DOTALL)
            addtorows = await addToEdits(ftext[1], msgg, entities)
            if addtorows == False:
                await event.edit(f"این کلمه درحال حاضر در لیست کلمات موجود است")
            else:
                await event.edit(f"کلمه {ftext[1]} با موفقیت به لیست کلمات اضافه شد")

        elif preg.search(r"^\/[Dd][Ee][Ll]_[Ee][Dd][Ii][Tt][Oo][Rr]\s\{(.+)\}$", text, preg.DOTALL):
            ftext = preg.search(r"^\/[Dd][Ee][Ll]_[Ee][Dd][Ii][Tt][Oo][Rr]\s\{(.+)\}$", text, preg.DOTALL)
            addtorows = await RemoveToEdits(ftext[1])
            if addtorows == False:
                await event.edit(f"این کلمه درحال حاضر در لیست کلمات موجود نیست")
            else:
                await event.edit(f"کلمه {ftext[1]} با موفقیت از لیست کلمات حذف شد")

        elif text.lower() == "/lock":
            if user_id == myid:
                return
            await addToUsers(user_id)
            addtorows = await lockUser(user_id)
            if addtorows == False:
                await event.edit("پیوی این یوزر درحال حاضر قفل است")
            else:
                await event.edit("پیوی این یوزر با موفقیت قفل شد")

        elif text.lower() == "/unlock":
            if user_id == myid:
                return
            await addToUsers(user_id)
            addtorows = await unlockUser(user_id)
            if addtorows == False:
                await event.edit("پیوی این یوزر درحال حاضر قفل نیست")
            else:
                await event.edit("پیوی این یوزر با موفقیت آزاد شد")

print("starting telethon client....")
client.start()
botclient.start(bot_token='7261059247:AAEIg_RgAeOcHMPoBO9MMynTYlS3V4mNJUM')
print("client is connect now !")
asyncio.get_event_loop().run_forever()