import time
import os
import asyncio
import math
from urllib.parse import quote
#
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from pyrogram import filters

#
from zip import split,compresion,getBytes
from progreso import progressub
from downloader.youtubedl import info,download
from cfg import *

"""============Botones de Compresion==============="""
MESSAGE_COMPRIMIDO = '**Seleccione el Tamaño Deseado**:👇'
MESSAGE_COMPRIMIDO_BOTTON = [
    [InlineKeyboardButton('Tamaño: 20mb',callback_data='z20'),
     InlineKeyboardButton('Tamaño: 50mb',callback_data='z50')
    ],
    [InlineKeyboardButton('Tamaño: 100mb',callback_data='z100'),
     InlineKeyboardButton('Tamaño: 200mb',callback_data='z200')
    ],
    [InlineKeyboardButton('Tamaño: 500mb',callback_data='z500'),
     InlineKeyboardButton('Tamaño: 1gb',callback_data='z1000')
    ],
    [InlineKeyboardButton('Tamaño: 1.5gb',callback_data='z1500'),
     InlineKeyboardButton('Tamaño: 2gb',callback_data='z2000')
    ],
    [InlineKeyboardButton('CANCEL',callback_data='stop')        
    ]
]


"""==========Nombre de Archivo de Telegram==========="""
def get_filename_media(message):
    if message.video:
        try:
            filename = message.video.file_name
        except:
            filename = message.video.file_id
    elif message.sticker:
        try:
            filename = message.sticker.file_name
        except:
            filename = message.sticker.file_id
    elif message.photo:
        try:
            filename = message.photo.file_name
        except:
            filename = message.photo.file_id
    elif message.audio:
        try:
            filename = message.audio.file_name
        except:
            filename = message.audio.file_id
    elif message.document:
        try:
            filename = message.document.file_name
        except:
            filename = message.document.file_id
    elif message.voice:
        try:
            filename = message.voice.file_name
        except:
            filename = message.voice.file_id
    return filename


"""==================Calcular Tamano de los Zip================"""
def calculador_tamaño(fichero):
    tamaño_total = 0
    for rutas, directorios, archivos in os.walk(fichero):
        for archivo in archivos:
            subarchivo = os.path.join(fichero, archivo)
            if not os.path.islink(subarchivo):
                tamaño_total += os.path.getsize(subarchivo)

    return tamaño_total    

"""==========Metodo de Compresion=========="""
def compresionbot(bot,msg,client,save,zips):
    try:
        msg = bot.send_message(msg.chat.id,'🖌**Escriba ahora el Nombre del Archivo**:👇 __Tiene 8 seg...__')
        try:
            name = asyncio.run(client.listen.Message(filters.chat(msg.chat.id), timeout = 8))
        except asyncio.TimeoutError:
            msg.edit_text('🚫**Tiempo de Espera Exedido**🚫')
            return
        print(f'./{name.chat.username}/')
        if os.path.exists(f'./{name.chat.username}/'):
            file = name.text + '.zip'
            tama = int(calculador_tamaño(save)/1048576)
            tpart = int(zips.split('M')[0])
            part = math.ceil(tama/tpart)  
            text = f'📚**Comprimiendo Archivos**\n📝**Nombre**: {file}\n'
            text += f'🗂**Tamaño Total**: {tama} MiB\n📂**Tamaño de Partes**: {tpart}MiB\n'
            text += f'💾**Cantidad de Partes**: {part}'
            msg = bot.send_message(
                msg.chat.id,
                text
            )
            comprimio,partes = split(compresion(file,save),f'./{name.chat.username}/',getBytes(zips))
            subidas = str(partes -1)
            msg.delete()
            if comprimio:
                cont = 1
                msg = bot.send_message(msg.chat.id,'⏫**Subiendo '+subidas+' Partes**')
                while cont < partes:
                    filename = file+'.'+str('%03d' % (cont))
                    url_direct = f'{BOT_URL}/file/{name.chat.username}/{quote(filename)}'
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
                        msg.chat.id,
                        f'./{name.chat.username}/'+file+'.'+str('%03d' % (cont)),
                        progress=progressub,
                        progress_args=(msg,bot,filename,start),
                        thumb='./Imagen.png',
                        reply_markup=reply_botton,
                        caption=f'**Enlace Directo👇🏻:**\n\n`{url_direct}`'
                    )  
                    cont += 1 
            msg.delete()
            bot.send_message(msg.chat.id,'✅**Subido Correctamente**')
        else:
            bot.send_message(msg.chat.id,'❌**La Carpeta del Usuario no Existe**❌')
    except Exception as e:
        msg.delete()
        bot.send_message(msg.chat.id,f'❌**Error al Subir Comprimidos **❌ {e}')


