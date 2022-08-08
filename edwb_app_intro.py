from asyncio.log import logger
from re import search
import sys
import os
import json 
sys.path.insert(0, os.path.dirname(__file__))
from flask_sse import sse
from flask import Flask,jsonify
from flask import make_response, request, current_app
from functools import update_wrapper
from datetime import timedelta
# from flask_socketio import SocketIO


app = Flask(__name__, instance_relative_config=True)
app.config["REDIS_URL"] = "redis://localhost"
app.register_blueprint(sse, url_prefix='/streamexplainintro')
print(__name__,app)

app.secret_key =b'\xaa\x12\xce\xdf\xc3\xb1\x90\xd8!z\xe6\xe9V\x82<r'

srv_url = 'http://127.0.0.1:8097/'
# app.config.from_object('config')

# socketio = SocketIO(app,logger=True, engineio_logger=True) 
application = app

from flask import render_template
from flask import request,jsonify,session
import urllib
import model
# import forms
import datetime

COURSE_NAMES = None
NUM_COURSES = None
NUM_VIS = 0
MAX_HIST = 50

IS_LOCAL_SRV = True

def crossdomain(origin=None, methods=None, headers=None, max_age=21600,
                attach_to_all=True, automatic_options=True):
    """Decorator function that allows crossdomain requests.
    Courtesy of
    https://blog.skyred.fi/articles/better-crossdomain-snippet-for-flask.html
    """
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    # use str instead of basestring if using Python 3.x
    if headers is not None and not isinstance(headers, str):
        headers = ', '.join(x.upper() for x in headers)
    # use str instead of basestring if using Python 3.x
    if not isinstance(origin, str):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        """ Determines which methods are allowed
        """
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        """The decorator function
        """
        def wrapped_function(*args, **kwargs):
            """Caries out the actual cross domain code
            """
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers
            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            h['Access-Control-Allow-Credentials'] = 'true'
            h['Access-Control-Allow-Headers'] = \
                "Origin, X-Requested-With, Content-Type, Accept, Authorization"
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

def get_prev_urls():
    global NUM_VIS
    try:
        prev_urls = session['urls']
        # print ("prev",prev_urls,session['disp_strs'])
        NUM_VIS = len(prev_urls)
    except KeyError:
        session['urls'] = []
        session['disp_strs'] = []
        session.modified = True
        NUM_VIS = 0
    return list(session['urls']),list(session['disp_strs'])

def set_sess(url,ses_disp_str):
    global MAX_HIST,IS_LOCAL_SRV
    if not IS_LOCAL_SRV:

        url = modify_url_domain(url)
    if (len(session['urls'])==0) or (len(session['urls'])>0 and session['urls'][-1]!=url): #consecutive visits to same slide
        if len(session['urls']) == MAX_HIST:
            session['urls'].pop(0)
            session['disp_strs'].pop(0)
        session['urls'].append(url)
        session['disp_strs'].append(ses_disp_str)
        session.modified = True

def modify_url_domain(url):
    return url.replace('http://127.0.0.1:8097/','http://127.0.0.1:8097/')

@app.route('/')
def index():
    global COURSE_NAMES,NUM_COURSES,NUM_VIS
    COURSE_NAMES,NUM_COURSES = model.get_course_names()
    model.load_related_slides()
    vis_urls,vis_strs = get_prev_urls()

    return render_template("home.html",course_names=COURSE_NAMES,num_courses=NUM_COURSES,vis_urls=vis_urls,vis_strs=vis_strs,num_vis=NUM_VIS)

@app.route('/feedback')
def feedback():
    global COURSE_NAMES,NUM_COURSES
    if COURSE_NAMES is None and NUM_COURSES is None:
        COURSE_NAMES,NUM_COURSES = model.get_course_names()
        model.load_related_slides()
    vis_urls,vis_strs = get_prev_urls()
    return render_template("feedback.html",course_names=COURSE_NAMES,num_courses=NUM_COURSES,vis_urls=vis_urls,vis_strs=vis_strs,num_vis=NUM_VIS)



