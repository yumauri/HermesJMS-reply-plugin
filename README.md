# HermesJMS reply plugin

This is a plugin for [HermesJMS](http://www.hermesjms.com/), it opens new message dialog with filled field **JMSCorrelationID** = **JMSMessageID** of selected message.

## Installation

When running HermesJMS, open *JyConsole* (*Jython*) in the left bottom corner, then type and execute following:
```python
import sys; sys.path
```

![lib path](https://github.com/yumauri/HermesJMS-reply-plugin/wiki/0.png)

Look for the path to the library folder (usually `%HERMES_HOME%\lib\Lib`) and copy folder **reply_plugin** into it.

Edit file `%HOMEDRIVE%\%HOMEPATH%\.hermes\hermesrc.py` (if there is no such file – create it), and add following:
```python
# ReplyTo plugin
import reply_plugin
```
If everything is ok, then after HermesJMS's restart you'll see new toolbar with single button «*Reply to the message*».

![plugin button](https://github.com/yumauri/HermesJMS-reply-plugin/wiki/1.png)

## Usage

Select a *message*, you want to send reply for; then in the tree on the left side select *queue*, you want to send reply to; and click button «*Reply to the message*». Hereby standard dialog «Create new message» will be created, and field **JMSCorrelationID** value will be setted to **JMSMessageID** value of selected message. Further you can open *Payload* tab and type/paste message as usual.

If **JMSReplyTo** field value is not empty in the selected message – plugin will try to get destination queue name from that value. If in than same moment in the tree on the left side there is another queue is selected – then on button «Reply to the message» click first of all you will need to choose destination queue in the appeared submenu.