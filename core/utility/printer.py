
colors = {'BOLD': '\033[1m','BLUE': '\033[34m' ,
            'GREEN': '\033[32m','YELLOW' :'\033[33m',
            'RED': '\033[91m','ENDC' : '\033[0m','CIANO' :'\033[1m','ORAN' : '\033[91m',
            'GREY': '\033[37m','DARKGREY' : '\033[1;30m','UNDERLINE' : '\033[4m'}

def banner():
    print ('''

            _ _             _    _
  _ __ ___ (_) |_ _ __ ___ | | _(_)_ __
 | '_ ` _ \| | __| '_ ` _ \| |/ / | '_ \.
 | | | | | | | |_| | | | | |   <| | | | |
 |_| |_| |_|_|\__|_| |_| |_|_|\_\_|_| |_|

''')

def setcolor(text,color='',underline=False):
    strcolored = {
        'blue':'{}{}{}{}'.format(colors['BOLD'],colors['BLUE'],text,colors['ENDC']),
        'red': '{}{}{}{}'.format(colors['BOLD'], colors['RED'], text, colors['ENDC']),
        'green': '{}{}{}{}'.format(colors['BOLD'], colors['GREEN'], text, colors['ENDC']),
        'yellow': '{}{}{}{}'.format(colors['BOLD'], colors['YELLOW'], text, colors['ENDC']),
        'grey': '{}{}{}{}'.format(colors['BOLD'], colors['GREY'], text, colors['ENDC']),
        'darkgrey': '{}{}{}{}'.format(colors['BOLD'], colors['DARKGREY'], text, colors['ENDC'])
        }
    if underline:
        return colors['UNDERLINE']+strcolored[color]
    return strcolored[color]
