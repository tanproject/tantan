'''缓存中存在的所有key'''

MODEL_K = 'Model-%s-%s' #模型缓存里的key，用来拼接Model名和对象的主键
VCODE_K='Vcode-%s'  #验证码缓存里的key，用来拼接用户手机号
PRIOR_RCMD_LIST='PriorRcmdL-%s' #优先推荐列表，拼接被滑用户id
REWIND_TIMES_K='Rewind_Times_K-%s-%s'   #每日反悔次数，拼接日期和用户id