from django.http import JsonResponse

def error404(request, exception):
  return JsonResponse({"status": False, "error": "404 Not Found", "details": "URL Path NOT FOUND"}, status=404)

def error500(request):
  return JsonResponse({"status": False, "error": "500 Internal Error", "details": "Internal Error"}, status=500)

def status(request):
  return JsonResponse({"status": True}, status=200)
