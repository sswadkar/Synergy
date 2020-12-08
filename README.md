# Synergy
Python Script to send emails to MCPS Students about what their grades in their classes

## Modules
* Uses [StudentVue](https://github.com/StudentVue/StudentVue.py) for logging in
  * requests_cache for maintaing cache data
* Beautiful Soup to read data off of Synergy

## Creating student object
  ```python
  sv = StudentVue('<INSERT_STUDENT_ID>','<INSERT_STUDENT_PASS>','<INSERT_GU>')
  ```
  
  `<INSERT_GU>` can be found on StudentVue link when going to the Grade Book tab
  
  `https://md-mcps-psv.edupoint.com/PXP2_Gradebook.aspx?AGU=0&studentGU=<THIS_IS_YOUR_GU>`
  
  `sv.get_classes()` returns a list
  
  `sv.get_grades()` returns a list
  
  `sv.get_missing_assignments()` returns a list

## SMTP
  Uses an SMTP connection in order to send an email. Username and password for email sender are required.
