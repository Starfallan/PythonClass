#创建 字典 info
#以张三，李四为key，value包括（年龄：20，性别：男，爱好：打球）
#李四value为              （年龄:20,性别:男,爱好:学习）


info = {'张三':{'年龄':20,'性别':'男','爱好':'打球'},
        '李四':{'年龄':20,'性别':'男','爱好':'学习'}}
print(info)
#appedn()key为小红，value为（年龄：18，性别：女，爱好：旅游）
info['小红'] = {'年龄':18,'性别':'女','爱好':'旅游'}
print(info)
#更改李四年龄为40
info['李四']['年龄'] = 40
print(info)
