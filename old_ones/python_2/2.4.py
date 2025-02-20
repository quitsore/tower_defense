http_code = int(input("http_code: "))

match http_code:
    case 200 | 201 | 202:
        print("Success")
    case 400 | 401 | 402 | 403 | 404:
        print("Client Error")
    case 500 | 501 | 502 | 503:
        print("Server Error")
    case _:
        print("Unknown Status")
