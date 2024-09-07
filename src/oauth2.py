from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.files.file import File
import io
import pandas as pd



sharepoint_url = 'https://diamonddelivery-my.sharepoint.com/'
tenant_id = '3f65100d-6d42-4737-8d83-3c9b1c7b56f8'
client_id = 'b1d6852b-fb3f-435a-ab82-a7e5bcbe04b0'
relative_url = '/personal/croman_rdiamondgroup_com/Documents/Sep-Obws.xlsm'



ctx_auth = AuthenticationContext(sharepoint_url)
ctx_auth.with_interactive(tenant_id, client_id)
ctx = ClientContext(sharepoint_url, ctx_auth)
web = ctx.web
ctx.load(web)
ctx.execute_query()

response = File.open_binary(ctx, relative_url)
response

bytes_file_obj = io.BytesIO()
bytes_file_obj.write(response.content)
bytes_file_obj.seek(0) #set file object to start

df = pd.read_excel(bytes_file_obj)
df.head(10)
