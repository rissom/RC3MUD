
import string
import os
from os.path import isfile, join
from os import listdir, remove
import string
import shutil
import base64
import asyncio
import tornado.web
import tornado.websocket
import json
import datetime



class Webserver(tornado.web.Application):

    
    main_loop = None
    
    def __init__(self):
        from system.websocket import Websocket
        from system.websocketrtc import WebsocketRTC
        handlers = [ (r"/upload", UploadHandler),
                     (r"/download", GetConfigHandler),
                     (r"/websocket", Websocket),
                     (r"/websocketrtc", WebsocketRTC),
                     (r'/(.*)', tornado.web.StaticFileHandler, {'path': '../webstatic', "default_filename": "index.html"}),]
        settings = {'debug': True}
        super().__init__(handlers, **settings)

    def run(self, port=80):
        self.listen(port)
        if os.path.exists("../../fullchain.pem"):
            self.listen(port+443,ssl_options={
                "certfile": "../../fullchain.pem",
                "keyfile": "../../privkey.pem",
            })
        Webserver.main_loop = tornado.ioloop.IOLoop().current()
        Webserver.main_loop.start()
        print("Webserver: TORNADO STARTED")
 
    
## handles downloads of configurations at /getconfig
class GetConfigHandler(tornado.web.RequestHandler):
    def delete_all_files_in_folder(path):
        mypath = Config.workingpath+path
        for f in listdir(mypath):
            if isfile(join(mypath, f)):
                remove(join(mypath, f))
    def get(self):
        config = Config.getSingleton()
        filename = config.get("device.name")+"."+config.get("device.mac")+"."+str(datetime.datetime.now().date())+".tgz"
        filename = filename.replace(" ","_")
        log.debug("Webserver: config filename: "+str(filename))
        
        if not os.path.exists(Config.workingpath+'/temp'):
            os.makedirs(Config.workingpath+'/temp')
        GetConfigHandler.delete_all_files_in_folder('/temp')
        mypath = Config.workingpath+"/temp"
        
        shutil.make_archive("config", "gztar", Config.workingpath , '.')
        self.add_header("Content-Disposition","attachment; filename="+filename)
        data = open("config.tar.gz", "rb").read() 
        self.write(data)

## handles uploads of updates at /upload
class UploadHandler(tornado.web.RequestHandler):
    def post(self):
        file1 = self.request.files['update'][0]
        original_fname = file1['filename']
        extension = os.path.splitext(original_fname)[1]
        fname = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(6))
        final_filename= fname+extension
        if not os.path.exists(Config.workingpath+'/update'):
            os.makedirs(Config.workingpath+'/update')
            os.makedirs(Config.workingpath+'/update/download')
        output_file = open(Config.workingpath+"/update/download/" + final_filename, 'wb')
        output_file.write(file1['body'])
        log.debug("file" + final_filename + " is uploaded")
        self.write( Updater.check_update_and_give_web_response() )

