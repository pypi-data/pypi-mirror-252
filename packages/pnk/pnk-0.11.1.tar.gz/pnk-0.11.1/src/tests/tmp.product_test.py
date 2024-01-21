#!/usr/bin/python3

import itertools

iterator = itertools.product(["tutu"], ["1v.e0e.mail.ru", "0v.e0e.mail.ru"])
for x in iterator:
    print(x)
