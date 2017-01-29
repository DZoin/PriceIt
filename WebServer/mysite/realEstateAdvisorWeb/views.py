from django.shortcuts import render

from django.http import HttpResponse
import sqlite3


def index(request):
     with sqlite3.connect("/home/zoin/workspace/RealEstateAdvisor/realEstate.sqlite") as db:
        dropdown = ''
        cursor = db.execute("SELECT Name FROM Districts")
        for row in cursor:
            dropdown += '<option value="{0}">{0}</option>'.format(row[0].encode('utf-8'))
        html = '''<html><body><form align="center">
                      Area:<br>
                      <input type="text" name="Area">
                      <div align="center">
                       <select name="mydropdown">''' + dropdown + '''</select>
                      </div>
                    </form></body></html'''
        return HttpResponse(html)
