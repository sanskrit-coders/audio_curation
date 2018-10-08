"""Shortening the name, to remove stuff like 'Sarga BK' (because my car display doesn't scroll!)"""

import mutagen.easyid3

def cleanPart(p):
    p = p.strip().strip('-').strip()
    while '  ' in p:
        p = p.replace('  ', '')
    return p

def titleParts(old, substr):
    parts = old.split(substr)
    parts = [cleanPart(p) for p in parts]
    parts = [p for p in parts if p]
    return parts

def newTitle(old, sarga, name):
    sargastr = {
        1: 'Sarga BK',
        2: 'Sarga AYK',
        3: 'Sarga ARK',
        4: 'Sarga KSK',
        5: 'Sarga SK',
        6: 'Sarga YK'}[sarga]
    parts = titleParts(old, sargastr)
    if sarga == 1 and len(parts) == 1 and parts[0] == 'dhyaana slokas':
        return '1.000-dhyaana slokas'
    if sarga == 4 and len(parts) == 1 and parts[0] == '001 dhyana slokas 2.mp3':
        return '4.001-dhyana slokas'
    if sarga == 6:
        prefix = 'Kanda.6.YK-'
        suffix = '.mp3'
        assert name.startswith(prefix), name
        assert name.endswith(suffix), name
        ret = '6.' + name[len(prefix):-len(suffix)]
        if ret.endswith('_0') or ret.endswith('_1'): ret = ret[:-2]
        return ret.strip()
    assert len(parts) == 2, old
    return ('%d.' % sarga) + '-'.join(parts)

def allNew(sarga):
    for name in glob.glob('K*'):
        f = mutagen.easyid3.EasyID3(name)
        title = f['title']
        newtitle = newTitle(title[0], sarga, name)
        if newtitle.endswith('.mp3'):
            newtitle = newtitle[:-4]
        print('%-80s %s' % (newtitle, name))
        f['title'] = newtitle
        f.save()

# Run allNew(1), allNew(2) etc in respective directories
