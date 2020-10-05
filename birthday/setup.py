# -*- coding: utf-8 -*-
import cx_Freeze
import pygame

base = None

executables = [cx_Freeze.Executable("birthday.py", base=base)]

cx_Freeze.setup(
    name="Birthday",
    options={"build_exe": {"packages":["pygame"]}},
    description="Birthday",
    executables = executables
    )
