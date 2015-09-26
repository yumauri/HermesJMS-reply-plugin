###
# @author Victor Didenko
# yumaa.verdin@gmail.com
# 05.12.2014
#
# ReplyPlugin allows to reply to the message
#

import time

from javax.swing import Action, AbstractAction, JPopupMenu, JMenuItem, ImageIcon
from java.awt.event import ActionEvent, ActionListener

from java.lang import Throwable
from java.util import ArrayList
from java.util.regex import Pattern

# from hermes.browser import IconCache
from hermes.browser.dialog.message import MessageEditorDialog
from hermes.browser.actions import AbstractEditedMessageHandler


# current timestamp
current_milli_time = lambda: long(round(time.time() * 1000))


# message handler
class MsgHandler(AbstractEditedMessageHandler):

	def __init__(self, browser, hermes, replyToQueue, replyToDomain):
		AbstractEditedMessageHandler.__init__(self, hermes)
		self.browser = browser
		self.replyToQueue = replyToQueue
		self.replyToDomain = replyToDomain

	def onMessage(self, message):
		list = ArrayList()
		list.add(message)
		self.browser.getActionFactory().createMessageCopyAction(self.hermes, self.replyToQueue, self.replyToDomain, list, False, False)


# context menu item handler
class MenuItemHandler(ActionListener):

	def __init__(self, plugin, hermes, replyToId, replyToQueue, replyToDomain):
		self.plugin = plugin
		self.hermes = hermes
		self.replyToId = replyToId
		self.replyToQueue = replyToQueue
		self.replyToDomain = replyToDomain

	def actionPerformed(self, event):
		self.plugin.replyTo(self.hermes, self.replyToId, self.replyToQueue, self.replyToDomain)


# reply plugin
class ReplyPlugin(AbstractAction):

	def __init__(self, browser, initPath):
		self.browser = browser
		self.putValue(Action.NAME, "ReplyPlugin")
		self.putValue(Action.SHORT_DESCRIPTION, "Reply to the message")
		self.putValue(Action.SMALL_ICON, ImageIcon(initPath.replace("__init__.py", "reply.gif"))) # IconCache.getIcon("hermes.replay")

		commandBar = browser.getDockableBarManager().getDockableBar("Scripts")
		if commandBar == None:
			commandBar = browser.createDockableBar("Scripts")
			browser.getDockableBarManager().addDockableBar(commandBar)
		self.button = commandBar.add(self)

	def actionPerformed(self, event):
		messages = self.browser.getSelectedMessages()
		numMessages = messages.size()

		if numMessages == 0:
			self.browser.showInformationDialog("No messages selected")
			return

		if numMessages > 1:
			self.browser.showInformationDialog("%d messages selected, choose one" % numMessages)
			return

		message = messages.get(0)
		replyToId = message.getJMSMessageID()
		replyToQueue0 = message.getJMSReplyTo()
		if replyToQueue0 != None:
			replyToQueue0 = replyToQueue0.getQueueName()
			p = Pattern.compile("[^\\s:/]+://[^\\s:/]*/([^\\s:/?]+)\\??.*")
			m = p.matcher(replyToQueue0)
			if m.matches():
				replyToQueue0 = m.group(1)
			else:
				replyToQueue0 = None

		dNode = self.browser.getBrowserTree().getFirstSelectedDestinationNode()
		hNode = self.browser.getBrowserTree().getSelectedHermesNode()
		if dNode == None or hNode == None:
			self.browser.showInformationDialog("Unknown destination, select destination queue")
			return

		hermes = hNode.getHermes()
		replyToQueue1 = dNode.getDestinationName()
		replyToDomain = dNode.getDomain()

		if replyToQueue0 == None and replyToQueue1 == None:
			self.browser.showInformationDialog("Unknown destination, select destination queue")
			return

		# show menu
		if replyToQueue0 != None and replyToQueue1 != None and replyToQueue0 != replyToQueue1:
			menu = JPopupMenu()
			q0item = JMenuItem(replyToQueue0)
			q0item.addActionListener(MenuItemHandler(self, hermes, replyToId, replyToQueue0, replyToDomain))
			menu.add(q0item)
			q1item = JMenuItem(replyToQueue1)
			q1item.addActionListener(MenuItemHandler(self, hermes, replyToId, replyToQueue1, replyToDomain))
			menu.add(q1item)
			menu.show(self.button, 0, self.button.getHeight())
			return

		# show new message dialog
		else:
			if replyToQueue0 != None:
				replyToQueue = replyToQueue0
			else:
				replyToQueue = replyToQueue1
			self.replyTo(hermes, replyToId, replyToQueue, replyToDomain)

	def replyTo(self, hermes, replyToId, replyToQueue, replyToDomain):
		try:
			msg = hermes.createTextMessage("")
			msg.setJMSTimestamp(current_milli_time())
			msg.setJMSCorrelationID(replyToId)

			dialog = MessageEditorDialog(msg, replyToQueue, replyToDomain, MsgHandler(self.browser, hermes, replyToQueue, replyToDomain))
			dialog.setLocationRelativeTo(self.browser)
			dialog.setVisible(True)
		except (Throwable), e:
			self.browser.showErrorDialog(e.getMessage())
		except (Exception), e:
			self.browser.showErrorDialog(str(e))
