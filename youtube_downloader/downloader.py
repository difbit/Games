#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytube

def download():
    """A simple code to download Youtube audios"""
    url = input()
    pytube.YouTube(url).streams.get_audio_only().download(
            '../../../Youtube_downloads')

download()
