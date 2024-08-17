1: All Elements Present

Note: Used for reference - actual schema for unit testing in tests/schema.json

```
requirements:
  requestType: POST
  queryParams:
    - name: param1
      required: true
      description: The first parameter.
      exampleData: id=12345ABC
    - name: param2
      required: false
      description: The second parameter (optional).
      exampleData: cell=Sheet2!B3
  inputSchema:
    type: object
    required: true
    properties:
      data:
        type: string
        required: true
      details:
        type: object
        required: true
        properties:
          createdAt:
            type: string
            required: true
  inputDescription: Input data and details
  outputSchema:
    type: object
    required: true
    properties:
      id:
        type: string
        required: true
      result:
        type: string
        required: true
  outputDescription: Response with ID and result
```

2: No Query Parameters
```
requirements:
  requestType: POST
  queryParams: []
  inputSchema:
    type: object
    required: true
    properties:
      payload:
        type: array
        items:
          type: integer
        required: true
      metadata:
        type: object
        required: true
        properties:
          requestId:
            type: string
            required: true
  inputDescription: Payload array and metadata
  outputSchema:
    type: object
    required: true
    properties:
      status:
        type: string
        required: true
      data:
        type: object
        required: true
        properties:
          value:
            type: float
            required: true
  outputDescription: Status and result data
```
3: Optional Input Schema
```
requirements:
  requestType: POST
  queryParams:
    - name: param1
      required: true
      description: Unique identifier.
      exampleData: id=ABCD1234
  inputSchema: null
  inputDescription: No input schema required
  outputSchema:
    type: object
    required: true
    properties:
      code:
        type: integer
        required: true
      message:
        type: string
        required: true
      details:
        type: object
        required: false
        properties:
          additionalInfo:
            type: string
  outputDescription: Response code and message
```
Variant 4: Optional Output Schema
```
requirements:
  requestType: POST
  queryParams:
    - name: param1
      required: true
      description: Identifier key.
      exampleData: id=789XYZ
    - name: param2
      required: false
      description: Optional cell reference.
      exampleData: cell=Sheet4!E6
  inputSchema:
    type: object
    required: true
    properties:
      name:
        type: string
        required: true
      attributes:
        type: object
        required: true
        properties:
          age:
            type: integer
            required: true
          height:
            type: float
            required: true
  inputDescription: Name and attributes
  outputSchema: null
  outputDescription: No output schema provided
```
5: Multiple Query Parameters
```
requirements:
  requestType: POST
  queryParams:
    - name: param1
      required: true
      description: The unique request identifier.
      exampleData: id=TEST1234
    - name: param2
      required: true
      description: Reference for the request.
      exampleData: cell=Sheet5!F7
    - name: param3
      required: false
      description: Optional additional parameter.
      exampleData: filter=active
  inputSchema:
    type: object
    required: true
    properties:
      text:
        type: string
        required: true
      details:
        type: object
        required: true
        properties:
          timestamp:
            type: string
            required: true
          user:
            type: object
            properties:
              username:
                type: string
                required: true
              email:
                type: string
                required: true
  inputDescription: Text and user details
  outputSchema:
    type: object
    required: true
    properties:
      result:
        type: string
        required: true
      metadata:
        type: object
        properties:
          processedAt:
            type: string
  outputDescription: Processed result with metadata
```
Variant 6: Nested Input and Output
```
requirements:
  requestType: POST
  queryParams:
    - name: param1
      required: true
      description: Required unique key.
      exampleData: id=OPTIONALKEY
  inputSchema:
    type: object
    required: true
    properties:
      data:
        type: object
        required: true
        properties:
          id:
            type: string
            required: true
          attributes:
            type: object
            required: true
            properties:
              name:
                type: string
              value:
                type: float
  inputDescription: Object with nested attributes
  outputSchema:
    type: object
    required: true
    properties:
      result:
        type: string
        required: true
      details:
        type: object
        properties:
          summary:
            type: string
            required: true
          items:
            type: array
            items:
              type: object
              properties:
                id:
                  type: string
                value:
                  type: float
  outputDescription: Result with nested details
```
7: Simple Schema
```
requirements:
  requestType: POST
  queryParams:
    - name: param1
      required: true
      description: Simple identifier.
      exampleData: id=123
  inputSchema: null
  inputDescription: No input schema required
  outputSchema:
    type: object
    required: true
    properties:
      message:
        type: string
        required: true
  outputDescription: Simple response message
```
8: Array Input with Optional Parameters
```
requirements:
  requestType: POST
  queryParams:
    - name: param1
      required: true
      description: Required identifier.
      exampleData: id=ARRAY123
    - name: param2
      required: false
      description: Optional reference.
      exampleData: cell=Sheet8!I10
  inputSchema:
    type: object
    required: true
    properties:
      items:
        type: array
        items:
          type: string
        required: true
  inputDescription: Array of items
  outputSchema:
    type: object
    required: true
    properties:
      count:
        type: integer
        required: true
      total:
        type: float
  outputDescription: Count and total values
```
9: Minimal Schema with Required Query Params
```
requirements:
  requestType: POST
  queryParams:
    - name: param1
      required: true
      description: Essential key.
      exampleData: id=KEY456
    - name: param2
      required: true
      description: Essential cell reference.
      exampleData: cell=Sheet9!J11
  inputSchema: null
  inputDescription: No input schema required
  outputSchema: null
  outputDescription: No output schema provided
```
10: Detailed Input with Optional Output
```
requirements:
  requestType: POST
  queryParams:
    - name: param1
      required: true
      description: Unique identifier.
      exampleData: id=UNIQUE567
    - name: param2
      required: true
      description: Data location reference.
      exampleData: cell=Sheet10!K12
  inputSchema:
    type: object
    required: true
    properties:
      header:
        type: string
        required: true
      body:
        type: array
        items:
          type: object
          properties:
            key:
              type: string
            value:
              type: float
  inputDescription: Header and array of key-value pairs
  outputSchema: null
  outputDescription: No output schema provided
 ```