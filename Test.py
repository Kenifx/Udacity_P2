#encoding = utf-8
import requests
import bs4
import expanddouban

list1 = ['aa']
list2 = ['b']

def output(list1,list2):
    return "this is {}, this is {}".format(list1,list2)

print(output(list1,list2))