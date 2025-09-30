# 1 Initialize System
flask init

# 2. Create Entities Manually (or use CSV)
Create a student
flask student create_student S100 "Alice Green" alice@example.com "Engineering major"

# 3. Create an employer
flask employer create_employer E100 "InnovateCo" "hr@innovateco.com"

# 4. Create a staff member
flask staff create_staff ST100 "Dr. Johnson" johnson@university.edu "Director"

# 4. Create Position
flask employer create_position E100 "Data Analyst Intern" "Analyze data and create reports"

# 5. Student Applies
First, list positions to get the position_id
flask position list

# 6. Then apply using the position_id
flask application apply S100 POSITION_ID

# 7.Staff Creates Shortlist
Create shortlist
flask staff create_shortlist ST100 "Top candidates for Data Analyst role"

# 8. Add student to shortlist (use the shortlist_id from previous command)
flask staff add_to_shortlist ST100 S100 SHORTLIST_ID

# 9. Student Views Shortlist
flask student view_shortlists S100

# 10. Employer Reviews Application
 First, list applications to get application_id
flask application list

# 11. Accept the student
flask employer accept_student APPLICATION_ID "Great profile! Welcome aboard."

# 12. Student Views Response
flask student view_responses S100