This Python tool allows users to import a CSV dataset, specify functional dependencies and a primary key, and analyze the dataset for 1NF, 2NF, 3NF, and BCNF compliance. 
It performs BCNF decomposition and generates an SQL script to create normalized tables and populate them with the original data. 
It also includes an interactive SQL interface using SQLite.

# installation instructions
1. Download/Clone repository & Install pandas
   - git clone https://github.com/siiimra/proj1.git
   - cd proj1
   - pip install pandas
3. Add desired .csv files to the project folder or use enrollment.csv to test

# usage instructions
1. Run the program (python proj1.py)
2. Enter the CSV file path (.csv file name)
3. Provide functional dependencies (e.g. A,B->C;D->E)
4. Provide the primary key(s) (e.g. A,B)
5. Write queries as desired
[CMPS664_Project#1.pdf](https://github.com/user-attachments/files/19677097/CMPS664_Project.1.pdf)
