#coding=utf8
from hiclient.client import Client
from hiclient import helper
import cPickle as pickle

import config

class Handler:
    def __init__(self, client):
        self.client = client
        for f in dir(self):
            if f.startswith('on_'):
                client.listen(f[3:], getattr(self, f))

    def on_message_received(self, data):
        message = helper.extract_text(data['Body'])
        if data['Header']['type'] == 2:
            # 群消息
            if "@op" not in message:
                return
        reply = self.process(message)
        self.client.send_text_message(data['Header']['type'], data['Header']['reply_to'], reply)

    def process(self, message):
        return message

    def on_login_success(self):
        self.client.send('query', 'get_offline_msg',
                version = '1.0',
                type = 1,
                #gid = 1396730,
                gid = 1435931,
		start_time = 0,
                start_id = 0)

        self.client.send('query', 'get_offline_msg',
                version = '1.0',
                type = 0,
                #gid = 1396730,
                start_time = 0,
                start_id = 0)

        #def sss(data = None):
        #    if data is None:
        #        start_time = 0
        #        start_id = 0
        #    else:
        #        if data['Header']['code'] == 200: return
        #        start_time = data['Header']['last_time']
        #        start_id = data['Header']['last_id']
        #    self.client.send('query', 'get_offline_msg2',
        #            version = '1.0',
        #            msg_type = 1,
        #            type = 0,
        #            count = 500,
        #            start_time = start_time,
        #            start_id = start_id,
        #            callback = sss)

        #sss()

        #self.client.delete_friend(860742613)
        #self.client.delete_friend(787076003)
        #self.client.group_delete_member(1405859, 860742613)
        #self.client.group_add_member(1405859, 860742613)
        #body = ('card', [('name', 'chingjun2-test')])
        #self.client.send('group', 'set_card2', body,
        #        version = '1.0',
        #        gid = '1405859',
        #        member = self.client.uid)
        #body = ('add_manager', [], [('manager', [('imid', '787076003')])])
        #self.client.send('group', 'add_manager', body,
        #        version = '1.0',
        #        gid = 1405859)
        #self.client.get_all_teams()
        #self.client.get_all_contacts()
        #self.client.get_self_info()
        #self.client.get_all_groups()
        #self.client.get_group_info(1405859)
        #self.client.get_group_member_list(1003069)
        #self.client.get_group_member_name(1003069)

    def on_friend_request(self, data):
        #self.client.accept_friend_request(data['imid'])
        pass

    def on_contact_info_ready(self):
        print self.client.friend_list
        pickle.dump(self.client.friend_list, open('friends','w'))

if __name__ == '__main__':
    host = getattr(config, 'host', 's1.im.baidu.com')
    port = getattr(config, 'port', 443)
    client = Client(host, port, config.username, config.password)
    handler = Handler(client)

    client.start()
