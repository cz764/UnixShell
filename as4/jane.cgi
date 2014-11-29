#!/usr/bin/python

import cgi
import cgitb  # for troubleshooting
import subprocess
import urllib
import operator
cgitb.enable() 
question = "/home/cz764/ost/as3/question"

class Answer(object):
	def __init__(self, aid=None, vote=None,content=None):
		self.aid = aid
		self.vote = vote
		self.content = content

def uniqid():
    from time import time
    return hex(int(time()*10))[2:]

def listQuestion():
	print "<h1>Question List: </h1>"
	print """<p><a href="addQuestion.html" class="addQuestion">
			<input type="button" value="Add Question"></a></p>"""
	p = subprocess.Popen([question + " list"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	out,err = p.communicate()
	list = out.split('\n')
	if len(err) > 1:
		print "Error: %s " % err
		return 0	
	else:
		for i in list:
			print """<p><a href="?qid=%s">%s</a></p>""" % (urllib.quote(i),i)
		return 1

def viewQuestion(qid):
	print "<h1>View Question: </h1>"
	# print "<h2>In view question qid is %s</h2>" % qid
	p = subprocess.Popen([question + ' view "%s"' % qid], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	out,err = p.communicate()
	raw = out.split('\n====\n')
	print out
	if len(err) > 1:
		print "Error: %s " % err
		return 0
	else:
		qTuple = raw[0].split('\n',2)
		del raw[0]
		answerList = []
		for group in raw:
			aTuple = group.split('\n', 2)
			if len(aTuple) == 3:
				answerList.append(Answer(aTuple[0], aTuple[1], aTuple[2]))
		answerList.sort(key=operator.attrgetter('vote'), reverse=True)
		if len(qTuple) == 3:
			print """<p>%s: <b>%s</b></p>
					<form action="" method="GET">%s
					<input type="text" class="hidden" name="aid" value="%s">
					<input type="text" class="hidden" name="qid" value="%s">
					<input type="submit" value="Up" name="up">
					<input type="submit" value="Down" name="down"></form> 
					<hr>
			""" % (qTuple[0], qTuple[2], qTuple[1],urllib.quote(qTuple[0]), urllib.quote(qid))
		for answer in answerList:
			print """<p>%s: %s</p>
				<form action="" method="GET">%s
				<input type="text" class="hidden" name="aid" value="%s">
				<input type="text" class="hidden" name="qid" value="%s">
				<input type="submit" value="Up" name="up">
				<input type="submit" value="Down" name="down"></form> 
				<hr class="dashed">
			""" % (answer.aid, answer.content, answer.vote, urllib.quote(answer.aid), urllib.quote(qid))		
		print """<p><a href='?addAnswer=%s&qid=%s'>Add Answer</a></p>""" % (False, urllib.quote(qid))
		print """<p><a href="jane.cgi"><input type="button" value="Back"></a></p>"""
		return 1

def addAnswers(addAnswer, qid, aContent):
	if addAnswer == "True":
		p = subprocess.Popen([question + ' answer "%s" "%s" "%s"' % (qid, uniqid(), aContent)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		out,err = p.communicate()
		if len(err) > 1:
			print """Sorry something blows up. Please <a href='jane.cgi?qid=%s'>try</a> again.""" % qid
		else:
			viewQuestion(qid)
	else:
		result = viewQuestion(qid)
		print """<h2>Adding your answer: </h2>
				<form action="jane.cgi" method="POST" ><textarea name="aContent" ></textarea>
				<input type="text" name="addAnswer" class="hidden" value="True">
				<input type="text" name="qid" class="hidden" value="%s">
				<input type="submit" value="Answer it!">
				</form>
		""" % urllib.quote(qid)

def createQuestion(addQuestion):
	if "qContent" not in form:
		print """Sorry content cannot be empty. Please <a href="jane.cgi">try</a>  again."""
	else:
		content = urllib.unquote(form['qContent'].value)
		p = subprocess.Popen([question + ' create "%s" "%s"' % (uniqid(), content)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		out,err = p.communicate()
		if len(err) > 1:
			print err
		else:
			listQuestion()

def handleVote(qid, aid, vote):
	if vote == "Up":
		p = subprocess.Popen([question + ' vote up "%s" "%s"' % (qid, "" if qid == aid else aid)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		out,err = p.communicate()
		if len(err) > 1:
			print err
		else:
			viewQuestion(qid)
	elif vote == "Down":
		p = subprocess.Popen([question + ' vote down "%s" "%s"' % (qid, "" if qid == aid else aid)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		out,err = p.communicate()
		if len(err) > 1:
			print err
		else:
			viewQuestion(qid)
	else:
		print """Sorry something blows up. Please <a href='jane.cgi?qid=%s'>try</a> again.""" % qid

# Below is the main method:
# Print header
print 'Content-Type: text/html'
print
htmlBeginning = """
	<html>
	<head>
	<title>OST- HW4 - Chen</title>
	<link rel="stylesheet" type="text/css" href="hw4.css">
	</head>
	<body>
	"""
htmlEnding = """
	</body>
	</html>
	"""

print htmlBeginning
form = cgi.FieldStorage()
if "addAnswer" not in form and "addQuestion" not in form and "qid" not in form and "up" not in form and "down" not in form:
	listQuestion()
elif "addAnswer" in form:
	addAnswer = form['addAnswer'].value
	aContent = ""
	if addAnswer == "True":
		aContent = urllib.unquote(form['aContent'].value)
	if "qid" in form:
		qid = urllib.unquote(form['qid'].value)
	else:
		print "Error: sorry something blows up. Please try again"
	addAnswers(addAnswer, qid, aContent)
elif "addQuestion" in form:
	addQuestion = form['addQuestion'].value
	createQuestion(addQuestion)
elif "up" in form:
	qid = urllib.unquote(form['qid'].value)
	aid = urllib.unquote(form['aid'].value)
	vote = urllib.unquote(form['up'].value)
	handleVote(qid, aid, vote)
elif "down" in form:
	qid = urllib.unquote(form.getvalue("qid"))
	aid = urllib.unquote(form.getvalue("aid"))
	vote = urllib.unquote(form.getvalue("down"))
	handleVote(qid, aid, vote)
elif "qid" in form:
	qid = urllib.unquote(form.getvalue("qid"))
	result = viewQuestion(qid)
	if not result:
		print "Sorry something blows up. Please try again."		
print htmlEnding