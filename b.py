#!/usr/bin/python3

from bottle import route, run, template, get, post, request

@route('/')
def index():
    with open("order.txt", "r") as f:
        ls = f.readlines()

    ls = [l.rstrip("\n") for l in ls]

    if len(ls):
        return template('order.tpl', name=ls[0], products=ls[1:])
    else:
        return "<meta http-equiv='refresh' content='1'><h1>Make an order!</h1>"

run(host='localhost', port=8080)
