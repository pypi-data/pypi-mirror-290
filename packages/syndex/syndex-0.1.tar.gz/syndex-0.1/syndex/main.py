#!/usr/bin/env python3

import argparse
import os
import xml.etree.ElementTree as ET
import urllib.request
from typing import Optional
from datetime import datetime

def is_url_valid(url: str) -> bool:
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            return response.status < 400
    except urllib.error.URLError:
        return False

def add_bookmark(file_path: str, url: str, message: Optional[str] = None):
    if not is_url_valid(url):
        print(f"Error: {url} is not a valid or accessible URL.")
        return

    if not os.path.isfile(file_path):
        root = ET.Element('rss', {'version': '2.0'})
        channel = ET.SubElement(root, 'channel')
    else:
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            channel = root.find('channel')
            if channel is None:
                print(f"Error: {file_path} is not a valid RSS file.")
                return
        except ET.ParseError:
            print(f"Error: {file_path} is not a valid XML file.")
            return

    item = ET.SubElement(channel, 'item')
    ET.SubElement(item, 'link').text = url
    ET.SubElement(item, 'pubDate').text = datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000")
    
    if message:
        ET.SubElement(item, 'description').text = message
    else:
        ET.SubElement(item, 'description', {'unspecified': 'true'})

    tree = ET.ElementTree(root)
    tree.write(file_path, encoding='utf-8', xml_declaration=True)
    print(f"Added bookmark to {file_path}: {url}")

def main():
    parser = argparse.ArgumentParser(description='Syndex - Add Bookmarks')
    parser.add_argument('filepath', type=str, help='Path to the XML file')
    parser.add_argument('url', type=str, help='URL of the bookmark')
    parser.add_argument('message', type=str, nargs='?', help='Description of the bookmark')

    args = parser.parse_args()
    add_bookmark(args.filepath, args.url, args.message)

if __name__ == '__main__':
    main()
