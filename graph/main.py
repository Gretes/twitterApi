import pyley

# Create cayley client
client = pyley.CayleyClient() # this creates client with default parameters `http://localhost:64210/api/v1/query/gizmo`
#or  specify `url` and `version` parameters
client = pyley.CayleyClient("http://localhost:64210", "v1")

g = pyley.GraphObject()

# Query all vertices in the graph, limit to the first 5 vertices found.


# Start with only one vertex, the literal name "Humphrey Bogart", and retrieve all of them.
# query = g.Vertex('character:finn').Out('action:loves').All()
# response = client.Send(query)
# response.result contains JSON data and response.r contains raw response
# print(response.result)

# query = g.Emit({'type': 'human', 'name': 'finn'})
# response = client.Send(query)
# print(response.result)

# client.AddQuad('character:finn', 'type', 'human', '.')
# client.AddQuad('character:finn', 'name', 'Finn')
client.AddQuad('fuad', '<follows>', 'veli')
client.AddQuad('veli', '<follows>', 'fuad')