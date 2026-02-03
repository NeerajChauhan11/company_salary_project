import random
from faker import Faker
import psycopg2
from db_config import DB_CONFIG

fake = Faker()

# Master data
companies = ["TCS", "Infosys", "Wipro", "Accenture", "Google", "Amazon", "Microsoft"]
departments = ["IT", "HR", "Finance"]
roles = [
    "Data Analyst",
    "AI Engineer",
    "Software Developer",
    "ML Engineer",
    "Business Analyst",
    "Cloud Engineer",
    "HR Manager",
    "Financial Analyst",
]

locations = ["Delhi", "Bangalore", "Hyderabad", "Mumbai", "Pune", "Chennai", "Noida"]


# Salary pattern based on experience
def salary_by_experience(exp):
    if exp <= 1:
        return random.uniform(2, 4)
    elif exp <= 3:
        return random.uniform(4, 7)
    elif exp <= 5:
        return random.uniform(7, 12)
    elif exp <= 8:
        return random.uniform(12, 20)
    else:
        return random.uniform(18, 30)


# Boost logic (realistic patterns)
def apply_boost(company, rating, salary):

    # Big tech pays more
    if company in ["Google", "Amazon", "Microsoft"]:
        salary *= 1.3

    # Performance impact
    if rating == 5:
        salary *= 1.2
    elif rating == 4:
        salary *= 1.1

    return round(salary, 2)


# PostgreSQL connection
conn = psycopg2.connect(**DB_CONFIG)
cursor = conn.cursor()


ROWS_TO_GENERATE = 100  # you can change to 150 or 200

for _ in range(ROWS_TO_GENERATE):

    name = fake.name()
    company = random.choice(companies)
    department = random.choice(departments)
    role = random.choice(roles)

    experience = random.randint(0, 12)
    location = random.choice(locations)
    rating = random.randint(1, 5)

    base_salary = salary_by_experience(experience)
    final_salary = apply_boost(company, rating, base_salary)

    cursor.execute(
        """
        INSERT INTO company_salary_data
        (employee_name, company_name, department, role,
        experience_years, location, ctc, performance_rating)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """,
        (name, company, department, role, experience, location, final_salary, rating),
    )

conn.commit()
cursor.close()
conn.close()

print("✅ Realistic dummy salary data inserted successfully!")
