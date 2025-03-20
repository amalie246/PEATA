#Handle query body formatting so user can easily pick filterings for which data
#Also coordinate video retrieval with user and comment informations retrieval!

#get_public_user info only needs to be called once
#get_video_comments needs to be called once per video retrieved! 
#This may cause problems to the API

class QueryFormatter:
    
    #This data should be retrieved from the GUI (or some service between)
    #UNTESTED SO FAR
    def build_query(self, bool_operation, value_field_operation_tuple):
        #Takes in boolean logic operations: AND, OR, NOT for now
        #TODO : make more dynamic, per now the logic operations is limited to 1 operation per query body
        #It is allowed to combine AND/OR/NOT operations in different clauses
        
        clause_arr = []
        #Takes in field_values[0], field_name[1] and operation[2]
        #The value_field_operation_tuple is an array of tupples(3)
        for i in range(len(value_field_operation_tuple)):
            #Build a clause in the query body
            clause = {
                "operation" : [f"{value_field_operation_tuple[i][2]}"],
                "field_name" : [f"{value_field_operation_tuple[i][1]}"],
                "field_values" : [f"{value_field_operation_tuple[i][0]}"]
                }
            clause_arr.extend(clause)
        
        #Create the entire query body
        query_body = {
                "query" : {
                    f"{bool_operation}" : clause_arr
                    }
            }
        return query_body
    
    #Takes in query clauses, dates, and builds the final query body
    def query_builder(self, startdate, enddate, *args):
        clause_arr = []
        
        for q in args:
            clause_arr.append(q)
            
        query_body = {
            "query": clause_arr[0] if len(clause_arr) == 1 else {"and": clause_arr},
            "start_date" : f"{startdate}",
            "end_date" : f"{enddate}"
            }
        print(query_body)
        return query_body
    
    #Takes in list of tuples(field_name, field_value, operation)
    #Returns a clause with AND operation
    def query_AND_clause(self, conditions):
        query_clauses = []
        
        for i in range(len(conditions)):
            if len(conditions[i]) != 3:
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
            "and": query_clauses
        }
        return query
    
    #Functions below are the same as above, with respective logical operations
    def query_OR_clause(self, logic_operation="OR", **kwargs):
        return []
    
    def query_NOT_clause(self, logic_operation="NOT", **kwargs):
        return []
