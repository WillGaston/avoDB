import click

from api.routes.messages import *
from api.routes.tables import *

#----------------------------------------------#
#           Database Commands                  #
#----------------------------------------------#

@click.group()
def msg():
  pass

@click.command(help="--userId <*userId*>")
@click.option('--userId', prompt=True, help="id of the user to have a conversation with")
def initiateConvo(userid):
  initiateConvoRoute(userid)

@click.command(help="")
def viewConvos():
  viewConvosRoute()

@click.command(help="--message <*message*>")
@click.option('--message', prompt=True, help="messaqge to send")
def sendMsg(message):
  sendMsgRoute(message)

@click.command(help="")
def viewMsgs():
  viewMsgsRoute()

msg.add_command(initiateConvo)
msg.add_command(viewConvos)
msg.add_command(sendMsg)
msg.add_command(viewMsgs)
