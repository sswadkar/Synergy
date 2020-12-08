from requests_cache import CachedSession
from requests_cache.backends import BaseCache
from bs4 import BeautifulSoup
from studentvue.StudentVueParser import StudentVueParser
import studentvue.helpers as helpers
import typing
URLS = {
        'LOGIN': 'https://md-mcps-psv.edupoint.com/PXP2_Login_Student.aspx?regenerateSessionId=True',
        'HOME': 'https://md-mcps-psv.edupoint.com/Home_PXP2.aspx',
        'SCHEDULE': 'https://md-mcps-psv.edupoint.com/PXP2_ClassSchedule.aspx?AGU=0',
        'CALENDAR': 'https://md-mcps-psv.edupoint.com/PXP2_Calendar.aspx?AGU=0',
        'STUDENT_INFO': 'https://md-mcps-psv.edupoint.com/PXP2_MyAccount.aspx?AGU=0',
        'SCHOOL_INFO': 'https://md-mcps-psv.edupoint.com/PXP2_SchoolInformation.aspx?AGU=0',
        'COURSE_HISTORY': 'https://md-mcps-psv.edupoint.com/PXP2_CourseHistory.aspx?AGU=0',
        'GRADE_BOOK': 'https://md-mcps-psv.edupoint.com/PXP2_Gradebook.aspx?AGU=0&studentGU=',
        'DATA_GRID': 'https://md-mcps-psv.edupoint.com/service/PXP2Communication.asmx/DXDataGridRequest',
        'LOAD_CONTROL': 'https://md-mcps-psv.edupoint.com/service/PXP2Communication.asmx/LoadControl',
        'GRADE_BOOK_FOCUS_INFO': 'https://md-mcps-psv.edupoint.com/service/PXP2Communication.asmx/GradebookFocusClassInfo',
        'OPEN': 'https://md-mcps-psv.edupoint.com/PXP2_ClassSchedule.aspx'
    }
class StudentVue():
    def __init__(self, username, password, studentgu, parser: typing.Type[StudentVueParser] = StudentVueParser, cache_backend: typing.Union[BaseCache, str] = 'memory'):
        self.username = username
        self.password = password
        self.studentgu = studentgu
        URLS['GRADE_BOOK'] += studentgu
        self.parser = parser
        self.session = CachedSession(
            cache_name=username,
            backend=cache_backend,
            expire_after=15 * 60,
            allowable_methods=('GET', 'POST')
        )
        self.session.cache.clear()
        login_page = BeautifulSoup(self.session.get(URLS['LOGIN']).text, 'html.parser')
        login_form_data = helpers.parse_form(login_page.find(id='aspnetForm'))
        login_form_data['ctl00$MainContent$username'] = username
        login_form_data['ctl00$MainContent$password'] = password
        resp = self.session.post(URLS['LOGIN'], data=login_form_data)
        if "Invalid user id or password" in resp.text:
            raise ValueError('Incorrect Username or Password')

    def get_grades(self):
        grades = self.session.post(URLS['GRADE_BOOK'])
        soup = BeautifulSoup(grades.text,features="lxml")
        soup.prettify()
        student_grades = []
        for x in soup.findAll("span", {"class":"score"}):
            x = str(x)
            student_grades.append(x[x.index(">")+1:x.index("%")+1])
        return student_grades

    def get_classes(self):
        grades = self.session.post(URLS['GRADE_BOOK'])
        soup = BeautifulSoup(grades.text, features="lxml")
        soup.prettify()
        student_classes = []
        actual_classes = []
        for x in soup.findAll("button", {"type": "button"}):
            x = str(x)
            student_classes.append(x[x.index(">") + 1:x.index("</button>")])
        for x in range(len(student_classes)):
            try:
                if int(student_classes[x][0]) > 0:
                    actual_classes.append(student_classes[x][3:])
            except Exception as e:
                continue
        return actual_classes
    def get_missing_assignments(self):
        grades = self.session.post(URLS['GRADE_BOOK'])
        soup = BeautifulSoup(grades.text, features="lxml")
        soup.prettify()
        missing_assigments = []
        for x in soup.findAll("td", {"class": "class-item-lessemphasis hide-for-print"}):
            x = str(x)
            missing_assigments.append(x[x.index("<div>") + 5:x.index("</div>")])
        return missing_assigments



