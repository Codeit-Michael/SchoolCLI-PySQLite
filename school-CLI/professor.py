import sqlite3
import json
from person import Person


cnt = sqlite3.connect('school.db')
cursr = cnt.cursor()

class Professor(Person):

	def create_professor(self,firstname,lastname,sex,birthdate,age,phone,address,salary=0.0):
		super().create_person(firstname,lastname,sex,birthdate,age,phone,address)
		self.salary = salary
		self.teaching = []

		cursr.execute("INSERT INTO professors VALUES (?,?,?,?,?,?,?,?,?,?)",(
			self.firstname,
			self.lastname,
			self.fullname,
			self.sex,
			self.birthdate,
			self.age,
			self.phone,
			self.address,
			self.salary,
			json.dumps(self.teaching)
		))
		cnt.commit()
		cnt.close()


	def fetch_professor_subjects(self,professor):
		professor_subjects = cursr.execute("SELECT teaching FROM professors WHERE fullname = ?",(professor,))
		professor_subjects = professor_subjects.fetchone()
		teaching = json.loads(professor_subjects[0])
		return teaching


	def check_subject_existance(self,subject,teaching_list):
		subject_prof = cursr.execute("SELECT professor FROM subjects WHERE name = ?",(subject,)).fetchone()[0]
		if subject_prof != None:
			return print(f'{Subject} has professor already assigned')
		if subject in teaching_list:
			return print('Professor has the subject already')


	def add_subject(self,professor,subject):
		self.teaching = self.fetch_professor_subjects(professor)
		self.check_subject_existance(subject,self.teaching)
		self.teaching.append(subject)
		cursr.execute("UPDATE professors SET teaching = ? WHERE fullname = ?",(json.dumps(self.teaching),professor))
		cursr.execute("UPDATE subjects SET professor = ? WHERE name = ?",(professor,subject))
		cnt.commit()
		cnt.close()
		return print(f'Added {subject} into {professor}\'s teachings')


	def get_teaching_salary(self,professor):
		subjects = cursr.execute("SELECT teaching FROM professors WHERE fullname = ?",(professor,))
		subjects = subjects.fetchone()
		subject_list = json.loads(subjects[0])
		salary = 5000 * len(subject_list)
		return salary


	def view_professors(self):
		professor_table = cursr.execute("SELECT * FROM professors")
		professor_table = professor_table.fetchall()
		cnt.close()
		return print(professor_table)


if __name__ == "__main__":
	pass
	# hello = Professor().create_professor('Kel','Mar','male','09/14/03',18,'09162667676','Maymangga,Cavite',0.0)
	# print(hello)	
	# Professor().add_professor_subject('Michael Maranan','Art Appreciation')
