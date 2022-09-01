import time

"""==========Barra de Progreso============"""
def text_progres(index,max):
	try:
		if max<1:
			max += 1
		porcent = index / max
		porcent *= 100
		porcent = round(porcent)
		make_text = ''
		index_make = 1
		make_text += '\n['
		while(index_make<21):
			if porcent >= index_make * 5: make_text+='●'
			else: make_text+='○'
			index_make+=1
		make_text += ']'
		return make_text
	except Exception as ex:
			return ''


"""============Progreso de Descarga==========="""
def progressddl(current, total,message,bots,filename,start,):
    porcent = int(current * 100 / total)
    act = time.time() - start
    velo = round((round(current/1000000,2)/act),2)
    if porcent % 8 == 0:
        try:
            text = f"⏬**Descargando**\n\n💾**Nombre**: {filename} \n"
            text += f'{text_progres(current,total)} {current * 100 / total:.1f}%\n\n'
            text += f'🗓**Total**:{round(total/1000000,2)} MiB \n'
            text += f'📥**Descargado**: {round(current/1000000,2)}MiB\n'
            text += f'📥**Velocidad**: {velo} MiB/S\n'
            bots.edit_message_text(message.chat.id,message.id,text)
        except:pass 


"""============Progreso de Subida==============="""
def progressub(current, total,message,bots,filename,start):
    porcent = int(current * 100 / total)
    act = time.time() - start
    velo = round((round(current/1000000,2)/act),2)
    if porcent % 20 == 0:
        try:
            text = f"⏫**Subiendo**\n\n💾**Nombre**: {filename} \n"
            text += f'{text_progres(current,total)} {current * 100 / total:.1f}%\n\n'
            text += f'🗓**Total **:{round(total/1000000,2)} MiB \n'
            text += f'📤**Subido**: {round(current/1000000,2)}MiB\n'
            text += f'📥**Velocidad**: {velo} MiB/S\n'
            bots.edit_message_text(message.chat.id,message.id,text)
        except:pass

"""============Progreso de Descarga de Youtube==============="""
def progressytdl(current, total,filename,message,bots):
    porcent = int(current * 100 / total)
    filename =filename.split('/')[-1]
    try:
        text = f"⏬**Descargando de Youtube**\n\n💾**Nombre**: {filename} \n"
        text += f'{text_progres(current,total)} {current * 100 / total:.1f}%\n\n'
        text += f'🗓**Total**:{round(total/1000000,2)} MiB \n'
        text += f'📥**Descargado**: {round(current/1000000,2)}MiB\n'
        bots.edit_message_text(message.chat.id,message.id,text)
    except:pass 