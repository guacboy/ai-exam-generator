# Group 15 Microservices
## ID Generator Microservice

### Installation

Install the required dependencies: pip install -r requirements.txt


### How to send a request

Write the ID generation command in the `request.txt` file. The command must be "generate ID".

```python
with open('request.txt', 'w') as f:
    f.write("generate ID")
```


### How to receive the results 

Results can be read directly from the `request.txt` file.

```python
    with open('request.txt', 'r') as f:
        results = f.read()
    print(results)
```
