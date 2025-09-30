# Complete Workflow Example
1. Initialize System
flask init
2. Create Entities Manually (or use CSV)
Create a student
flask student create_student S100 "Alice Green" alice@example.com "Engineering major"

# Create an employer
flask employer create_employer E100 "InnovateCo" "hr@innovateco.com"

# Create a staff member
flask staff create_staff ST100 "Dr. Johnson" johnson@university.edu "Director"
3. Create Position
bashflask employer create_position E100 "Data Analyst Intern" "Analyze data and create reports"
4. Student Applies
bash# First, list positions to get the position_id
flask position list

# Then apply using the position_id
flask application apply S100 POSITION_ID
5. Staff Creates Shortlist
bash# Create shortlist
flask staff create_shortlist ST100 "Top candidates for Data Analyst role"

# Add student to shortlist (use the shortlist_id from previous command)
flask staff add_to_shortlist ST100 S100 SHORTLIST_ID
6. Student Views Shortlist
bashflask student view_shortlists S100
7. Employer Reviews Application
bash# First, list applications to get application_id
flask application list

# Accept the student
flask employer accept_student APPLICATION_ID "Great profile! Welcome aboard."
8. Student Views Response
bashflask student view_responses S100