def resolve_slide(course_name,lno,type_,slide_name=None,log=False,action=None):
    global COURSE_NAMES,NUM_COURSES
    if COURSE_NAMES is None and NUM_COURSES is None:
        COURSE_NAMES,NUM_COURSES = model.get_course_names()
    if type_ =='drop-down':
        ret = model.get_next_slide(course_name,lno)
    elif type_ == 'related' or type_=='search_results':
        ret = model.get_slide(course_name,slide_name,lno)
    elif type_ == 'next':
        ret = model.get_next_slide(course_name,lno,slide_name)
    elif type_ == 'prev':
        ret = model.get_prev_slide(course_name,lno,slide_name)
    if log:
        if ret[0] is not None:
            print ('logging ', ret[0],request.headers.get("X-Forwarded-For"))
            model.log(request.headers.get("X-Forwarded-For").split(',')[0],ret[0],datetime.datetime.now(),action)
        else:
            model.log(request.headers.get("X-Forwarded-For").split(',')[0],'End',datetime.datetime.now(),action)
    return ret 

@app.route('/searchPage', methods= ["POST"])
def searchPage():
    srch_term = request.form.get("srch-term")
    app.logger.warning('searchPage')
 
    global COURSE_NAMES,NUM_COURSES
    if COURSE_NAMES is None and NUM_COURSES is None:
        COURSE_NAMES,NUM_COURSES = model.get_course_names()
        model.load_related_slides()
    next_slide_name,lno,lec_name,(num_related_slides,related_slides,disp_str,related_course_names,rel_lnos,rel_lec_names,disp_color,disp_snippet),lec_names,lnos,ses_disp_str,video_link, lec_slides = resolve_slide('CS 225',3,'drop-down')
    vis_urls,vis_strs = get_prev_urls()
    return render_template("searchPage.html",slide_name=next_slide_name,course_name= 'Select Course',num_related_slides=num_related_slides,related_slides = related_slides,disp_str=disp_str,disp_color=disp_color,disp_snippet=disp_snippet,related_course_names=related_course_names,lno=lno,lec_name=lec_name,lec_names=lec_names,lnos=lnos,course_names=COURSE_NAMES,num_courses=NUM_COURSES,rel_lnos=rel_lnos,rel_lec_names=rel_lec_names,vis_urls=vis_urls,vis_strs=vis_strs,num_vis=NUM_VIS,video_link=video_link,lec_slides=lec_slides, srch_term=srch_term)


@app.route('/slide/<course_name>/<lno>')
def slide(course_name,lno):
    global NUM_VIS
    next_slide_name,lno,lec_name,(num_related_slides,related_slides,disp_str,related_course_names,rel_lnos,rel_lec_names,disp_color,disp_snippet),lec_names,lnos,ses_disp_str,video_link, lec_slides = resolve_slide(course_name,lno,'drop-down')
    vis_urls,vis_strs = get_prev_urls()


    if next_slide_name is not None:
        set_sess(request.url,ses_disp_str)

    return render_template("slide.html",slide_name=next_slide_name,course_name=course_name,num_related_slides=num_related_slides,related_slides = related_slides,disp_str=disp_str,disp_color=disp_color,disp_snippet=disp_snippet,related_course_names=related_course_names,lno=lno,lec_name=lec_name,lec_names=lec_names,lnos=lnos,course_names=COURSE_NAMES,num_courses=NUM_COURSES,rel_lnos=rel_lnos,rel_lec_names=rel_lec_names,vis_urls=vis_urls,vis_strs=vis_strs,num_vis=NUM_VIS,video_link=video_link,lec_slides=lec_slides)

