"""
This file contains functions for parsing different forms of text.
The functions convert the various text formats into simple strings.
"""
import os

import PyPDF2
import docx
import ebooklib
import html2text
import pysrt
import requests
import re
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from ebooklib import epub


def parse_docx(filename):
    """
    This function parses a docx file by parsing the file given by the filename and returning a string of the
    content in the file.
    :param filename: The docx file to parse.
    :return: A string containing the docx file's contents.
    """
    doc = docx.Document(filename)
    full_text = ""
    for paragraph in doc.paragraphs:
        paragraph.style = 'Normal'
        full_text += paragraph.text
    full_text = os.linesep.join([s for s in full_text.splitlines() if s])  # strips out blank lines
    return full_text


def parse_pdf(filename):
    """
    This function parses a pdf file by parsing the file given by the filename and returning a string of the content in
    the file.
    :param filename: The pdf file to parse.
    :return: A string containing the pdf file's contents.
    """
    with open(filename, 'rb') as pdf:
        pdf_reader = PyPDF2.PdfFileReader(pdf)
        page_objects = []
        full_text = ""
        filtered_text = ""
        for x in range(0, pdf_reader.getNumPages()):
            page_objects.append(pdf_reader.getPage(x))
        for page_object in page_objects:
            full_text += page_object.extractText()
    for line in full_text.split('\n'):
        if not re.match(r'^\s*$', line):
            filtered_text += (line + '\n')
    return filtered_text


def parse_epub(filename):
    """
    This function parses an epub file by parsing the file given by the filename and returning a string of the content
    in the file.
    :param filename: The epub file to parse.
    :return: A string containing the epub file's contents.
    """
    book = epub.read_epub(filename)
    full_text = ""
    for obj in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        full_text += (obj.get_content()).decode('utf-8')
    full_text = html2text.html2text(full_text)
    full_text = os.linesep.join([s for s in full_text.splitlines() if s]) # strips out blank lines
    return full_text


def parse_txt(filename):
    """
    This function parses a txt file by parsing the file given by the filename and returning a string of the content
    in the file.
    :param filename: The txt file to parse.
    :return: A string containing the txt file's contents.
    """
    with open(filename) as txt_file:
        full_text = txt_file.read()
        full_text = os.linesep.join([s for s in full_text.splitlines() if s])  # strips out blank lines
    return full_text


def parse_srt(filename):  # parses .srt subtitle files
    """
    This function parses srt subtitle file by parsing the file given by the filename and returning a string of the
    content in the file.
    :param filename: The srt subtitle file to parse.
    :return: A string containing the srt subtitle file's contents.
    """
    subs = pysrt.open(filename)
    full_text = ""
    for sub in subs:
        full_text += sub.text
        if (sub.text).endswith("."):
            full_text += " "
        else:
            full_text += ". "
    return full_text


def search_songs(song, artist=""):
    """
    This function searches for a song given a song title and artist and returns a string containing the lyrics.
    :param song: The song title to search.
    :param artist: The artist of the song to search.
    :return: A string containing the song's lyrics.
    """
    params = {
        'uid': 6191,
        'tokenid': 'fTm7bNQjneSL7j7D',
        'term': song
    }
    r = requests.get('http://www.stands4.com/services/v2/lyrics.php', params=params)
    song = song.lower()
    artist = artist.lower()
    e = ET.fromstring(r.text)
    song_link = ""
    for res in e.findall('result'):
        song_search = (res.find('song').text).lower()
        artist_search = (res.find('artist').text).lower()
        if artist:
            if (artist in artist_search and song in song_search) or (artist_search in artist and song_search in song):
                song_link = res.find('song-link').text
                break
        else:
            if song in song_search or song_search in song:
                song_link = res.find('song-link').text
                break
    if not song_link:
        return 0
    soup = BeautifulSoup((requests.get(song_link)).text, 'html.parser')
    text = soup.find('pre', attrs={'id': 'lyric-body-text', 'class': 'lyric-body'})
    full_text = os.linesep.join([s for s in (text.text).splitlines() if s])  # strips out blank lines
    text_list = [sent.strip() for sent in full_text.split('\n')]
    full_text = ". ".join(text_list)
    return full_text


def search_website(website):
    """
    This function gets the contents from a website and returns its contents as a string.
    :param website: The website title to retrieve content from.
    :return: A string containing the website's contents.
    """
    r = requests.get(website)
    full_text = html2text.html2text(r.text)
    return full_text
