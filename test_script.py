import os
from dotenv import load_dotenv
from app import configure, generate_sql_query, generate_expected_output, generate_explanation

# Load environment variables
load_dotenv()

# Configure model
model = configure()

# Test queries
test_queries = [
    "Create a table of employee which includes column employee_id, employee_name, and department_id."
]

def main():
    for idx, query in enumerate(test_queries, start=1):
        print(f"Running Test Case {idx}: {query}")
        
        # Generate SQL query
        sql_query = generate_sql_query(model, query)
        
        # Generate expected output and explanation
        expected_output = generate_expected_output(model, sql_query)
        explanation = generate_explanation(model, sql_query)
        
        # Print results
        print("Generated SQL Query:")
        print(sql_query)
        print("")

        print("Expected Output:")
        print(expected_output)
        print("")

        print("Explanation:")
        print(explanation)
        print("")

if __name__ == "__main__":
    main()