@app.route('/searchPage/<srch_term>/<course_name>')
def filter(srch_term, course_name):
    app.logger.warning(course_name)
    app.logger.warning(srch_term)
    global COURSE_NAMES,NUM_COURSES
    if COURSE_NAMES is None and NUM_COURSES is None:
        COURSE_NAMES,NUM_COURSES = course_name,1
        model.load_related_slides()
    next_slide_name,lno,lec_name,(num_related_slides,related_slides,disp_str,related_course_names,rel_lnos,rel_lec_names,disp_color,disp_snippet),lec_names,lnos,ses_disp_str,video_link, lec_slides = resolve_slide('CS 225',3,'drop-down')
    vis_urls,vis_strs = get_prev_urls()
    return render_template("searchPage.html",slide_name=next_slide_name,course_name=course_name,num_related_slides=num_related_slides,related_slides = related_slides,disp_str=disp_str,disp_color=disp_color,disp_snippet=disp_snippet,related_course_names=related_course_names,lno=lno,lec_name=lec_name,lec_names=lec_names,lnos=lnos,course_names=COURSE_NAMES,num_courses=NUM_COURSES,rel_lnos=rel_lnos,rel_lec_names=rel_lec_names,vis_urls=vis_urls,vis_strs=vis_strs,num_vis=NUM_VIS,video_link=video_link,lec_slides=lec_slides, srch_term=srch_term)
    
@app.route('/related_slide/<course_name>/<lno>/<slide_name>')
def related_slide(course_name,slide_name,lno):
    global NUM_VIS
    next_slide_name,lno,lec_name,(num_related_slides,related_slides,disp_str,related_course_names,rel_lnos,rel_lec_names,disp_color,disp_snippet),lec_names,lnos,ses_disp_str,video_link, lec_slides =resolve_slide(course_name,lno,'related',slide_name=slide_name)
    vis_urls,vis_strs = get_prev_urls()


    if next_slide_name is not None:
        set_sess(request.url,ses_disp_str)

    return render_template("slide.html",slide_name=next_slide_name,course_name=course_name,num_related_slides=num_related_slides,related_slides = related_slides,disp_str=disp_str,disp_color=disp_color,disp_snippet=disp_snippet,related_course_names=related_course_names,lno=lno,lec_name=lec_name,lec_names=lec_names,lnos=lnos,course_names=COURSE_NAMES,num_courses=NUM_COURSES,rel_lnos=rel_lnos,rel_lec_names=rel_lec_names,vis_urls=vis_urls,vis_strs=vis_strs,num_vis=NUM_VIS,video_link=video_link,lec_slides=lec_slides)



@app.route('/next_slide/<course_name>/<lno>/<curr_slide>')
def next_slide(course_name,lno,curr_slide):
    global NUM_VIS
    next_slide_name,lno,lec_name,(num_related_slides,related_slides,disp_str,related_course_names,rel_lnos,rel_lec_names,disp_color,disp_snippet),lec_names,lnos,ses_disp_str,video_link, lec_slides = resolve_slide(course_name,lno,'next',slide_name=curr_slide)

    vis_urls,vis_strs = get_prev_urls()


    if next_slide_name is not None:
        set_sess(request.url,ses_disp_str)


    if next_slide_name is not None:
        return render_template("slide.html",slide_name=next_slide_name,course_name=course_name,num_related_slides=num_related_slides,related_slides = related_slides,disp_str=disp_str,disp_color=disp_color,disp_snippet=disp_snippet,related_course_names=related_course_names,lno=lno,lec_name=lec_name,lec_names=lec_names,lnos=lnos,course_names=COURSE_NAMES,num_courses=NUM_COURSES,rel_lnos=rel_lnos,rel_lec_names=rel_lec_names,vis_urls=vis_urls,vis_strs=vis_strs,num_vis=NUM_VIS,video_link=video_link,lec_slides=lec_slides )
    else:
        return render_template("end.html",course_names=COURSE_NAMES,num_courses=NUM_COURSES,vis_urls=vis_urls,vis_strs=vis_strs,num_vis=NUM_VIS)

