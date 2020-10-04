from system.log import log
from game.player import Player
from system.helper import i18n

class Parser(object):
       
    def parse_user_command(wsclient, jsonmsg):
        
        lang = wsclient.player.lang
        
        if jsonmsg['cmd']=='user':
            #wsclient.player.parse_user_command(jsonmsg['data'])
            answered = False
            msg = jsonmsg['data']
            for a in Player.actions:
                if msg.startswith(i18n(lang,a['command'])):
                    parameter = msg[ len(i18n(lang,a['command']))+1:]
                    getattr(wsclient.player,a['function'])(a,msg, parameter)
                    answered = True
    
            if not answered:
                answered = wsclient.player.room.parse_user_command(wsclient.player, msg)
            if not answered:
                wsclient.player.send_text(i18n(lang,{ "en":"What you mean by '","de":"Was meinst Du mit '"})+msg+i18n(lang,{"en":"'? Try 'help' and remember: The TAB-key has always been your friend!","de":"'? Versuche 'hilfe' und erinnere Dich: Die TAB-Taste war schon immer Dein bester Freund!"}))

    