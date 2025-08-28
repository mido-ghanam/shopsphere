from rest_framework_simplejwt.tokens import RefreshToken
from urllib.parse import urlparse

HostURL = "https://apis.shopsphere.midoghanam.site"
CodeSpaceURL = ""
def NowURL(request):
  return request.scheme + "://" + request.get_host()

def get_page_url(request):
  referer = request.META.get('HTTP_REFERER', '')
  return urlparse(referer).path if referer else '/'