@app.route('/prev_slide/<course_name>/<lno>/<curr_slide>')
def prev_slide(course_name,lno,curr_slide):
    global NUM_VIS
    prev_slide_name,lno,lec_name,(num_related_slides,related_slides,disp_str,related_course_names,rel_lnos,rel_lec_names,disp_color,disp_snippet),lec_names,lnos,ses_disp_str,video_link, lec_slides=resolve_slide(course_name,lno,'prev',slide_name=curr_slide)

    vis_urls,vis_strs = get_prev_urls()

    if prev_slide_name is not None:
        set_sess(request.url,ses_disp_str)


    if prev_slide_name is not None:
        return render_template("slide.html",slide_name=prev_slide_name,course_name=course_name,num_related_slides=num_related_slides,related_slides = related_slides,disp_str=disp_str,disp_color=disp_color,disp_snippet=disp_snippet,related_course_names=related_course_names,lno=lno,lec_name=lec_name,lec_names=lec_names,lnos=lnos,course_names=COURSE_NAMES,num_courses=NUM_COURSES,rel_lnos=rel_lnos,rel_lec_names=rel_lec_names,vis_urls=vis_urls,vis_strs=vis_strs,num_vis=NUM_VIS,video_link=video_link,lec_slides=lec_slides)
    else:
        return render_template("end.html",course_names=COURSE_NAMES,num_courses=NUM_COURSES,vis_urls=vis_urls,vis_strs=vis_strs,num_vis=NUM_VIS)


@app.route('/end')
def end():
    global COURSE_NAMES,NUM_COURSES,NUM_VIS
    if COURSE_NAMES is None and NUM_COURSES is None:
        COURSE_NAMES,NUM_COURSES = model.get_course_names()
    vis_urls,vis_strs = get_prev_urls()
    return render_template("end.html",course_names=COURSE_NAMES,num_courses=NUM_COURSES,vis_urls=vis_urls,vis_strs=vis_strs,num_vis=NUM_VIS)

# @socketio.on('connect')
# def value_changed():
#     print("connected")


@app.route('/google_search', methods=['POST'])
def google_search():
    app.logger.warning('google_search')
    raw_results = request.json['results']
    query = request.json['query']
    ranked_index = model.rank_google_result(raw_results, request.json['context'], query)
    ranked_result = [raw_results[i] for i in ranked_index]
    # print(ranked_result,'m=======')
    # socketio.emit('google-search-result', ranked_result, broadcast=True)
    sse.publish({"message": "google-search-result","rankedResult":ranked_result}, type='publish')
    return 'OK'

@app.route('/txt_search', methods=['POST'])
def txt_search():
    app.logger.warning('/txt_search')
    query = request.json['query']
    ranked_result = model.search_txtbook(query)
    # print(ranked_result,'m=======')
    # socketio.emit('google-search-result', ranked_result, broadcast=True)
    sse.publish({"message": "google-search-result","rankedResult":ranked_result}, type='publish')
    return 'OK'


@app.route('/explain', methods=['POST','OPTIONS'])
@crossdomain(origin='*')
def socket_connection(course_name=None, lno=None, slide_name=None, curr_slide=None):

    search_string = request.json['searchString']

    context = request.json['slidesContext']
    app.logger.warning('explain')
    app.logger.warning(search_string)
    log_helper(search_string + '###EXPLAIN',request.json['route'])
    app.logger.warning('explain2')
    # socketio.emit('message', {"searchString": search_string, "context": context} ,broadcast=True) 
    print(request.json['url']) 
    if ('CS%20410') in request.json['url']:
        is_410 = True
        print('true')
    else:
        is_410 = False
    sse.publish({"is_410":is_410,"message": "explain","searchString":search_string,"context":context}, type='publish')
    print(request,search_string,'1')
    # model.log(request.remote_addr,search_string,datetime.datetime.now(),'search_query')
    # num_results,results,disp_strs,search_course_names,lnos, snippets,lec_names = model.get_search_results(search_string)
    # if not results:
    #   num_results = 0
    #   results = []

    return 'OK'

