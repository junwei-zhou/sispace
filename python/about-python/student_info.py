'''
user:junwei-zhou
time:2020/4/20
'''
grade = []
str_print="姓名:{} \t数学:{} \t语文:{} \t英语:{} \t 总分:{}"
while True:
    print('''***********欢迎使用学生信息管理系统**********
        请输入以下的选择：
            1.新建学生信息
            2.显示全部学生信息
            3.查询学生信息
            4.删除学生信息
            5.修改学生信息
            0.退出系统
    ***********************************************''')
    action = input('请选择你的输入选项：')
    if action == "1":
        '''新建学生信息'''
        name = input('please input name:')
        math = input('please input math:')
        chinese = input('please input chinese:')
        english = input('please input english:')
        total = int(math)+int(chinese)+int(english)
        grade.append([name,math,chinese,english,total])
        print(str_print.format(name,math,chinese,english,total))
    elif action == "2":
        '''显示全部学生信息'''
        for info in grade:
            print(str_print.format(*info))

    elif action == "3":
        '''查询学生信息'''
        name = input('please input the name you check:')
        for info in grade:
            if name in info:
                print(str_print.format(*info))
                break
        else:
            print('no found')

    elif action == "4":
        '''删除学生信息'''
        name = input('please input the name you want to del')
        for info in grade:
            if name in info:
                info_ = grade.pop(grade.index(info))
                print('the name you del is ',info_)

    elif action == "5":
        '''修改学生信息'''
        name = input('please input the name you want to fix')
        for info in grade:
            if name in info:
                index = grade.index(info)
                break
        else:
            print('no found the name')
            continue
        math = input('please input math:')
        chinese = input('please input chinese:')
        english = input('please input english:')
        total = int(math) + int(chinese) + int(english)
        grade[index][1:]=[math, chinese, english, total]
        print('修改后的信息为',grade[index])
    elif action == "0":
        '''退出系统'''
        break
    else:
        print('输入有误')
