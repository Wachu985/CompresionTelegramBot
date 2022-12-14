import time
import os
from urllib.parse import quote
from asyncio import sleep
from shutil import rmtree

#Apps de Terceros
from pyrogram import Client,filters
import tgcrypto
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup,CallbackQuery
from convopyro import Conversation
import nest_asyncio
from pyrogram.methods.utilities.idle import idle
from aiohttp import web,ClientSession
import gdown

#
from cfg import *
from utils import *
from progreso import progressub,progressddl,progressytdl,progresswget
from downloader.youtubedl import YoutubeDL
from downloader.wget import download as downloadwget
from server import download_file
from downloader.mediafire import get




print('Iniciando BOT')

"""===========Variables Globales============"""
nest_asyncio.apply()
yturls = []




"""=========Cliente del Bot========="""
bot = Client('CompresionWachu',api_id=API_ID,api_hash=API_HASH,bot_token=BOT_TOKEN)
Conversation(bot)


"""============Metodo Start============="""
@bot.on_message(filters.command('start') & filters.private)
def Bienvenido(client,message):
    enlace_directo = [
            [InlineKeyboardButton(
                '⚙️Soporte',
                url=f'https://t.me/Wachu985'
            ),
            InlineKeyboardButton(
                '💻GITHUB',
                url=f'https://github.com/Wachu985/CompresionTelegramBot'
            ),
            ]      
        ]
    reply_botton = InlineKeyboardMarkup(enlace_directo)
    bot.send_message(message.chat.id,'✉️**Bienvenido al Bot '+message.chat.first_name+'**'+'\n\n__📱Soy un Simple Bot de Compresion de Archivos de Telegram y Descargas de Enlaces Directos de Internet con Servicio File to Link📱__',reply_markup=reply_botton)


"""============Descarga de Archivos de Telegram==========="""
@bot.on_message(filters.media & filters.private)
def media_telegram(client,message):
    try:
        save = './'+message.chat.username+'/'
        filename = get_filename_media(message)
        msg = bot.send_message(
            message.chat.id,
            "📡**Descargando Archivos... Por Favor Espere**",
            reply_to_message_id=message.id
        )
        start = time.time() 
        #Descarga de Media
        bot.download_media(
            message,
            save,
            progress=progressddl,
            progress_args=(msg,bot,filename,start)
        )
        msg.delete()
        msg = bot.send_message(msg.chat.id,'✅Descargado Correctamente',reply_to_message_id=message.id)
    except Exception as e:
        msg.delete()
        bot.send_message(msg.chat.id,f'❌Error de Descarga❌ {e}')


"""============Mostrar Directorio============"""
@bot.on_message(filters.command('ls') & filters.private)
def list(client,message):
    save = './'+message.chat.username+'/'
    if os.path.exists(save):
        oslist = os.listdir(save)
        cont = 1
        msg ='🔡**DIRECTORIO**: \n\n'
        for f in oslist:
            msg += '**'+str(cont)+'**'+'-'+f'`{str(f)}`'+'\n\n'
            cont +=1
        bot.send_message(message.chat.id,msg)
    else:
        bot.send_message(message.chat.id,'🚫**No tienes ningun Elemento**🚫')


"""============Obtener Link de Internet============"""
@bot.on_message(filters.command('link') & filters.private)
def get_link(client,message):
    save = './'+message.chat.username+'/'
    val = message.command[-1]
    if os.path.exists(save):
        oslist = os.listdir(save)
        file = oslist[int(val)-1]
        url_direct = f'{BOT_URL}/file/{message.chat.username}/{quote(file)}'
        print(url_direct)
        enlace_directo = [
            [InlineKeyboardButton(
                'Enlace Directo',
                url=url_direct
            ),
            ]      
        ]
        reply_botton = InlineKeyboardMarkup(enlace_directo)

        message.reply(f'**Enlace Directo a Internet 👇🏻:**\n\n`{url_direct}`',reply_markup=reply_botton)
        
    else:
        bot.send_message(message.chat.id,'🚫**No tienes ningun Elemento**🚫')

    
