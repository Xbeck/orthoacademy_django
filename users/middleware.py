class SimpleMiddleware:
  def __init__(self, get_response):
    self.get_response = get_response

  def __call__(self, request):
    print(f"Before request for {request.path}")

    response = self.get_response(request)

    print("After getting response")

    return response