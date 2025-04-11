class QueryFormatter:
    """ 
    Takes in clauses from query_AND/OR/NOT_clause
    And builds a full query body, ready to use in tiktok_api class
    """
    def query_builder(self, startdate, enddate, args):
        clause_arr = args

        query_structure = {}
        for clause in clause_arr:
            for key, value in clause.items():
                if key in query_structure:
                    query_structure[key].extend(value)
                else:
                    query_structure[key] = value

        query_body = {
            "query": query_structure,
            "start_date": f"{startdate}",
            "end_date": f"{enddate}",
            "cursor": 0
        }
        return query_body
    
    
    """ 
    Builds a clause with conditions and the correct boolean operation
    """
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
    
    """ 
    Takes in list of tuples (field_name, field_value, operation)
    And sends it to build_clause with correct AND/OR/NOT
    """
    def query_AND_clause(self, conditions):
        return self.build_clause("and", conditions)
    
    #Functions below are the same as above, with respective logical operations
    def query_OR_clause(self, conditions):
        return self.build_clause("or", conditions)
    
    def query_NOT_clause(self, conditions):
        return self.build_clause("not", conditions)