"""=============Eliminar Elementos============="""
@bot.on_message(filters.command('rm') & filters.private)
def delete(client,message):
    save = './'+message.chat.username+'/'
    if os.path.exists(save):
        val = message.command[-1]
        varios = val.split('-')
        if len(varios)>1:
            if os.path.exists(save):
                oslist = os.listdir(save)
                for v in varios:
                    file = oslist[int(v)-1]
                    os.remove(f'./{message.chat.username}/{file}')
                message.reply('💢**Archivos Eliminados Correctamente**💢')
        else:
            if os.path.exists(save):
                oslist = os.listdir(save)
                file = oslist[int(val)-1]
                os.remove(f'./{message.chat.username}/{file}')
                message.reply('💢**Archivo Eliminado Correctamente**💢')
    else:
        bot.send_message(
            message.chat.id,
            '🚫**No se Pudo Eliminar el Elemento Correctamente Por que no Existe**🚫'
        )


"""=============Eliminar Directorio============="""
@bot.on_message(filters.command('rmall') & filters.private)
def delete(client,message):
    save = './'+message.chat.username+'/'
    if os.path.exists(save):
        rmtree(save)
        bot.send_message(
            message.chat.id,
            '💢**Eliminado el Directorio Correctamente**💢'
        )
    else:
        bot.send_message(
            message.chat.id,
            '🚫**No se Pudo Eliminar el Directorio Correctamente Por que no Existe**🚫'
        )


"""===============Comando de Compresion==============="""
@bot.on_message(filters.command('zips') & filters.private)
def zip(client,message):
    text = MESSAGE_COMPRIMIDO
    reply_botton = InlineKeyboardMarkup(MESSAGE_COMPRIMIDO_BOTTON)
    msg=bot.send_message(
        chat_id=message.chat.id,
        text=text,
        reply_markup=reply_botton,
        reply_to_message_id=message.id
    )

