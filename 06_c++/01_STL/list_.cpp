#include <iostream>
#include <list>
#include <string>

void p_list(const std::list<int>& l, std::string desc){
    std::cout << desc << ":" << std::endl; 
    for (int i : l){
        std::cout << i << " ";
    }
    std::cout << std::endl;
}
int main(){
    // list是c++中双向链表的实现, 所以随机插入和删除的时间复杂度为O(log_n), 随机访问的时间复杂度为O(n)
    std::cout << "-----------> list的初始化" << std::endl;
    std::list<int> l1;
    p_list(l1, "空的链表");

    std::list<int> l2(5, 10);
    p_list(l2, "初始化长度和默认值");

    std::list<int> l3 = {1,2,3,4,5,6};
    p_list(l3, "列表初始化");

    std::list<int> l4(l3);
    p_list(l4, "拷贝初始化");

    // 链表不支持随机索引, 所以不能使用[]运算符
    // 其余的增删改查方式基本一致
    // 删除所有等于3的元素的方法
    l3.push_back(3);
    l3.push_front(3);
    p_list(l3, "初始");
    l3.remove(3);
    p_list(l3, "remove 删除所有3");
    
}