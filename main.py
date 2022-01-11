import json
import urllib.parse
import base64
v2ray_all=[{'v2ray_cfg':'ws'},{'v2ray_cfg':'quic'},{'v2ray_cfg':'tls'}]   # all v2ray plugins

servercfgs = [  
    {
        'server': 'server1.domain',
        'subconfigs': [*v2ray_all, {'v2ray_cfg':'plain','server_port': 10443}],   # use default port, v2ray ws on 80, v2ray quic on 443, v2ray tls 443, and plain on 10443 port 
    },
    {
        'server': 'server2.domain',
        'password':'customizedbreakwall',    # customized password for this server 
        'method':'chacha20-ietf-poly1305',    # customized method for this server 
        'ipv6': True,
        'subconfigs': [*v2ray_all, {'server_port': 10443}]    # same as server1.domain
    },
    {
        'server': 'server3.domain',
        'subconfigs': [{'v2ray_cfg':'ws','server_port': 8080}, {'v2ray_cfg':'quic','server_port': 1443}]   # specify the port 8080 for v2ray ws, 1443 for v2ray quic
    }
]

default_config = {'password':'breakwall',     # default config for all server
          'method':'chacha20-ietf-poly1305',
          'route': 'bypass-lan-china',
          'remote_dns': 'dns.google',
          'ipv6': False,
          'metered': False,
          'udpdns': False,
          'remarks': '',
          'proxy_apps':
              {'enabled': True, 'bypass': False}
          }

android_list=['android', 'com.google.android.wearable.app',     # apps that needs proxy on android, welcome PR to add more
                    'com.instagram.android',
                    'com.google.android.projection.gearhead',
                    'com.google.android.webview',
                    'com.google.android.marvin.talkback',
                    'com.google.android.setupwizard',
                    'com.google.android.apps.restore',
                    'com.google.android.captiveportallogin',
                    'com.google.android.ims', 'com.android.chrome',
                    'com.google.android.configupdater',
                    'com.google.android.apps.turbo', 'com.facebook.katana',
                    'com.facebook.appmanager', 'com.facebook.services',
                    'com.google.android.inputmethod.latin',
                    'com.google.android.gm',
                    'com.google.android.googlequicksearchbox',
                    'com.google.android.partnersetup',
                    'com.google.android.apps.walletnfcrel',
                    'com.google.ar.core', 'com.android.vending',
                    'com.google.android.gms',
                    'com.google.android.play.games',
                    'com.google.android.tts', 'com.google.android.gsf',
                    'com.google.android.syncadapters.contacts',
                    'com.google.android.apps.chromecast.app',
                    'com.google.android.keep', 'com.facebook.orca',
                    'com.google.android.printservice.recommendation',
                    'com.twitter.android',
                    'com.google.android.wearable.app',
                    'com.google.android.youtube',
                    'com.google.android.apps.docs',
                    'com.google.android.apps.messaging',
                    'com.google.android.apps.fitness',
                    'com.google.android.apps.maps',
                    'com.google.android.apps.docs.editors.slides',
                    'com.google.android.feedback',
                    'com.google.android.apps.setupwizard.searchselector',
                    'com.google.android.apps.wellbeing',
                    'com.google.android.apps.docs.editors.docs',
                    'com.google.android.calendar',
                    'com.google.android.deskclock', 'com.google.ar.lens',
                    'com.google.android.talk', 'com.google.android.dialer',
                    'com.google.android.apps.photos',
                    'com.google.android.networkstack',
                    'com.google.android.apps.translate',
                    'com.google.android.apps.docs.editors.sheets',
                    'com.google.android.apps.work.oobconfig',
                    'com.google.android.apps.authenticator2',
                    'com.google.chromeremotedesktop',
                    'com.google.android.contacts',
                    'com.android.providers.downloads']

default_config['proxy_apps']['android_list']=android_list

def android_json(filename='android.json'):
    custom_cfgs=[]
    result_cfgs=[]
    v2ray_cfgs = {
        'plain': {},
        'ws': {'server_port': 80, 'plugin': 'v2ray-plugin', 'plugin_opts': 'host='},
        'quic': {'server_port': 443, 'plugin': 'v2ray-plugin', 'plugin_opts': 'mode=quic;host='},
        'tls': {'server_port': 443, 'plugin': 'v2ray-plugin', 'plugin_opts': 'tls;host='}
    }
    for servercfg in servercfgs:
        subconfigs=servercfg['subconfigs'].copy()
        del servercfg['subconfigs']
        for subconfig in subconfigs:
            config=servercfg.copy()
            if not 'v2ray_cfg' in subconfig:
                subconfig['v2ray_cfg'] = 'plain'
            config = {**config, **v2ray_cfgs[subconfig['v2ray_cfg']]}
            config={**config,**subconfig}
            del config['v2ray_cfg']
            assert 'server' in config
            if not subconfig['v2ray_cfg']=='plain':
                if config['plugin_opts'].endswith('host='):
                    config['plugin_opts'] = config['plugin_opts'] + config['server']
            custom_cfgs.append(config)
            config = {**default_config, **config}
            assert 'server_port' in config
            if config['remarks'] == '':
                config['remarks'] = "{} {} {}".format(config['server'], config['server_port'], subconfig['v2ray_cfg'])
            result_cfgs.append(config)
    with open(filename, 'w') as f:
        json.dump(result_cfgs, f)
    return result_cfgs

def SIP002_tofile(configs,filename='subscription'):
    SS_URIs=[]
    for config in configs:
        userinfo = base64.b64encode(bytes(config['method']+':'+config['password'], 'utf-8'))
        SS_URI = 'ss://' + str(userinfo,'utf-8') + '@'+ config['server']+ ':' + str(config['server_port'])
        if 'plugin' in config:
            SS_URI_opts = config['plugin']+';'+config['plugin_opts']
            SS_URI_opts= 'plugin=' + urllib.parse.quote(SS_URI_opts)
            SS_URI=SS_URI+ '/?'+SS_URI_opts
        SS_URI=SS_URI+'#'+ urllib.parse.quote(config['remarks'])
        SS_URIs.append(SS_URI)
    with open(filename, 'w') as f:
        for SS_URI in SS_URIs:
            f.write("%s\n" % SS_URI)

if __name__ == '__main__':
    json_cfgs=android_json()
    SIP002_tofile(json_cfgs)

