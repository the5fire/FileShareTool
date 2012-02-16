#_*_encoding=utf-8_*_

from xmlrpclib import ServerProxy,Fault
from server import Node,UNHANDLED  #引入前面的程序
from utils import randomString  #引入前面的程序
from threading import Thread
from time import sleep
from os import listdir
import os
import sys
import wx

HEAD_START = 0.1 #Seconds
SECRET_LENGTH = 100

class ListableNode(Node):
		def list(self):
				return listdir(self.dirname)

class Client(wx.App):

		def __init__(self, url, dirname, urlfile):
				self.secret = randomString(SECRET_LENGTH)
				n = ListableNode(url,dirname, self.secret)
				t = Thread(target=n._start)
				t.setDaemon(1)
				t.start()

				sleep(HEAD_START)
				self.server = ServerProxy(url)
				super(Client, self).__init__()

		def updateList(self):
				print self.server.list()
				self.files.Set(self.server.list())

		def updateRemoteList(self, remote_url):
				#print self.server
				self.remotefiles.Set(self.server.remoteList(remote_url))

		def OnInit(self):

				win = wx.Frame(None, title="File Share Tool",size=(800,499))

				bkg = wx.Panel(win)

				#self.input = input = wx.TextCtrl(bkg)
				self.urlinput = urlinput = wx.TextCtrl(bkg)

				self.urlinput.AppendText('http://192.168.1.106:4242')

				url_text = wx.StaticText(bkg, -1, 'remote URL:', size=(80, 25))

				self.statusBar = win.CreateStatusBar()
				submit = wx.Button(bkg, label="Fetch",size=(80,25))
				submit.Bind(wx.EVT_BUTTON, self.getRemoteResource)

				hbox = wx.BoxSizer()

				hbox.Add(url_text, proportion=1,flag=wx.ALL, border=10)
				hbox.Add(urlinput, proportion=1,flag=wx.ALL | wx.EXPAND, border=10)
				#hbox.Add(input, proportion=1, flag=wx.ALL | wx.EXPAND, border=10)
				hbox.Add(submit, flag=wx.TOP | wx.BOTTOM | wx.RIGHT, border=10)

				self.files = files = wx.ListBox(bkg,size=(350,400))
				self.remotefiles = remotefiles = wx.ListBox(bkg,size=(350,400))
				self.remotefiles.Bind(wx.EVT_LISTBOX_DCLICK, self.listDClick)


				vbox = wx.BoxSizer(wx.VERTICAL)
				vbox.Add(hbox, proportion=0, flag=wx.EXPAND)
				
				hbox2 = wx.BoxSizer()

				hbox2.Add(remotefiles,proportion=1, flag=wx.ALL | wx.EXPAND, border=10)
				hbox2.Add(files, proportion=1,flag=wx.ALL | wx.EXPAND, border=10)

				vbox.Add(hbox2,proportion=0, flag=wx.EXPAND)

				bkg.SetSizer(vbox)

				win.Show()
				self.updateList()

				return True

		def getRemoteResource(self, event):
				query_url = self.urlinput.GetValue()
				if query_url == '':
						sefl.statusBar.SetStatusText('query url can not be null!')
						return

				self.server.hello(query_url)
				self.updateRemoteList(query_url)
		
		def listDClick(self, event):
				#print 'on click'
				query = self.remotefiles.GetString(self.remotefiles.GetSelection())
				self.fetchHandler(query)


		def fetchHandler(self, query):

				#query =self.input.GetValue()
				#query_url = self.urlinput.GetValue()

				if query == '':
						self.statusBar.SetStatusText('query string can not be null!')
						return
				#if query_url != '':
				#		self.server.hello(query_url.strip())
				try:
						self.server.fetch(query, self.secret)
						self.statusBar.SetStatusText('download the file %s successed!' % query)
						self.updateList()

				except Fault,f:
						if f.faultCode != UNHANDLED: raise
						self.statusBar.SetStatusText("Counldn't find the file %s" % query)

def main():
		urlfile, directory,url = 'urls', 'share','http://192.168.1.203:4242'#sys.argv[1:]
		if not os.path.exists('share'):
				os.makedirs('share')
		client = Client(url, directory, urlfile)
		client.MainLoop()

if __name__ == '__main__': main()