"""==============CallQuery de Compresion================="""
def query_data_compress(query,bot,client):
    if 'z' in query.data:
        zips = query.data.split('z')[-1] + 'MiB'
        msg = query.message
        save = './'+msg.chat.username+'/'
        msg.delete()
        compresionbot(bot,msg,client,save,zips)


"""================Constructor de Menu para los Videos de Youtube================"""
def build_menu(buttons,n_cols,header_buttons=None,footer_buttons=None):
    menu = []
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


"""================Descarga de Videos de Youtube================"""
def download_of_youtube(CallbackQuery,each,bot):
    msg = CallbackQuery.message
    format = each[0]
    ext = each[-1]
    username = msg.chat.username
    url = CallbackQuery.message.reply_to_message.text.split(sep=' ')[-1]
    msg.delete()
    msg = bot.send_message(msg.chat.id,'⏬**Descargando... Por favor Espere...**')
    try:
        print(format)
        file,duration = download(url,username,format)
        msg.delete()
        msg = bot.send_message(msg.chat.id,'✅**Descargado Correctamente..**')
        msg.delete()
        print(file)
    except Exception as e:
        msg.delete()
        bot.send_message(msg.chat.id,f'❌**Error al Descargar de Youtube**❌ {e}')
        return False
    if os.path.exists(file):
        if os.path.getsize(file) < 1572864000:
            try:
                msg = bot.send_message(msg.chat.id,'⏫**Subiendo a Telegram... Por Favor Espere**')
                filename = file.split('/')[-1]
                start = time.time()
                dir_user = file.split('/')[-2]
                dir_name = file.split('/')[-1]
                url_direct = f'{BOT_URL}/file/{username}/{quote(dir_name)}'
                enlace_directo = [
                    [InlineKeyboardButton(
                        'Enlace Directo',
                        url=url_direct
                        ),
                    ]      
                ]
                reply_botton = InlineKeyboardMarkup(enlace_directo)
                bot.send_video(
                    msg.chat.id,
                    file,
                    reply_markup=reply_botton,
                    progress=progressub,
                    progress_args=(msg,bot,filename,start),
                    thumb='./Imagen.png',
                    duration=duration,
                    caption=f'**Enlace Directo👇🏻:**\n\n`{url_direct}`'
                )
                msg.delete()
                return True
            except Exception as e:
                msg.delete()
                bot.send_message(msg.chat.id,f'❌**Error al Subir a Telegram**❌ {e}')
                return False
        elif os.path.getsize(file) > 1572864000:
            try:
                string = file.split(sep='/')[:-1]
                sub = str(file.split(sep='/')[-1].split(sep='.')[0])+'.zip'
                dir = ''
                for f in string:
                    dir += f+'/'
                namef = str(file.split(sep='/')[-1])
                tama = int(os.path.getsize(file)/1048576)
                tpart = 1500
                part = math.ceil(tama/tpart) 
                text = f'📚**Comprimiendo Archivos**\n📝**Nombre:** {file}\n'
                text += f'🗂**Tamaño Total**: {tama} MiB\n📂**Tamaño de Partes**: {tpart}MiB\n'
                text += f'💾**Cantidad de Partes**: {part}' 
                msg = bot.send_message(
                    msg.chat.id,
                    text
                )
                comprimio,partes = split(file,f'./{msg.chat.username}/',getBytes('1500MiB'))
                msg.delete()
                subidas = str(partes -1)
                if comprimio:
                    cont = 1
                    msg = bot.send_message(msg.chat.id,'⏫**Subiendo '+subidas+' Partes**')
                    while cont < partes:
                        filename = sub.split(sep='.')[0]+'.zip.'+str('%03d' % (cont))
                        start = time.time()
                        url_direct = f'{BOT_URL}/file/{msg.chat.username}/{quote(filename)}'
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
                            f'./{msg.chat.username}/'+sub.split(sep='.')[0]+'.zip.'+str('%03d' % (cont)),
                            reply_markup=reply_botton,
                            progress=progressub,
                            progress_args=(msg,bot,filename,start),
                            thumb='./Imagen.png',
                            caption=f'**Enlace Directo👇🏻:**\n\n`{url_direct}`'
                        )  
                        os.remove(f'./{msg.chat.username}/'+sub.split(sep='.')[0]+'.zip.'+str('%03d' % (cont)))
                        cont += 1 
                    msg.delete()
                bot.send_message(msg.chat.id,'✅**Subido Correctamente**')
                return True
            except Exception as e:
                msg.delete()
                bot.send_message(msg.chat.id,f'❌**Error al Subir a Telegram**❌ {e}')
                return False
        else:
            bot.send_message(msg.chat.id,'❌**El Archivo no se Descargó Correctamente**❌')