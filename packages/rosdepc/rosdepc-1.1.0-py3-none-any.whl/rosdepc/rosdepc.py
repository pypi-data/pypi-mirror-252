import sys
import os
import rosdep2
rosdep2_path = rosdep2.__file__[:rosdep2.__file__.rfind('/')]

def main(args=None):
    print('您已经成功安装rosdepc,下面提示的用法中，请将rosdep替换为rosdepc使用～')
    
    print('欢迎使用国内版rosdep之rosdepc，我是作者小鱼！')
    print('学习机器人,就关注《鱼香ROS》（公众号|B站|CSDN）！')
    print('小鱼rosdepc正式为您服务')
    args = ''
    if len(sys.argv)>=2 and sys.argv[1]=='init':
        os.system("sudo rm -rf /etc/ros/rosdep/sources.list.d/20-default.list")
        os.system("sudo find "+rosdep2_path+" -type f -exec sed -i 's|https://raw.githubusercontent.com/ros/rosdistro/master/rosdep/sources.list.d/20-default.list|https://mirrors.tuna.tsinghua.edu.cn/github-raw/ros/rosdistro/master/rosdep/sources.list.d/20-default.list|g' {} \;")
    if len(sys.argv)>=2:
        args = ' '.join(sys.argv[1:])  
    command = 'rosdep '+args
    command = "export ROSDISTRO_INDEX_URL=https://mirrors.tuna.tsinghua.edu.cn/rosdistro/index-v4.yaml && "+command
    os.system(command)

    print("---------------------------------------------------------------------------")
    if len(sys.argv)>=2 and sys.argv[1]=='init':
        print('小鱼提示：恭喜你完成初始化，快点使用\n\n rosdepc update\n\n更新吧')
    if len(sys.argv)>=2 and sys.argv[1]=='update':
        print('小鱼恭喜：rosdepc已为您完成更新!!')
    print("---------------------------------------------------------------------------")
    print('小鱼科普：rosdep干什么用的？可以跳过吗？https://fishros.org.cn/forum/topic/2124')
    print('如果再使用过程中遇到任何问题，欢迎通过fishros.org.cn反馈，或者加入QQ交流群(139707339)')

