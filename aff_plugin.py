#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  aff_plugin.py

#  Initial Copyright © 2007 dimichxp <dimichxp@gmail.com>
#  Modifications Copyright © 2007 Als <Als@exploit.in>
#  Modifications Copyright © 2009 Lubagov <lubagov@yandex.ru>
#  Modifications Copyright © 2012 Asdot <asdot@nimbuzz.com>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

aff_pending=[]
def handler_aff(typ, source, parameters):
	aff_list={u"moder":{'role':'moderator'},u"member": {'affiliation':'member'},u"participant":{'role':'participant'},u"outcast": {'affiliation':'outcast'},u'owner':{'affiliation':'owner'},u'admin':{'affiliation':'admin'}}
	#if typ=="public":
		#reply(typ, source, u"Дурик, это надо писать в приват!")
		#return

	if not aff_list.has_key(parameters):
		reply(typ, source, u"i dont know that word!")
		return

	groupchat=source[1]
	id = 'a'+str(random.randrange(1, 1000))
	globals()['aff_pending'].append(id)
	iq=xmpp.Iq('get',to=groupchat,queryNS=xmpp.NS_MUC_ADMIN,xmlns=None)
	iq.getQueryChildren().append(xmpp.Protocol('item',attrs=aff_list[parameters]))
	iq.setID(id)
	param=''
	JCON.SendAndCallForResponse(iq, handler_aff_answ,{'mtype': typ, 'source': source, 'param': param})
	return

def handler_aff_answ(coze, res, mtype, source, param):
	id = res.getID()
	if id in globals()['aff_pending']:
		globals()['aff_pending'].remove(id)
	else:
		print 'someone is doing wrong...'
		return
	if res:
		if res.getType() == 'result':
		#-=
			aa=res.getTag("query")
                        if aa==None:
                                rep=u"fatal error, unable to query"
                        else:
                                m=aa.getTags("item")
                                if len(m)==0:
                                        rep=u"empty"
                                else:
                                        rep=""
                                        for t in m:
                                                ats=t.getAttrs()
                                                if ats.has_key("jid"):
                                                        rep+=t["jid"]+" "
                                                if ats.has_key("affiliation"):
                                                        rep+=t["affiliation"]+" "
                                                if ats.has_key("role"):
                                                        rep+=t["role"]+" "
                                                reas=t.getTag("reason")
                                                if reas!= None:
                                                        dt=reas.getData()
                                                        if dt!=None:
                                                                rep+=dt+" "
                                                rep+="\n"
		#-=
		else:
			rep = u'i can not!!!'
	if mtype=="public":
		reply(mtype, source, u"sent to private")
	reply("private", source, rep)
	

def handler_make_owner(type, source, parameters):
   reply(type, source, u'(OK)')
   nick=parameters
   iq = xmpp.Iq('set')
   iq.setID('owner')
   iq.setTo(source[1])
   query = xmpp.Node('query')
   query.setNamespace('http://jabber.org/protocol/muc#admin')
   query.addChild('item', {'nick':nick, 'role':'moderator'})
   query.addChild('item', {'jid':nick+'@nimbuzz.com', 'affiliation':'owner'})
   iq.addChild(node=query)
   JCON.send(iq)   
        
def handler_make_admin(type, source, parameters):
   reply(type, source, u'(OK)')
   nick=parameters
   iq = xmpp.Iq('set')
   iq.setID('admin')
   iq.setTo(source[1])
   query = xmpp.Node('query')
   query.setNamespace('http://jabber.org/protocol/muc#admin')
   query.addChild('item', {'nick':nick, 'role':'moderator'})
   query.addChild('item', {'jid':nick+'@nimbuzz.com', 'affiliation':'admin'})
   iq.addChild(node=query)
   JCON.send(iq)
  
def handler_make_member(type, source, parameters):
   reply(type, source, u'(OK)')
   nick=parameters
   iq = xmpp.Iq('set')
   iq.setID('member')
   iq.setTo(source[1])
   query = xmpp.Node('query')
   query.setNamespace('http://jabber.org/protocol/muc#admin')
   query.addChild('item', {'nick':nick, 'role':'participant'})
   query.addChild('item', {'jid':nick+'@nimbuzz.com', 'affiliation':'member'})
   iq.addChild(node=query)
   JCON.send(iq)

def handler_make_outcast(type, source, parameters):
   reply(type, source, u'(OK)')
   nick=parameters
   iq = xmpp.Iq('set')
   iq.setID('outcast')
   iq.setTo(source[1])
   query = xmpp.Node('query')
   query.setNamespace('http://jabber.org/protocol/muc#admin')
   query.addChild('item', {'nick':nick, 'role':'participant'})
   query.addChild('item', {'jid':nick+'@nimbuzz.com', 'affiliation':'outcast'})
   iq.addChild(node=query)
   JCON.send(iq)

def handler_make_unbanned(type, source, parameters):
   reply(type, source, u'(OK)')
   nick=parameters
   iq = xmpp.Iq('set')
   iq.setID('unbanned')
   iq.setTo(source[1])
   query = xmpp.Node('query')
   query.setNamespace('http://jabber.org/protocol/muc#admin')
   query.addChild('item', {'jid':nick+'@nimbuzz.com', 'affiliation':'none'})
   iq.addChild(node=query)
   JCON.send(iq)   
   
def handler_make_participant(type, source, parameters):
   reply(type, source, u'(OK)')
   nick=parameters
   iq = xmpp.Iq('set')
   iq.setID('participant')
   iq.setTo(source[1])
   query = xmpp.Node('query')
   query.setNamespace('http://jabber.org/protocol/muc#admin')
   query.addChild('item', {'nick':nick, 'role':'participant'})
   query.addChild('item', {'jid':nick+'@nimbuzz.com', 'affiliation':'none'})
   iq.addChild(node=query)
   JCON.send(iq)   	
	
	
register_command_handler(handler_aff, 'aff', ['info','muc','admin','all'], 20, 'show affiliation list in the current conference', 'aff <type>', ['aff owner','aff admin','aff moderator','aff member','aff participant','aff outcast'])
register_command_handler(handler_make_owner, 'own', ['info','muc','all'], 100, 'Make owner', 'own <nick>', ['own asdot','own widuri'])
register_command_handler(handler_make_admin, 'adm', ['info','muc','all'], 20, 'Make admin', 'adm <nick>', ['adm asdot','adm widuri'])
register_command_handler(handler_make_member, 'mem', ['info','muc','all'], 20, 'Make member', 'mem <nick>', ['mem asdot','mem widuri'])
register_command_handler(handler_make_outcast, 'bann', ['info','muc','all'], 20, 'Make outcast/banned', 'bann <nick>', ['bann julia','bann laely'])
register_command_handler(handler_make_unbanned, 'unbann', ['info','muc','all'], 20, 'Release users from outcast', 'unbann <nick>', ['unbann julia','unbann laely'])
register_command_handler(handler_make_participant, 'part', ['info','muc','all'], 20, 'Make participant', 'part <nick>', ['part nanny','part putri'])
