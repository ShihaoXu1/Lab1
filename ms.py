from SocketServer import BaseRequestHandler,ThreadingTCPServer
import threading

BUF_SIZE=1024

medals = [
       {
       'teamName': 'Gauls',
       'gold': 2,
       'silver': 4,
       'bronzer': 0
       },
       { 'teamName': 'Romans',
          'gold': 4,
          'silver': 5,
          'bronzer': 1
       }
    ]

eventTypes = [
       {'eventType':'skate', 'rom_score':6,'gau_score':5},
       {'eventType':'hockey','rom_score':2,'gau_score':4},
       {'eventType':'curling','rom_score':4,'gau_score':3}]
def getMedalTally(teamName):
       medal = filter(lambda t: t['teamName'] == teamName, medals)
       return {'medals':medal[0]} 

def getScore(eventType):
       event = filter(lambda t: t['eventType'] == eventType, eventTypes)
       return {'eventType':event[0]}

def incrementMedalTally(teamName, medalType, auth_id,change):
    if auth_id =='Caco':
       medal = filter(lambda t: t['teamName'] == teamName, medals)
       medal[0][medalType] = medal[0][medalType]+int(change)
       return {'change is finished in medal': medal[0]}
    else:
      return{'error':'NoAuthorization'}

def setScore(eventType,rom_score,gau_score,auth_id,rom_s,gau_s):
    if auth_id =='Caco':
       event = filter(lambda t: t['eventType'] == eventType, eventTypes)
       event[0][rom_score] = int(rom_s)
       event[0][gau_score] = int(gau_s)
       return {'setScore is finished in eventTypes': eventTypes[0]}
    else:
      return{'error':'NoAuthorization'}

class Handler(BaseRequestHandler):
    def handle(self):
        address,pid = self.client_address
        print('%s connected!'%address)
        while True:
            data = self.request.recv(BUF_SIZE)
            if len(data)>0:
                print('receive=',data.decode('utf-8'))
                cur_thread = threading.current_thread()
                #response = '{}:{}'.format(cur_thread.ident,data)
                Url=data.split('/')
                n=len(Url)
                if Url[0]=='getMedalTally':
                   m=getMedalTally(Url[1])
                if Url[0]=='getScore':
                   m=getScore(Url[1])
                if Url[0]=='incrementMedalTally':
                   m=incrementMedalTally(Url[1],Url[2],Url[3],Url[4])
                if Url[0]=='setScore':
                   m=setScore(Url[1],Url[2],Url[3],Url[4],Url[5],Url[6])

                self.request.send('[%s] %s' %("You requese:", m))
            else:
                print('close')
                break

if __name__ == '__main__':
    HOST = ''
    PORT = 8999
    ADDR = (HOST,PORT)
    server = ThreadingTCPServer(ADDR,Handler)  
    print('listening')
    server.serve_forever()
    print(server)