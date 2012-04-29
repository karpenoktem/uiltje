SMB_HOSTNAME='files.vpn.karpenoktem.nl'
CERT_DOWNLOAD_URI = 'https://www.karpenoktem.nl/smoelen/ik/openvpn/openvpn'+ \
                        '-config-%s.zip'

STATE_UNKNOWN = 0
STATE_CONNECTED = 1
STATE_DISCONNECTED = 2
STATE_CHECKING_CREDS = 3
STATE_PROMPTING_CREDS = 4
