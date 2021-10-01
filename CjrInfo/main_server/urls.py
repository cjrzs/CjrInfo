from django.conf.urls import url
from main_server.views import ReceiveWeChatMsgView, SyncMaterialToDatabase, EsRebuild

urlpatterns = [
    url(r'^wechat/receive_msg$', ReceiveWeChatMsgView.as_view()),
    url(r'^sync_data$', SyncMaterialToDatabase.as_view()),
    url(r'^rebuild$', EsRebuild.as_view()),
]


