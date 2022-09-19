import streamlit as st
from datetime import datetime
import data

class Course:
    def __init__(self,title):
        self.title = title
        self.assignments = []
        st.session_state['courses'].append(self)
    def refresh_assignments(self):
        for a in st.session_state['assignments']:
            if a.coursetitle == self.title and a not in self.assignments:
                self.assignments.append(a)
            

class Assignment:
    def __init__(self, course, title, due_date):
        self.course = course
        self.coursetitle = course.title
        self.title = title
        self.due_date = due_date
        st.session_state['assignments'].append(self)
    def link_course(self):
        # For use after loading from file
        for c in st.session_state['courses']:
            if c.title == self.coursetitle:
                self.course = c
    def edit_dialog(self):
        form = st.form('edit_asgn_form')
        form.subheader(f'Edit Assignment: {self.title}')
        form.form_submit_button(
            'Delete',on_click=self.suicide
        )
        title = form.text_input(
            'Description',key='etitle',
            value=self.title
        )
        due_date = form.date_input(
            'Due Date',key='edue_date'
        )
        form.form_submit_button(
            on_click=self.apply_edit
        )
    def apply_edit(self):
        self.title = st.session_state['etitle']
        self.due_date = st.session_state['edue_date']
        save()
    def suicide(self):
        self.course.assignments.remove(self)
        st.session_state['assignments'].remove(self)
        del self
    def due_date_string(self):
        return self.due_date.strftime('%B %d')

def selbox_format(x):
    return x.title

def register_asgn():
    Assignment(
        st.session_state['fcourse'],
        st.session_state['ftitle'],
        st.session_state['fdue_date']
    )
    save()


def get_asgn_max():
    return max([
        len(c.assignments) for c in courses
    ])

def save():
    assignments = st.session_state['assignments']
    data.save(assignments,courses)

if 'courses' not in st.session_state:
    st.session_state['courses'] = data.courses
courses = st.session_state['courses']
if not courses:
    Course('CAS-111')
    Course('COMM-202')
    Course('ENGL-110')
    Course('IT-105')

if 'assignments' not in st.session_state:
    st.session_state['assignments'] = data.assignments

weeknumber = datetime.now().isocalendar()[1] - 32
st.header(f"It's Week {weeknumber}")

if st.button('+'):
    form = st.form('asgn_form')
    fcourse = form.selectbox(
        'Course',
        courses,key='fcourse',
        format_func=selbox_format
    )
    ftitle = form.text_input('Description',key='ftitle')
    fdue_date = form.date_input('Due Date',key='fdue_date')
    form.form_submit_button(
        on_click=register_asgn
    )

if st.button('Clear'):
    st.session_state.clear()
    st.experimental_rerun()

for c in st.session_state['courses']:
    c.refresh_assignments()
#    st.subheader(c.title)
#    for assignment in c.assignments:
#        st.write(assignment.title)
#        st.caption(assignment.due_date)

headercolumns = st.columns(len(courses),gap='large')
for i,column in enumerate(headercolumns):
    column.header(courses[i].title)

for x in range(get_asgn_max()):
    thisrow = st.columns(
        len(courses),gap='large'
    )
    for i,column in enumerate(thisrow):
        if len(
            courses[i].assignments
        )-1 >= x:
            asgn = courses[i].assignments[x]
            column.button(
                asgn.title,
                key=f'button{x}-{i}',
                on_click=asgn.edit_dialog
            )
            column.caption(asgn.due_date_string())
    

