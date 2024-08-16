import os
import json
import random

def Similar_Strings(Str, Stry): #侦测字符串相似值
    if isinstance(Str, str) == False or isinstance(Stry, str) == False:
        raise ValueError("Pyvirertory Key Must Be <str>")
    Boundary = 0 #定义侦测字符串的【边界线】
    count = 0 #计数变量
    KeyStry, IFStry = None, None #被遍历字符串【长】,被侦测字符串【短】
    if len(Stry) > len(Str): #对比字符串长度,设置字符串遍历关系
        KeyStry, IFStry = Stry,Str
    else: 
        KeyStry, IFStry = Str,Stry

    for Key in KeyStry: #遍历字符串【钥匙】
        if Boundary > (len(IFStry)-1): #侦测边界线是否超出字符串索引范围
            break
        if (IFStry[Boundary] not in KeyStry) and (Boundary+1 <= (len(IFStry)-1)):
            Boundary += 1 #如果 被侦测字符 不存在于 被遍历字符串则跳过
        if Key == IFStry[Boundary]: #侦测字符是否相同【锁】
            count += 1
            Boundary += 1
    if int(len(KeyStry)/2) < count: #计算相同字符的数量是否满足判断条件
        return "OK"
        
def AIKey(storage="None", Moodkey="None", Mypath="AI-key", KeyMode="training"):
    if KeyMode not in ["training", "Conversation"]: #报错提示
        raise ValueError("Pyvirertory Cant Get <KeyMode> Must Be <training Conversation>")
    if isinstance(storage, str) == False or isinstance(Moodkey, str) == False: #报错提示
        raise ValueError("Pyvirertory <Moodkey storage> Must Be <str>")
        
    Memory_Storage, Conversation_list, Button_list = {}, [], []
    if os.path.exists((Mypath + ".json")): #检测路径里有没有存储的记忆空间,这是有的情况
        with open((Mypath + ".json"), "r+",encoding="utf-8") as My: #打开记忆空间
            Memory_Storagey = json.load(My) #读取记忆空间
            for key in Memory_Storagey: #循环侦测,选取对话列表
                if Moodkey == json.loads(key)[1] and Similar_Strings(storage, json.loads(key)[0]) == "OK":
                    Conversation_list.append(Memory_Storagey[key])
                    Button_list.append(key)
        
        if Conversation_list == []: #若与问题匹配的对话列表不存在,创建对话列表
            if KeyMode == "training":
                print("【问题未收录】已创建新对话列表")
                Memory_Storagey[json.dumps([storage, Moodkey], ensure_ascii=False)] = [input("请输入您想让AI回复的答案: ")] #储存记忆空间(答案)
                with open((Mypath + ".json"), "w",encoding="utf-8") as My:
                    json.dump(Memory_Storagey, My, ensure_ascii=False) #写入训练数据 
            
            elif KeyMode == "Conversation":
                return "我听不懂您在说什么【未收录】"
        else:
            Number = random.randint(0, len(Conversation_list)-1)
            if KeyMode == "training":
                print(Conversation_list[Number][random.randint(0, len(Conversation_list[Number])-1)])
                AND = input("请输入您想让AI回复的答案: ")
                if AND == "None":
                    return "【训练已结束】"
                
                Memory_Storagey[Button_list[Number]].append(AND) #储存记忆空间(答案)
                with open((Mypath + ".json"), "w",encoding="utf-8") as My:
                    json.dump(Memory_Storagey, My, ensure_ascii=False) #写入训练数据
            elif KeyMode == "Conversation":
                return Conversation_list[Number][random.randint(0, len(Conversation_list[Number])-1)]
        return "【训练已结束】"
        
    else: #没有的情况
        with open((Mypath + ".json"), "w", encoding="utf-8") as My: #with open创建记忆空间文件
            json.dump(Memory_Storage, My, ensure_ascii=False) #写入训练数据
        print("已创建记忆空间:【" + Mypath +".json】")