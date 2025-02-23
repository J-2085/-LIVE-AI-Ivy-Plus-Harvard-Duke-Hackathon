from flask import Blueprint,request
from backend_ibm.utils import get_ibm_red_vote,get_ibm_blue_vote,get_ibm_red_chat,get_ibm_blue_chat


aiRoute = Blueprint('aiRoute', __name__)


@aiRoute.route('/red_vote',methods=['POST'])
def red_vote():
    data = request.json
    prompt = data.get('prompt')
    active_list = data.get('active_list')
    return get_ibm_red_vote(prompt,active_list)


@aiRoute.route('/blue_vote',methods=['POST'])
def blue_vote():
    data = request.json
    prompt = data.get('prompt')
    active_list = data.get('active_list')
    return get_ibm_blue_vote(prompt,active_list)


@aiRoute.route('/red_chat',methods=['POST'])
def red_chat():
    data = request.json
    prompt = data.get('prompt')
    return get_ibm_red_chat(prompt)


@aiRoute.route('/blue_chat',methods=['POST'])
def blue_chat():
    data = request.json
    prompt = data.get('prompt')
    return get_ibm_blue_chat(prompt)