"""==============Descarga de Archivos de Internet================"""
@bot.on_message(filters.regex('http') & filters.private | filters.regex('youtu') & filters.private | filters.regex('youtube') & filters.private)
def download(client,message):

    #==================Descagando Lista de Reproduccion======================
    if "playlist" in message.text:
        playlist = message.text
        msg = bot.send_message(message.chat.id,'🖌**Escriba la Resolucion de los Videos**:👇 __Tiene 8 seg...__')
        try:
            res = asyncio.run(client.listen.Message(filters.chat(msg.chat.id), timeout = 8))
        except asyncio.TimeoutError:
            msg.edit_text('🚫**Tiempo de Espera Exedido**🚫')
            return
        zips = '2000MiB'
        username = message.chat.username
        try:
            msg = bot.send_message(message.chat.id,'⏫**Recopilando Información... Por Favor Espere**')
            ytdl = YoutubeDL(progressytdl,msg,bot)
            save,title = ytdl.downloadlist(playlist,res.text,username)
            file = title+'.zip'
            msg.delete()
            msg = bot.send_message(message.chat.id,'📚**Comprimiendo Archivos**')
            comprimio,partes = split(compresion(file,save),f'./{message.chat.username}/',getBytes(zips))
            subidas = str(partes -1)
            msg.delete()
            if comprimio:
                cont = 1
                up = bot.send_message(message.chat.id,'⏫**Subiendo '+subidas+' Partes...**')
                while cont < partes:
                    filename = file+'.'+str('%03d' % (cont))
                    start = time.time()
                    enlace_directo = [
                        [InlineKeyboardButton(
                            'Enlace Directo',
                            url=f"{BOT_URL}/file/{message.chat.username}/"+file+'.'+str('%03d' % (cont))
                        ),
                        ]      
                    ]
                    reply_botton = InlineKeyboardMarkup(enlace_directo)
                    bot.send_document(
                        message.chat.id,
                        f'./{message.chat.username}/'+file+'.'+str('%03d' % (cont)),
                        progress=progressub,
                        reply_markup=reply_botton,
                        progress_args=(up,bot,filename,start),
                        thumb='./Imagen.png',
                        caption=f"`{BOT_URL}/file/{message.chat.username}/"+file+'.'+str('%03d' % (cont))+'`'
                    )
                    cont += 1 
                up.delete()
                bot.send_message(message.chat.id,'✅**Subido Correctamente**')
        except Exception as e:
            msg.delete()
            bot.send_message(message.chat.id,f'❌**Error al Descargar la Lista❌ {e}**')

    #=====================Comando de Videos de Youtube y De Twitch=====================#
    elif "youtu" in message.text or 'twitch' in message.text:
        global yturls
        yturls = []
        ytdl = YoutubeDL()
        try:
            yt = ytdl.info(message.text)
            for f in yt:
                yturls.append(f.split(sep=':'))
            button_list = []
            for each in yturls:
                button_list.append(InlineKeyboardButton(each[1], callback_data = each[0]))
            keyboard_group=InlineKeyboardMarkup(build_menu(button_list, n_cols=3))
            text = '**Seleccione la Resolucion:👇**'
            msg= bot.send_message(chat_id=message.chat.id,text=text,reply_markup=keyboard_group,reply_to_message_id=message.id) 
        except Exception as e:
            bot.send_message(message.chat.id,f'❌**Error al Analizar el Video❌-> {e}**')

    #================Descargas de Mediafire===================
    elif "mediafire" in message.text:
        try:
            save = './'+message.chat.username+'/'
            if not os.path.exists(save):
                os.mkdir(save)
            msg = bot.send_message(message.chat.id, '⏬**Descargando Archivo. Por Favor Espere....**')
            name = downloadwget(get(message.text),msg,bot,out=f'./{message.chat.username}/',bar=progresswget)
            filename = name.split("/")[-1]
            msg = bot.edit_message_text(message.chat.id,msg.id, '✅**Archivo Descargado Correctamente**')
            #Si el Tamaño de el Archivo es menor q 1500MiB 
            if os.path.exists(name):
                if os.path.getsize(name) < 1572864000:
                    url_direct = f'{BOT_URL}/file/{message.chat.username}/{quote(name.split("/")[-1])}'
                    enlace_directo = [
                            [InlineKeyboardButton(
                                'Enlace Directo',
                                url=url_direct
                            ),
                            ]      
                        ]
                    reply_botton = InlineKeyboardMarkup(enlace_directo)
                    start = time.time()
                    bot.send_document(
                        message.chat.id,
                        name,
                        progress=progressub,
                        reply_markup=reply_botton,
                        progress_args=(msg,bot,name,start),
                        thumb='./Imagen.png',
                        caption=f"**Enlace Directo👇🏻:**\n\n`{url_direct}`"
                    )
                    msg.delete()
                    msg = bot.send_message(message.chat.id, '✅**Subido Correctamente**')
                elif os.path.getsize(name) > 1572864000:
                    msg.delete()
                    sub = ''.join(filename.split(sep='.')[:-1])+'.zip'
                    msg = bot.send_message(
                        msg.chat.id,
                        f'📚**Comprimiendo Archivos... Por Favor Espere..**'
                    )
                    comprimio,partes = split(compressionone(sub,name),f'./{message.chat.username}/',getBytes('1500MiB'))
                    msg.delete()
                    if comprimio:
                        cont = 1
                        subidas = str(partes -1)
                        msg = bot.send_message(msg.chat.id,'⏫**Subiendo '+subidas+' Partes**')
                        while cont < partes:
                            filename = sub+'.'+str('%03d' % (cont))
                            start = time.time()
                            url_direct = f'{BOT_URL}/file/{message.chat.username}/{quote(filename)}'
                            enlace_directo = [
                                [InlineKeyboardButton(
                                    'Enlace Directo',
                                    url=url_direct
                                ),
                                ]      
                            ]
                            reply_botton = InlineKeyboardMarkup(enlace_directo)
                            bot.send_document(
                                msg.chat.id,
                                f'./{message.chat.username}/'+sub+'.'+str('%03d' % (cont)),
                                reply_markup=reply_botton,
                                progress=progressub,
                                progress_args=(msg,bot,filename,start),
                                thumb='./Imagen.png',
                                caption=f'**Enlace Directo👇🏻:**\n\n`{url_direct}`'
                            )  
                            cont += 1 
                        msg.delete()
                bot.send_message(msg.chat.id,'✅**Subido Correctamente**')
        except Exception as e: bot.edit_message_text(message.chat.id, msg.id, f"❌ **El Enlace no se pudo descargar -> {e}**❌")
        return

    #================Descargas de Google Drive===================
    elif 'drive.google.com' in message.text:
        try:
            save = './'+message.chat.username+'/'
            if not os.path.exists(save):
                os.mkdir(save)
            url = message.text
            msg = bot.send_message(message.chat.id, "⏬**Descargando Archivo. Por Favor Espere...**")
            filename = gdown.download(url=url, output=f"./{message.chat.username}/")
            file = filename.split("/")[-1]
            bot.edit_message_text(message.chat.id, msg.id, f"✅**Descargado Correctamente**")
            #Si el Tamaño de el Archivo es menor q 1500MiB 
            if os.path.exists(filename):
                if os.path.getsize(filename) < 1572864000:
                    url_direct = f'{BOT_URL}/file/{message.chat.username}/{quote(filename.split("/")[-1])}'
                    enlace_directo = [
                        [InlineKeyboardButton(
                            'Enlace Directo',
                            url=url_direct
                        ),
                        ]      
                    ]
                    reply_botton = InlineKeyboardMarkup(enlace_directo)
                    start = time.time()
                    bot.send_document(
                        message.chat.id,
                        filename,
                        progress=progressub,
                        reply_markup=reply_botton,
                        progress_args=(msg,bot,filename.split('/')[-1],start),
                        thumb='./Imagen.png',
                        caption=f"**Enlace Directo👇🏻:**\n\n`{url_direct}`"
                    )
                    msg.delete()
                elif os.path.getsize(filename) > 1572864000:
                    sub = ''.join(file.split(sep='.')[:-1])+'.zip'
                    msg.delete()
                    msg = bot.send_message(
                        msg.chat.id,
                        f'📚**Comprimiendo Archivos... Por Favor Espere..**'
                    )
                    comprimio,partes = split(compressionone(sub,filename),f'./{message.chat.username}/',getBytes('1500MiB'))
                    msg.delete()
                    if comprimio:
                        cont = 1
                        subidas = str(partes -1)
                        msg = bot.send_message(msg.chat.id,'⏫**Subiendo '+subidas+' Partes**')
                        while cont < partes:
                            filename = sub+'.'+str('%03d' % (cont))
                            start = time.time()
                            url_direct = f'{BOT_URL}/file/{message.chat.username}/{quote(filename)}'
                            enlace_directo = [
                                [InlineKeyboardButton(
                                    'Enlace Directo',
                                    url=url_direct
                                ),
                                ]      
                            ]
                            reply_botton = InlineKeyboardMarkup(enlace_directo)
                            bot.send_document(
                                msg.chat.id,
                                f'./{message.chat.username}/'+filename,
                                reply_markup=reply_botton,
                                progress=progressub,
                                progress_args=(msg,bot,filename,start),
                                thumb='./Imagen.png',
                                caption=f'**Enlace Directo👇🏻:**\n\n`{url_direct}`'
                            )
                            cont += 1 
                        msg.delete()
                bot.send_message(msg.chat.id,'✅**Subido Correctamente**')
        except Exception as e: bot.edit_message_text(message.chat.id, msg.id, f"❌ **El Enlace no se pudo descargar -> {e} **❌")
        return

    elif 'http' in message.text:
        try:
            save = './'+message.chat.username+'/'
            if not os.path.exists(save):
                os.mkdir(save)
            msg = bot.send_message(message.chat.id,'⏬**Descargando Archivo. Por Favor Espere....**')
            filename = downloadwget(message.text,msg,bot,out=f'./{message.chat.username}/',bar=progresswget)
            file = filename.split("/")[-1]
            msg = bot.edit_message_text(message.chat.id,msg.id,f'✅**Archivo Descargado Correctamente**')
            if os.path.exists(filename):
                if os.path.getsize(filename) < 1572864000:
                    url_direct = f'{BOT_URL}/file/{message.chat.username}/{quote(filename.split("/")[-1])}'
                    enlace_directo = [
                        [InlineKeyboardButton(
                            'Enlace Directo',
                            url=url_direct
                        ),
                        ]      
                    ]
                    reply_botton = InlineKeyboardMarkup(enlace_directo)
                    start = time.time()
                    bot.send_document(
                        message.chat.id,
                        filename,
                        progress=progressub,
                        reply_markup=reply_botton,
                        progress_args=(msg,bot,filename.split('/')[-1],start),
                        thumb='./Imagen.png',
                        caption=f"**Enlace Directo👇🏻**:\n`{url_direct}`"
                    )
                    msg.delete()
                elif os.path.getsize(filename) > 1572864000:
                    sub = ''.join(file.split(sep='.')[:-1])+'.zip'
                    msg = bot.send_message(
                        msg.chat.id,
                        f'📚**Comprimiendo Archivos... Por Favor Espere..**'
                    )
                    comprimio,partes = split(compressionone(sub,filename),f'./{message.chat.username}/',getBytes('1500MiB'))
                    msg.delete()
                    subidas = str(partes -1)
                    if comprimio:
                        cont = 1
                        msg = bot.send_message(msg.chat.id,'⏫**Subiendo '+subidas+' Partes**')
                        while cont < partes:
                            filename = sub+'.'+str('%03d' % (cont))
                            start = time.time()
                            url_direct = f'{BOT_URL}/file/{message.chat.username}/{quote(filename)}'
                            enlace_directo = [
                                [InlineKeyboardButton(
                                    'Enlace Directo',
                                    url=url_direct
                                ),
                                ]      
                            ]
                            reply_botton = InlineKeyboardMarkup(enlace_directo)
                            bot.send_document(
                                msg.chat.id,
                                f'./{message.chat.username}/'+filename,
                                reply_markup=reply_botton,
                                progress=progressub,
                                progress_args=(msg,bot,filename,start),
                                thumb='./Imagen.png',
                                caption=f'**Enlace Directo👇🏻:**\n\n`{url_direct}`'
                            )  
                            cont += 1 
                        msg.delete()
                bot.send_message(msg.chat.id,'✅**Subido Correctamente**')
        except Exception as e: bot.edit_message_text(message.chat.id, msg.id, f"❌ **El Enlace no se pudo descargar -> {e} **❌")
        return


        
        
