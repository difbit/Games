#!/usr/bin/env python
# -*- coding: utf-8 -*-

numbers = {'1': u'yksi', '2': u'kaksi', '3': u'kolme', '4': u'neljä', '5': u'viisi', '6': u'kuusi', \
        '7': u'seitsemän', '8': u'kahdeksan', '9': u'yhdeksän', '10': u'kymmenen'}

for hundred in range(0, 11):
    if hundred == 0:
        sata = ''
    elif hundred == 1:
        sata = 'sata'
    elif hundred == 10:
        print 'tuhat'
        break
    else:
        sata = numbers[str(hundred)] + 'sataa'
    if sata != '':
        print sata
    for num in range(0, 3):
        start = 1
        end = 10
        if num == 0:
            msg = ""
            end = 11
        elif num == 1:
            msg = 'toista'
        else:
            msg = numbers['10'] + u'tä'
            start = 2
        for i in range(start, end):
            message = numbers[str(i)] + msg
            if num >= 2:
                for ten_number in range(0, 10):
                    if ten_number == 0:
                        ten_add = ""
                    else:
                        ten_add = numbers[str(ten_number)]
                    print sata + message + ten_add
            else:
                print sata + message

