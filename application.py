import requests
import os
from flask import Flask, request

SERVER_IP = 'flask-app-tv.herokuapp.com'   # Edit this line
PORT = 9000

app = Flask(__name__)

@app.route('/ustvgo.m3u')
def playlist_generator():
    playlist = '#EXTM3U'
    info_file = f'{os.path.dirname(__file__)}/ustvgo_channel_info.txt'
    with open(info_file) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            line = line.split('|')
            name = line[0].strip()
            code = line[1].strip()
            logo = line[2].strip()
            playlist += f'\n#EXTINF:-1 tvg-id="{code}" group-title="ustvgo" tvg-logo="{logo}", {name}'
            playlist += f'\nhttps://{SERVER_IP}/channels?id={code}'
    return playlist

@app.route('/channels')
def getChannel():
    code = request.args.get('id')
    data = {'stream' : code}
    pl = requests.post('https://ustvgo.tv/data.php', data=data).text
    base = pl.split('playlist.m3u8')[0]
    head = '#EXTM3U\n#EXT-X-VERSION:3\n#EXT-X-STREAM-INF:BANDWIDTH=818009,RESOLUTION=640x360,CODECS="avc1.64001f,mp4a.40.2"\n'
    m3u = requests.get(pl).text.strip().split('\n')[-1]
    return head + base + m3u + pl

if __name__ == '__main__':
    app.run('0.0.0.0', PORT)