"""==================Query de Compresion y Videos de Youtube=================="""
@bot.on_callback_query()
def callback_querry(client,CallbackQuery):
    if 'z' in CallbackQuery.data:
        query_data_compress(CallbackQuery,bot,client)

    elif CallbackQuery.data =='stop':
            msg = CallbackQuery.message 
            client.listen.Cancel(filters.user(msg.from_user.id))
            msg.delete()

    global yturls
    for each in yturls:
        if CallbackQuery.data == each[0]:
            upload = download_of_youtube(CallbackQuery,each,bot)
            if upload:
                yturls = []
                break



"""==============Declarando Variables del Servidor=============="""
server = web.Application()
server.router.add_get('/file/{route}/{file_name}', download_file)
runner = web.AppRunner(server)

"""===================Metodo Para Mantener Despierto el Bot========================="""
async def despertar(sleep_time=TIME_WAKE * 60):
    while True:
        await sleep(sleep_time)
        async with ClientSession() as session:
            async with session.get(f'{BOT_URL}' + "/Despiertate"):
                pass



"""================Incio del Bot=============="""
async def run_server():
    await bot.start()
    print('=========Bot Iniciado=========')
    await runner.setup()
    print('=========Iniciando Server=========')
    await web.TCPSite(runner, host='0.0.0.0', port=os.getenv('PORT')).start()
    print('=========Server Iniciado=========')

if __name__=='__main__':
    try:
        bot.loop.run_until_complete(run_server())
        bot.loop.run_until_complete(despertar())
        idle()
    except:
        bot.loop.run_until_complete(run_server())
        bot.loop.run_until_complete(despertar())
        idle()
