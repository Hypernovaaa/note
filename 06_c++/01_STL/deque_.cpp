#include <deque> 
#include <iostream>
#include <string> 

void p_deque(const std::deque<int> que, std::string desc){
    std::cout << desc << " : " << std::endl;
    for (int i : que){
        std::cout << i << " ";
    }
    std::cout << std::endl;
}

int main(){
    // 默认构造空的队列
    std::deque<int> d;
    p_deque(d, "默认构造的空");

    // 指定大小的初始化，每个元素的值为0
    std::deque<int> d1(5);
    p_deque(d1, "指定初始大小");

    // 初始化大小， 并并且为设置默认值
    std::deque<int> d2(5, 10);
    p_deque(d2, "指定初始大小和默认值");

    // 使用列表初始化
    std::deque<int> d3 = {1,2,3,4,5};
    p_deque(d3, "列表初始化");

    std::cout << "------------> 增加元素" << std::endl;
    p_deque(d3, "初始");
    d3.push_back(999);
    p_deque(d3, "队列末尾添加");

    d3.push_front(0);
    p_deque(d3, "队列开始添加");

    auto it1 = d3.begin() + 3;
    d3.insert(it1, 33);
    p_deque(d3, "在第三个位置插入");

    std::cout << "------------> 删除元素" << std::endl;
    p_deque(d3, "初始");
    d3.pop_back();
    p_deque(d3, "弹出末尾元素");

    d3.pop_front();
    p_deque(d3, "弹出开始元素");

    auto it2 = d3.begin() + 3;
    d3.erase(it2);
    p_deque(d3, "删除第三个元素");

    

    return 0;
}