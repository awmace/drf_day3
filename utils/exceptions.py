# 自定义异常处理
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework import status
def exception_handler(exc,context):
    # print(exc,'01010101',context)

    # 详细错误信息的定义
    error="%s %s %s"%(context['view'],context['request'].method,exc)
    print(error)

    # 先让drf处理，drf无法处理(返回值为None)再由自定义异常处理
    response=drf_exception_handler(exc,context)
    if response is None:
        return Response(
            {'error_msg':'程序失误了，请稍等一会'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,exception=None
        )
        # return  Response({'error_msg':error})  #error替换掉原来的内容
    # 异常信息不为空，说明异常已被drf处理
    return None