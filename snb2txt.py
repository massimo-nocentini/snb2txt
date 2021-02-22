
from os import walk, listdir
from xml.dom import minidom
import zipfile
import sys
import tempfile

main_path = sys.argv[1]
prefix = main_path + ('' if main_path.endswith('/') else '/')

_, _, filenames = next(walk(main_path))

snbs = list(filter(lambda f: f.endswith('.snb'), filenames))

print('I have to process {} snb files.'.format(len(snbs)))

for snb in snbs:

    path = prefix + snb

    with tempfile.TemporaryDirectory() as temp:

        print('Processing: ' + path)

        with zipfile.ZipFile(path, 'r') as zip_ref:
            zip_ref.extractall(temp)
        
        # parse an xml file by name
        mydoc = minidom.parse(temp + '/snote/snote.xml')

        items = mydoc.getElementsByTagName('sn:t')

        # all item attributes
        content = '\n'.join(elem.firstChild.data for elem in items)

        with open(prefix + snb.replace('snb', 'txt'), 'w') as f:
            f.write(content)

print('Completed')
