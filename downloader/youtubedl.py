import unicodedata
import random
import re
# Apps de Terceros
import yt_dlp


"""==================Modificacion de Texto======================="""
import unicodedata
import random
import re
# Apps de Terceros
import yt_dlp


class YoutubeDL():
    def __init__(self,downlad_progres=None,msg=None,bot=None):
        self.downlad_progres = downlad_progres
        self.msg = msg
        self.bot = bot

    """============Conversion de Nombres============="""
    def slugify(self,value, allow_unicode=False):
        """
        Taken from https://github.com/django/django/blob/master/django/utils/text.py
        Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
        dashes to single dashes. Remove characters that aren't alphanumerics,
        underscores, or hyphens. Convert to lowercase. Also strip leading and
        trailing whitespace, dashes, and underscores.
        """
        value = str(value)
        ext = str(value).split('.')[-1]
        value = str(value).split('.')[0]
        if allow_unicode:
            value = unicodedata.normalize('NFKC', value)
        else:
            value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
        value = re.sub(r'[^\w\s-]', '', value.lower())
        return re.sub(r'[-\s]+', '-', value).strip('-_')

    """==================Progreso de Descarga de Videos==================="""
    def my_hook(self,d):
        if d['status'] == 'downloading':
            filename = d['filename']
            current = d['downloaded_bytes']
            total = d['total_bytes']
            speed = 0
            if d['speed'] is not None:
                speed = d['speed']
            tiempo = d['_eta_str']
            self.downlad_progres(int(current), int(total),speed,filename,tiempo,self.msg,self.bot)
        if d['status'] == 'finished':
            print('Done downloading, now converting ...')

    """==================Informacion de el Video==================="""
    def info(self,url):
        ydl_opts = {
            'restrict_filenames':True,
            'windowsfilenames':False
            }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            meta = ydl.extract_info(
                url, download=False)

        formats = meta['formats']
        id = []
        ext = []
        formato = []
        for format in formats:
            if format['vcodec'] !='none' and format['acodec'] != 'none':
            # if 'DASH' in str(format['format']):
            #     continue
                # if 'mp4' == str(format['ext']):    
                id.append(format['format_id'])
                ext.append(format['ext'])
                formato.append(format['format'].split(sep='-')[-1])
        guardar = []
        for val1,val2,val3 in zip(id,ext,formato): 
            guardar.append(val1 +':'+val3 + ':'+val2)
        return guardar   


    """================Obtencion del Titulo del Video================"""
    def getTitle(self,url):
        elem = 'abcdefgh1jklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        ids = "".join(random.sample(elem,4))
        ydl_opts = {
            'restrict_filenames':True,
            'windowsfilenames':False
            }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            meta = ydl.extract_info(
                url, download=False)
            title = meta['title']+ids
            return self.slugify(title)


    """===============Obtencion de la PlayList==============="""
    def getPlaylist(self,url):
        elem = 'abcdefgh1jklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        ids = "".join(random.sample(elem,4))
        ydl_opts = {
            'restrict_filenames':True,
            'windowsfilenames':False
            }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            meta = ydl.extract_info(
                url, download=False)
            playlist = str(meta['title'])+ids
            return self.slugify(playlist)


    """===============Descarga de Video de Youtube================="""
    def download(self,url,username,format):
        title = self.getTitle(url)
        file = './'+username+'/'+title+'.%(ext)s'
        format = format.split(sep=('('))[-1].replace(')','')
        opcions = {
            'format': format,
            'outtmpl': file,
            'restrict_filenames':True,
            'windowsfilenames':False,
            'progress_hooks': [self.my_hook],
        }

        with yt_dlp.YoutubeDL(opcions) as ydl:
            ydl.download([url])
            meta = ydl.extract_info(url, download=False)
            name = './'+username+'/'+title+'.mp4'
            duration = int(meta['duration'])
        return name,duration


    """================Descarga de Lista de Youtube=================="""
    def downloadlist(self,urls,res,username):
        playlist = self.getPlaylist(urls)
        file = './'+username+'/'+playlist+'/%(title)s.%(ext)s'
        ydl_opts = {
            'format': f'b[height<={res}]',
            'outtmpl': file,
            'restrict_filenames':False,
            'windowsfilenames':False,
            'progress_hooks': [self.my_hook]
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([urls])
            dir = './'+username+'/'+playlist+'/'
            name = playlist
            return dir,name
        



    