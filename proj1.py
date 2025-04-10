# Simra Ahmed
# CMPS664 Project 1
# This script reads in a dataset, checks normal forms, and performs BCNF decomposition.
# It generates SQL scripts and creates a SQLite DB with an interactive shell.

import pandas as pd
import sqlite3


# Step 1: CSV Import
def import_csv():
    path = input("Enter CSV file path: ")
    try:
        df = pd.read_csv(path)
        print("\nCSV Loaded")
        print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
        print("\nSample Records:\n", df.head())
        print("\nAttribute Data Types:\n", df.dtypes)
        return df
    except Exception as e:
        print("Error loading file:", e)
        return None

# Step 2: FD and Primary Key Input
def input_fd():
    fds_raw = input("Enter functional dependencies (e.g. A,B->C;D->E): ")
    pk_raw = input("Enter primary key(s), comma separated: ")

    fd_list = []
    for fd in fds_raw.split(";"):
        if "->" in fd:
            lhs, rhs = fd.strip().split("->")
            fd_list.append((lhs.strip(), rhs.strip()))

    primary_key = [attr.strip() for attr in pk_raw.split(",")]

    print("\nFunctional Dependencies:")
    for lhs, rhs in fd_list:
        print(f"{lhs} -> {rhs}")

    print("\nPrimary Key(s):", primary_key)
    return fd_list, primary_key

# Closure of attributes
def closure(attributes, fds):
    closure_set = set(attributes)
    changed = True
    while changed:
        changed = False
        for lhs, rhs in fds:
            lhs_set = set(lhs.strip().split(","))
            rhs_set = set(rhs.strip().split(","))
            if lhs_set.issubset(closure_set) and not rhs_set.issubset(closure_set):
                closure_set.update(rhs_set)
                changed = True
    return closure_set

# Step 3: Normalization Process
# 1NF Check
def check_1nf(df):
    for _, row in df.iterrows():
        for val in row:
            if isinstance(val, list) or isinstance(val, set):
                return False
    return True

# 2NF Check
def check_2nf(fds, primary_keys):
    partial_dependencies = []
    pk_set = set(primary_keys)
    for lhs, rhs in fds:
        lhs_set = set(lhs.strip().split(","))
        rhs_set = set(rhs.strip().split(","))
        if lhs_set.issubset(pk_set) and not lhs_set == pk_set:
            partial_dependencies.append((lhs, rhs))
    return partial_dependencies

# 3NF Check
def check_3nf(fds, primary_keys):
    transitive_dependencies = []
    pk_set = set(primary_keys)
    for lhs, rhs in fds:
        lhs_set = set(lhs.strip().split(","))
        if not lhs_set.issubset(pk_set):
            transitive_dependencies.append((lhs, rhs))
    return transitive_dependencies

def check_bcnf(fds, all_attributes):
    violations = []
    for lhs, rhs in fds:
        lhs_attrs = lhs.strip().split(",")
        closure_set = closure(lhs_attrs, fds)
        if set(closure_set) == set(all_attributes):
            continue  # lhs is a candidate key
        else:
            violations.append((lhs, rhs))
    return violations

def is_candidate_key(attrs, fds, all_attrs):
    return set(closure(attrs, fds)) == set(all_attrs)

def decompose_bcnf(relation_attrs, fds):
    decomposed_relations = []

    def relevant_fds(attrs, fds):
        return [
            (lhs, rhs) for lhs, rhs in fds
            if set(lhs.strip().split(",")).issubset(set(attrs))
        ]

    def already_decomposed(attrs):
        return any(set(attrs) == set(existing) for existing in decomposed_relations)

    def bcnf_decompose(attrs):
        current_fds = relevant_fds(attrs, fds)
        for lhs, rhs in current_fds:
            lhs_set = lhs.strip().split(",")
            rhs_set = rhs.strip().split(",")
            if not is_candidate_key(lhs_set, current_fds, attrs):
                left_attrs = set(lhs_set + rhs_set)
                remaining_attrs = set(attrs) - set(rhs_set)
                if left_attrs == set(attrs) or already_decomposed(left_attrs):
                    continue  # Skip if it's the same or already done
                bcnf_decompose(list(left_attrs))
                bcnf_decompose(list(remaining_attrs))
                return
        if not already_decomposed(attrs):
            decomposed_relations.append(attrs)

    bcnf_decompose(relation_attrs)
    return decomposed_relations

