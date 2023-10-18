from pymongo import MongoClient

# Connect to your MongoDB database
client = MongoClient('localhost', 27017)  # Replace with your MongoDB server details
db = client['Python_developer']  # Replace with your database name
collection = db['job_listings']

# Calculate the average salary for Python developers in your city
city = 'faridabad'  # Replace with your city
cursor = collection.find({"location": city, "salary": {"$ne": None}})
salaries = [listing['salary'] for listing in cursor]
total_salaries = [float(salary.replace('$', '').replace(',', '')) for salary in salaries]
avg_salary = sum(total_salaries) / len(total_salaries)

# Print or store the average salary
print(f'Average salary for Python developers in {city}: ${avg_salary:.2f}')

# Close the MongoDB connection
client.close()
