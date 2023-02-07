# -*- coding: utf-8 -*-
# # #############################################################################
# Copyright (C) 2022 manatlan manatlan[at]gmail(dot)com
#
# MIT licence
#
# https://github.com/manatlan/htag
# #############################################################################

from .. import Tag
from ..render import HRenderer
from . import commons


""" REAL WEB http,
- .exit() has no effect ;-)
- can handle multiple client (with request.session/starlette (see commons.htagsession))
- can handle multiple "tag class", and brings query_params as "query_params:dict" when instanciate tag
- the hr session are purged automatically after timeout/5m of inactivity
- "http get query_params" are passed at Tag'init, if it accepts a query_params:dict param. (needed for https://htag.glitch.me)
- the main root is setable with path parameter (default: "/")
- add renew (bool) parametter on .serve() (and instanciate), to force renewal in all cases.
"""

import time
import asyncio
import logging

from starlette.applications import Starlette
from starlette.responses import HTMLResponse,JSONResponse,Response
from starlette.routing import Route
logger = logging.getLogger(__name__)

QN = lambda klass: (klass.__module__+"."+klass.__qualname__).replace("__main__.","")

class WebHTTP(Starlette):
    """ Simple ASync Web Server (with starlette) with HTTP interactions with htag.
        can handle multiple instances & multiples Tag

        The instance is an ASGI htag app
    """
    def __init__(self,tagClass:type=None, timeout=5*60):
        if tagClass: assert issubclass(tagClass,Tag)
        self.tagClass=tagClass
        self.timeout=timeout
        self.sessions={} # {htuid:session,}

        routes=[ Route('/{fqn:str}-{hrid:int}',   self.POST,  methods=["POST"]) ]
        if tagClass:
            routes.append( Route("/",   self.GET,   methods=["GET"]) )

        Starlette.__init__(self,debug=True, routes=routes, on_startup=[self._purgeSessions])
        Starlette.add_middleware(self,commons.HtagSession, sessions=self.sessions )

    def purger(self,timeout:float) -> int:
        """ remove session from sessions whose are older than 'timeout' seconds"""
        now=time.time()
        to_remove=[]
        for htuid,data in self.sessions.items():
            if "lastaccess" in data:
                if now - data["lastaccess"] > timeout:
                    to_remove.append( htuid )
            else:
                # remove session which hasn'g got a lastaccess timestamp
                to_remove.append( htuid )
        for htuid in to_remove:
            del self.sessions[htuid]
        return len(to_remove)

    async def _purgeSessions(self):
        session=self.middleware_stack.app   # solid ? TODO: do better
        logger.info(f"PURGE: started")

        async def loop():
            while True:
                nb=self.purger( self.timeout )
                logger.info(f"PURGE: remove %s session(s)",nb)
                await asyncio.sleep(60) # check every 60s

        asyncio.ensure_future( loop() )

    async def GET(self,request) -> HTMLResponse:
        return self.serve(request, self.tagClass )

    def serve(self,request, klass, init=None, renew=False) -> HTMLResponse:
        """ Serve for the `request`, an instance of the class 'klass'
        initialized with `init` (tuple (*args,**kargs))
        if init is None : takes them from request.url ;-)

        return an htmlresponse (htag init page to start all)
        """
        request.session["HRSessions"] = request.session.get( "HRSessions", commons.HRSessions() )

        if init is None:
            # no init params
            # so we take thoses from the url
            init = commons.url2ak( str(request.url) )
        else:
            assert type(init)==tuple
            assert type(init[0])==tuple
            assert type(init[1])==dict

        hr = self.instanciate(request, klass, init , renew)
        request.session["lastaccess"]=time.time()

        return HTMLResponse( str(hr) )

    def instanciate(self, request, klass, init, renew) -> HRenderer:
        """ get|create an instance of `klass` for user session """
        fqn = QN(klass)

        logger.info("intanciate : renew=%s",renew)
        hr=request.session["HRSessions"].get_hr( fqn )
        if renew==False and hr and hr.init == init:
            # same url (same klass/params), same htuid -> same instance
            logger.info("intanciate : Reuse Renderer %s ",fqn)
        else:
            # url has changed ... recreate an instance
            logger.info("intanciate : Create Renderer %s",fqn)

            js = """
                async function interact( o ) {
                    let resp = await window.fetch("/%s-<<hrid>>",{method:"POST", body:JSON.stringify(o)});
                    if(resp.status == 412)
                        alert("Session has ended");
                    else
                        action( await resp.text() );
                }
                window.addEventListener('DOMContentLoaded', start );
            """ % fqn

            hr=HRenderer(klass, js, init=init, session=request.session ) # NO EXIT !!

        # update session info

        request.session["HRSessions"].set_hr( fqn,hr )
        return hr


    async def POST(self,request) -> Response:
        fqn=request.path_params.get('fqn',None)
        hrid=request.path_params['hrid']

        hr=request.session["HRSessions"].get_hr( fqn )
        if hr:
            if id(hr) == hrid:
                # we are on the right current instance
                request.session["lastaccess"]=time.time()
                logger.info("INTERACT WITH %s",fqn)
                data=await request.json()
                actions = await hr.interact(data["id"],data["method"],data["args"],data["kargs"],data["event"])
                return JSONResponse(actions)
            else:
                # Current instance has been renewed, and you talking to a dead objet !
                return HTMLResponse( "412 DOESN'T MATCH CURRENT INSTANCE" , status_code=412 ) # 412 Precondition Failed
        else:
            # session expired or bad call
            return HTMLResponse( "400 BAD REQUEST" , status_code=400 )


    def run(self, host="0.0.0.0", port=8000):   # wide, by default !!
        import uvicorn
        uvicorn.run(self, host=host, port=port)
