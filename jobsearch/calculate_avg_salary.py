from pymongo import MongoClient

# Connect to your MongoDB database
client = MongoClient('localhost', 27017) 
db = client['Python_developer']  
collection = db['job_listings']

city = input("Enter the city: ")

# Calculate the average salary for Python developers in the entered city
cursor = collection.find({"location": city, "salary": {"$ne": None}})
salaries = [listing['salary'] for listing in cursor]
if salaries:
    total_salaries = [float(salary.replace('$', '').replace(',', '')) for salary in salaries]
    avg_salary = sum(total_salaries) / len(total_salaries)
    print(f'Average salary for Python developers in {city}: ${avg_salary:.2f}')
else:
    print(f'No salary data available for Python developers in {city}.')

# Close the MongoDB connection
client.close()
