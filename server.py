import asyncio
import os
#Apps de Terceros
from aiohttp import web
from aiohttp import streamer

"""==============Envio de el Archivo por HTTP================="""
@streamer
async def file_sender(writer, file_path=None):

    with open(file_path, 'rb') as f:
        chunk = f.read(2 ** 16)
        while chunk:
            await writer.write(chunk)
            chunk = f.read(2 ** 16)

"""===============Servicio de Recepcion de la Peticion GET==================="""
async def download_file(request):
    file_name = request.match_info['file_name']  
    route =  request.match_info['route']

    file_path = os.path.join(route, file_name)
    headers = {
        "Content-disposition": "attachment; filename={file_name}".format(file_name=file_name),
        "Accept-Ranges": "bytes",
        "Content-Type": f'{file_path.split("/")[-1].split(".")[-1]}',
        "Content-Length": str(os.path.getsize(file_path))
        }  

    if not os.path.exists(file_path):
        return web.Response(
            body='El Archivo  <{file_name}> No Existe'.format(file_name=file_name),
            status=404
        )

    return web.Response(
        body=file_sender(file_path=file_path),
        headers=headers
    )


