from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from blocks.rpc.SimpleJSONRPCServer import SimpleJSONRPCDispatcher

# Create a Dispatcher; this handles the calls and translates info to function maps
dispatcher = SimpleJSONRPCDispatcher(allow_none=False, encoding=None)

def echo(a):
    return "pong %s" % a

def pages():
    from blocks.apps.core.models import StaticPage
    return list(StaticPage.objects.values())

# you have to manually register all functions that are xml-rpc-able with the dispatcher
# the dispatcher then maps the args down.
# The first argument is the actual method, the second is what to call it from the XML-RPC side...
dispatcher.register_function(echo, 'echo')

dispatcher.register_function(pages, 'pages')

@login_required
def rpc_request(request):
    response = HttpResponse()
    if len(request.POST):
        response.write(dispatcher._marshaled_dispatch(request.raw_post_data))
    else:
        response.write("<b>This is an XML-RPC Service.</b><br>")
        response.write("You need to invoke it using an XML-RPC Client!<br>")
   
        if settings.DEBUG:
            response.write("The following methods are available:<ul>")
            methods = dispatcher.system_listMethods()

            for method in methods:
                sig = dispatcher.system_methodSignature(method)

                # this just reads your docblock, so fill it in!
                help =  dispatcher.system_methodHelp(method)

                response.write("<li><b>%s</b>: [%s] %s" % (method, sig, help))

            response.write("</ul>")

    response['Content-length'] = str(len(response.content))
    return response
