from SakaiPy import RequestGenerator
from SakaiPy.SakaiTools import Assignment

authInfo={}
authInfo['baseURL']="https://sakai.rutgers.edu"

authInfo['loginFormId']='fm1'
authInfo['usernameField']='username'
authInfo['passwordField']='password'

authInfo['loginURL']="https://cas.rutgers.edu/login?service=https%3A%2F%2Fsakai.rutgers.edu%2Fsakai-login-tool%2Fcontainer"
authInfo['username']= ""
authInfo['password']= ""

rq = RequestGenerator.RequestGenerator(authInfo)

cs213 = "e4ee535b-99b1-41fc-922a-0f89d4f436a6"
assigns = Assignment.Assignment(rq).getAllAssignmentsForSite(cs213)
col = assigns['assignment_collection']
for i in col:
	print 'Due: ' + i['dueTimeString']
	print i['instructions'].replace("<p>", "").replace("</p>","").replace("<br />","") + "\n"