import json
import requests
import re
from operator import itemgetter

# -- Globals --

SUBJECT_URL = "https://sis.rutgers.edu/soc/subjects.json?semester=12015&campus=NB&level=U"
COURSES_URL = "http://sis.rutgers.edu/soc/courses.json?subject=%(subject_code)s&semester=12015&campus=NB&level=U"
COURSES_FALL_URL = "http://sis.rutgers.edu/soc/courses.json?subject=%(subject_code)s&semester=92014&campus=NB&level=U"
# -- Classes --

class Subject(object):
	def __init__(self, code, name):
		super(Subject, self).__init__()
		self.code = code
		self.name = name
	def setCourses(self, courses):
		self.courses = courses

class Course(object):
	def __init__(self, name, code, credits, prereqs, semester):
		super(Course, self).__init__()
		self.name = name
		self.code = code
		self.credits = credits
		self.semester = semester
		self.prereqs = prereqs 
	def __getitem__(self, key):
		return self.code

# -- API Requests --

def getSubjectData():
	r = requests.get(SUBJECT_URL)
	if r.status_code == 200:
		try:
			return json.loads(r.text)
		except Exception, e:
			print e
	return None

def getCourseData(subject, url):
	r = requests.get(url % {'subject_code': subject})
	if r.status_code == 200:
		try:
			return json.loads(r.text)
		except Exception, e:
			print e
	return None

# -- Parsing JSON --

def parseSubjects(subjectData, user_subject):
	subject_list = []
	for entry in subjectData:
		s = Subject(entry['code'], entry['description'])
		if entry['description'] == user_subject:
			subject_list.append(s)
	return subject_list

def search(data, storage):
	for i in storage:
		if data['title'] == i.name:
			return True
	return False

def parseCourses(courseData, courseData2):
	course_list = []
	for entry in courseData:
		prereqs = parsePrereqs(entry['preReqNotes'])
		c = Course(entry['title'], entry['courseNumber'], entry['credits'], prereqs, "Fall")
		course_list.append(c)
	for entry in courseData2:
		if not search(entry, course_list):
			prereqs = parsePrereqs(entry['preReqNotes'])
			c = Course(entry['title'], entry['courseNumber'], entry['credits'], prereqs, "Spring")
			course_list.append(c)
		else:
			for i in course_list:
				if i.name == entry['title']:
					i.semester = "Fall & Spring"
	course_list = sorted(course_list, key=itemgetter('name'))
	return course_list

def parsePrereqs(prereqStr):
	if prereqStr == None or prereqStr == 'null':
		return "-"
	if (prereqStr.find('Any Course EQUAL or GREATER Than: ') >= 0):
		prereqStr = prereqStr.replace('Any Course EQUAL or GREATER Than: ', '')
	prereqlist = []
	tokenizedPrereq = prereqStr.split("<em> OR </em>")
	for token in tokenizedPrereq:
		token = token.strip()
		prereqlist.append(token)
	return ",".join(prereqlist)

# -- Main -- 

def downloadSubjectsAndParse(user_subject):
	subjectData = getSubjectData()
	subject_list = parseSubjects(subjectData, user_subject)
	springData = getCourseData(subject_list[0].code, COURSES_URL)
	fallData = getCourseData(subject_list[0].code, COURSES_FALL_URL)
	subject_list[0].setCourses(parseCourses(fallData, springData))
	return subject_list

if __name__ == '__main__':
	user_major = raw_input("What is your Major?")
	sl = downloadSubjectsAndParse(user_major.upper())
	output = open('./temp.txt', 'w')
	output.write( sl[0].name + "\n\n")
	for c in sl[0].courses:
		output.write("%s:%s\t%s\n" % (sl[0].code, c.code, c.name))
		output.write("%s\t%s\t%s\n\n" % (c.prereqs, c.credits, c.semester))
	output.close()

