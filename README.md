# 3DS_Game_Server

Creates a web page listing from user-provided CIAs.
Generated web page includes a sortable table with auto-generated QR codes for downloading/installing the CIAs over LAN via FBI.
Game titles link to descriptions on www.gametdb.com, and table also pulls cover art from there.
Uses Python SimpleHTTPServer, so just one download request/thread at a time.

To do (maybe someday, but I don't really need it): Add error logging for unparseable titleids and games not found in release XML

Requires Python 2.7

To use an updated releases list, download '3dsreleases.xml' from http://www.3dsdb.com/

1. Edit  BuildCatalog.py
- Set "releasesXML" and "ciaFolder"
2. Create a folder to match the name set in "ciaFolder"
3. Dump all desired CIAs into the created folder (subfolders are OK)
4. Run BuildCatalog.py
5. Edit StartServer.py
- Set "PORT"
6. Run StartServer.py