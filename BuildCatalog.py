import os
import sys
from struct import unpack
import xml.etree.ElementTree as ET
import shutil
import SimpleHTTPServer
import SocketServer
import socket
import webbrowser

releasesXML = '3dsreleases.xml' # Name of XML downloaded from http://www.3dsdb.com/
ciaFolder = 'CIAs' # Root folder with CIAs

def buildReleaseLookup(input_file):
    tree = ET.parse(input_file)
    root = tree.getroot()
    return(root)

def getTitleID(input_file):
    cia_file = open(input_file, 'r+b')
    cia_header = cia_file.read(0x20)

    # Find offset for tmd
    cert_offset = 0x2040
    cert_size = unpack('<I', cia_header[0x08:0x0C])[0]
    tik_size = unpack('<I', cia_header[0x0C:0x10])[0]
    tmd_size = unpack('<I', cia_header[0x10:0x14])[0]
    tmd_offset = cert_offset + cert_size + 0x30 + tik_size
    # print(format(tmd_offset, '08x'))

    # Read titleid from tmd
    cia_file.seek(tmd_offset + 0x18C)
    titleid = format(unpack('>Q', cia_file.read(0x8))[0], '016x')
    cia_file.close()
    return(titleid)
    
def addListing(release):
    global strTable
    name = release.find('name').text
    print('Found game "%s"...' % name)
    id = release.find('serial').text.split('-')
    stringcount = len(id)
    print('count "%s"..' % stringcount)
    if stringcount == 3:
        id = release.find('serial').text.split('-')[2]
    elif stringcount == 2:
        id = release.find('serial').text.split('-')[1]

    coverURL = 'https://art.gametdb.com/3ds/box/US/%s.png' % id
    dbURL = 'https://www.gametdb.com/3DS/%s' % id
    strTable = strTable + '''
    <tr>
        <td><a href="%s">%s</a></td>
        <td><img src="%s"></td>
        <td><a href="%s"><div id="qrcode%s"></div>
            <script type="text/javascript">
            var loc = window.location.href;
            var dir = loc.substring(0, loc.lastIndexOf('/'));
            new QRCode(document.getElementById("qrcode%s"),{width : 125,height : 125,text: encodeURI(dir + "/%s")});
            </script></a></td>
    </tr>''' % (dbURL,name,coverURL,relpath,id,id,relpath.replace(os.sep, '/'))
    print('Done.')
    
releases = buildReleaseLookup(releasesXML)

strTable = '''<html>
    <script type="text/javascript" src="jquery.min.js"></script>
    <script type="text/javascript" src="qrcode.js"></script>
    <script src="sorttable.js"></script>
        <table class="sortable" border="1">
            <tr>
                <th>Title</th>
                <th>Cover</th>
                <th>Download</th>
            </tr>'''

# Process every CIA in ciaFolder and subfolders
for (root,dirs,files) in os.walk(os.path.join(os.path.dirname(__file__),ciaFolder)):
    for file in files:
        if file.endswith('.cia'):
            filepath = os.path.join(os.path.join(root, file))
            relpath = os.path.relpath(os.path.join(root, file),os.path.dirname(__file__))
            titleid = getTitleID(filepath)
            print('Processing "%s"...' % file)
            print('Title ID: %s' % titleid)
            for release in releases:
                if release.find('titleid').text.lower() == titleid.lower():
                    addListing(release)
                    break

strTable = strTable+"</table></html>"

htmlFile = 'index.html'
hs = open(htmlFile, 'w')
hs.write(strTable)
hs.close()
