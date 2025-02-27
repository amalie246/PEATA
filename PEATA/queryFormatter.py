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
    
    def build_query_handling_multiple_bool_operations(self):
        #Needs to take in a operation for multiple clauses
        #And it should also be able to take in multiple such operations!
        clause_arr = []
        query_body = []
        
        return query_body