def generate_sql(relations, df, output_file="normalized_output.sql"):
    sql_statements = []

    for i, attrs in enumerate(relations, start=1):
        table_name = f"Relation_{i}"
        columns_sql = []
        for attr in attrs:
            dtype = df[attr].dtype
            if pd.api.types.is_integer_dtype(dtype):
                col_type = "INT"
            elif pd.api.types.is_float_dtype(dtype):
                col_type = "FLOAT"
            else:
                col_type = "VARCHAR(255)"
            columns_sql.append(f"{attr} {col_type}")
        
        create_stmt = f"CREATE TABLE IF NOT EXISTS {table_name} (\n  " + ",\n  ".join(columns_sql) + "\n);"
        sql_statements.append(create_stmt)

        sub_df = df[attrs].drop_duplicates()
        for _, row in sub_df.iterrows():
            values = []
            for val in row:
                if pd.isna(val):
                    values.append("NULL")
                elif isinstance(val, str):
                    values.append("'" + str(val).replace("'", "''") + "'")
                else:
                    values.append(str(val))
            columns_str = ", ".join(attrs)
            insert_stmt = f"INSERT INTO {table_name} ({columns_str}) VALUES (" + ", ".join(values) + ");"
            sql_statements.append(insert_stmt)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n\n".join(sql_statements))

    print(f"\nSQL script saved as '{output_file}'.")

# Step 5: Create DB and Interactive SQL Interface
def db_setup(sql_file, db_name="normalized.db"):
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        with open(sql_file, "r", encoding="utf-8") as f:
            sql_script = f.read()

        cursor.executescript(sql_script)
        conn.commit()
        print(f"\nDatabase '{db_name}' created and populated.")
        return conn
    except Exception as e:
        print("Error setting up database:", e)
        return None

def interface(conn):
    cursor = conn.cursor()
    print("\nInteractive SQL Console")
    print("Type 'exit' to quit.\n")
    
    while True:
        query = input("SQL> ")
        if query.strip().lower() == "exit":
            break
        try:
            cursor.execute(query)
            if query.strip().lower().startswith("select"):
                rows = cursor.fetchall()
                for row in rows:
                    print(row)
            else:
                conn.commit()
                print("Query executed.")
        except Exception as e:
            print("Error:", e)

# Main Execution
def main():
    df = import_csv()
    if df is None:
        print("Step 1 Failed.")
        return
    print("\nStep 1 Complete.")

    fds, primary_key = input_fd()
    closure_set = closure(primary_key, fds)
    print("Closure:", closure_set)

    print("\nChecking 1NF:")
    if check_1nf(df):
        print("1NF satisfied: No multi-valued attributes found.")
    else:
        print("1NF violated: Multi-valued attributes present.")

    print("\nChecking 2NF:")
    partial_deps = check_2nf(fds, primary_key)
    if partial_deps:
        print("2NF violated. Partial Dependencies found:")
        for lhs, rhs in partial_deps:
            print(f"{lhs} -> {rhs}")
    else:
        print("2NF satisfied: No partial dependencies.")

    print("\nChecking 3NF:")
    trans_deps = check_3nf(fds, primary_key)
    if trans_deps:
        print("3NF violated. Transitive Dependencies found:")
        for lhs, rhs in trans_deps:
            print(f"{lhs} -> {rhs}")
    else:
        print("3NF satisfied: No transitive dependencies.")
    
    print("\nChecking BCNF:")
    bcnf_violations = check_bcnf(fds, df.columns.tolist())
    if bcnf_violations:
        print("BCNF violated. The following FDs do not have a candidate key:")
        for lhs, rhs in bcnf_violations:
            print(f"{lhs} -> {rhs}")
        
    else:
        print("BCNF satisfied: All determinants are candidate keys.")
    
    print("\nBCNF Decomposition:")
    relations = decompose_bcnf(df.columns.tolist(), fds)
    for i, rel in enumerate(relations, 1):
        print(f"Relation {i}: {rel}")

    # Step 4: Generate sql script
    print("\nGenerating SQL Scripts...")
    generate_sql(relations, df)

    # Step 5: Create Database and Run Interactive Console
    conn = db_setup("normalized_output.sql")
    if conn:
        interface(conn)
        conn.close()



if __name__ == "__main__":
    main() 