@app.route('/search', methods=['POST'])
def results(course_name=None, lno=None, slide_name=None, curr_slide=None):   
    data = json.loads(request.data)
    # print(1,1,data)
    querytext = data['searchString']
    explanation,file_names = model.get_explanation(querytext)
    if explanation == '':
        num_results = 0
    else:
        num_results = 1
    response = jsonify({ 'num_results': num_results, 'explanation':explanation,'file_names':file_names})
    # print(response)
    return response

@app.route('/search_slide/<course_name>/<lno>/<slide_name>')
def search_slide(course_name,slide_name,lno):
    return related_slide(course_name,slide_name,lno)

@app.route('/search_slides', methods=['POST'])
def search_results(lno=None, slide_name=None, curr_slide=None):
    search_string = request.json['searchString']
    course_name = request.json['course_name']
    app.logger.warning(course_name)
    app.logger.warning(search_string)
    app.logger.warning('search_slide')
    log_helper(search_string + '###QUERY',request.json['route'])
    app.logger.warning('search_slide2')
    num_results,results,disp_strs,search_course_names,lnos, snippets,lec_names = model.get_search_results(search_string, course_name)
    '''
    for i in range(0, len(search_course_names)):
        if (course_name != search_course_names[i]):
            app.logger.warning(i)
            results.pop(i)
            disp_strs.pop(i)
            lnos.pop(i)
            snippets.pop(i)
            lec_names.pop(i)
    num_results = len(results)
    search_course_names.clear()
    for i in range(0, num_results):
        search_course_names[i] = course_name
    
    app.logger.warning(num_results)
    app.logger.warning(len(search_course_names))
    app,logger.warning(search_course_names[0])
    app.logger.warning(snippets[0])
    '''
    if not results:
        num_results = 0
        results = []
    response = jsonify({ 'num_results': num_results, 'results':results, 'disp_strs':disp_strs, 'search_course_names': search_course_names,'lnos':lnos,'course_names':COURSE_NAMES,'num_courses':NUM_COURSES,'snippets':snippets,'lec_names':lec_names
    })
    return response

def log_helper(action,route):
    if action is not None and route is not None:
        route_ele = route.split('/')
        if IS_LOCAL_SRV:
            func_type = route_ele[1]
        else:
            func_type = route_ele[3]
        print (func_type,route_ele)
        if IS_LOCAL_SRV:
            beg = 2
        else:
            beg = 4
        if func_type == 'related_slide':
            resolve_slide(route_ele[beg],route_ele[beg+1],'related',slide_name=route_ele[beg+2].replace('%20',' '),log=True,action=action)
        elif func_type == 'next_slide':
            resolve_slide(route_ele[beg],route_ele[beg+1],'next',slide_name=route_ele[beg+2].replace('%20',' '),log=True,action=action)
        elif func_type == 'prev_slide':
            resolve_slide(route_ele[beg],route_ele[beg+1],'prev',slide_name=route_ele[beg+2].replace('%20',' '),log=True,action=action)
        elif func_type == 'slide':
            resolve_slide(route_ele[beg],route_ele[beg+1],'drop-down',log=True,action=action)
        elif func_type == 'search_slide':
            resolve_slide(route_ele[beg],route_ele[beg+1],'search_results',slide_name=route_ele[beg+2].replace('%20',' '),log=True,action=action)
        else:

            model.log(request.remote_addr,'',datetime.datetime.now(),action)

@app.route('/log_action',methods=['GET', 'POST'])
def log_action():
    request_dict = json.loads(request.data)
    action = request_dict['action']
    route = request_dict['route']
    log_helper(action,route)
    resp = jsonify(success=True)

    return resp 


if __name__ == '__main__':
    # socketio.run(app,host='localhost',port=8097)
    app.run(host='localhost',port=8097)
