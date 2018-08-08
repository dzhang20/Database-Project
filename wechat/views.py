from django.shortcuts import render,HttpResponse
from django.contrib.auth.decorators import login_required
from wechat import models
from catalog.models import UserProfile
from wechat.models import EventGroup
import json,time,queue
# Create your views here.

MSG_RECORDS = {

}


# View dash(request):
# display the chat dashboard when logged in
@login_required
def dash(request):
        return render(request,'chat_dash.html')

@login_required
def send_msg(request):
        # print(request.POST)
        msg_data = request.POST.get('data')
        if msg_data:
                msg_data = json.loads(msg_data)
                msg_data['time'] = time.time()
                if msg_data['type'] == 'friend':
                        if not MSG_RECORDS.get(int(msg_data['receiver'])):
                                MSG_RECORDS[int(msg_data['receiver'])] = queue.Queue()
                        MSG_RECORDS[int(msg_data['receiver'])].put(msg_data)
                else:
                        group_members = models.EventGroup.objects.get(id = int(msg_data['receiver']))
                        for mb in group_members.members.select_related():
                                if not MSG_RECORDS.get(mb.id):
                                        MSG_RECORDS[mb.id] = queue.Queue()
                                if mb.id != request.user.userprofile.user_id:
                                        MSG_RECORDS[mb.id].put(msg_data)
        # print(MSG_RECORDS)
        return HttpResponse("message received")



# View get_msg(request):
# First create a queue for current user in the RECORDS if not exist, then obtain its message count and queue object
# if there are messages to post (count > 0), we append them to a list one by one
# if there is no message currently, the method initiates a get to queue every 60s and append to list if a new one appeared
# finally method repond by dumping the msg_list as json datas back to front-end
def get_msg(request):
        if request.user.userprofile.user_id not in MSG_RECORDS:
                # print("no queue for user[%s]"%request.user.userprofile.user_id,request.user)
                MSG_RECORDS[request.user.userprofile.user_id] = queue.Queue()
        msg_count = MSG_RECORDS[request.user.userprofile.user_id].qsize()
        q_obj = MSG_RECORDS[request.user.userprofile.user_id]
        msg_list = []
        if msg_count > 0:
                for msg in range(msg_count):
                        msg_list.append(q_obj.get())
        else:
                try:
                        msg_list.append(q_obj.get(timeout=60))
                except queue.Empty:
                        print("no new msg")
        return HttpResponse(json.dumps(msg_list))
