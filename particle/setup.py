# -*- coding: utf-8 -*-
import cx_Freeze
import pygame

base = None

executables = [cx_Freeze.Executable("particle.py", base=bae)]

cx_Freeze.setup(
    name="Particle",
    options={"build_exe": {"packages":["pygame"]}},
    description="Particle",
    executables=executables
    )
