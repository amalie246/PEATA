class QueryFormatter:
    
    #This data should be retrieved from the GUI (or some service between)
    #UNTESTED SO FAR
    
    #Takes in query clauses, dates, and builds the final query body
    def query_builder(self, startdate, enddate, *args):
        clause_arr = list(args)

        query_structure = {}
        for clause in clause_arr:
            print("Clause: ")
            print(clause)
            print()
            for key, value in clause.items():
                if key in query_structure:
                    query_structure[key].extend(value)
                else:
                    query_structure[key] = value

        query_body = {
            "query": query_structure,
            "start_date": f"{startdate}",
            "end_date": f"{enddate}"
        }
        print(query_body)
        return query_body
    
    def build_clause(self, logic_op, conditions):
        if logic_op not in ["and", "or", "not"]:
            raise ValueError("Needs logic operations: AND/OR/NOT")
        
        query_clauses = []
        for i in range(len(conditions)):
            if(len(conditions[i])) != 3:
                raise ValueError("Invalid condition format")
            
            condition = conditions[i]
            field = condition[0]
            value = condition[1]
            operation = condition[2]
            
            clause = {
                "operation": f"{operation}",
                "field_name": f"{field}",
                "field_values": [f"{value}"]
                }
            query_clauses.append(clause)
        query = {
            f"{logic_op}": query_clauses
            }
        return query
    
    #Takes in list of tuples(field_name, field_value, operation)
    #Returns a clause with AND operation
    def query_AND_clause(self, conditions):
        return self.build_clause("and", conditions)
    
    #Functions below are the same as above, with respective logical operations
    def query_OR_clause(self, conditions):
        return self.build_clause("or", conditions)
    
    def query_NOT_clause(self, conditions):
        return self.build_clause("not", conditions)
