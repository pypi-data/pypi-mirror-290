lagrange_config = {
    'Logging': {
        'LogLevel': {
            'Default': 'Information',
            'Microsoft': 'Warning',
            'Microsoft.Hosting.Lifetime': 'Information'
        }
    },
    'SignServerUrl': 'https://sign.lagrangecore.org/api/sign',
    'MusicSignServerUrl': '',
    'Account': {
        'Uin': 0,
        'Password': '',
        'Protocol': 'Linux',
        'AutoReconnect': True,
        'GetOptimumServer': True
    },
    'Message': {
        'IgnoreSelf': True,
        'StringPost': False
    },
    'QrCode': {
        'ConsoleCompatibilityMode': False
    },
    'Implementations': [
        {
            'Type': 'ReverseWebSocket',
            'Host': '127.0.0.1',
            'Port': 8000,
            'Suffix': '/onebot/v11/ws',
            'ReconnectInterval': 5000,
            'HeartBeatInterval': 5000,
            'HeartBeatEnable': True,
            'AccessToken': ''
        }
    ]
}
