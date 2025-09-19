#include <iostream>
#include <map>
#include <string>

void p_map(const std::map<int, std::string>& m, std::string desc){
    std::cout << desc << " : " << std::endl;
    for (auto it = m.begin(); it != m.end(); it++){
        std::cout << "key : " << it->first << " , value : " << it->second << " | ";
    }
    std::cout << std::endl;
}

int main(){
    // 1. 初始化
    std::cout << "========= 初始化 =========" << std::endl;
    std::map<int, std::string> m = {
        {1,"ans"},
        {2,"res"}};
    p_map(m, "初始化列表");

    // 默认初始化, 创建空map
    std::map<int, std::string> m1;
    p_map(m1, "创建空map");
    
    // 使用构造函数
    std::map<int, std::string> m2;
    m2.insert(std::make_pair(1, "one"));
    p_map(m2, "后调用构造函数");

    std::cout << "========= 插入=========" << std::endl;
    // insert插入
    p_map(m2, "初始");
    m2.insert({2, "second"});
    p_map(m2, "insert插入");

    // [] 插入, 类似pytho的逻辑
    m2[3] = "thr";
    p_map(m2, "[] 插入");

    // emplace 插入
    m2.emplace(4, "four");
    p_map(m2, "emplace 插入");

    // insert or assing, 和[]一致 c++17 中支持
    // m2.insert_or_assign(f, "five");
    // p_map(m2, "insert_or_assign:");
    
    std::cout << "========= 删除=========" << std::endl;
    p_map(m2, "初始");
    // earse 按键删除
    m2.erase(2);
    p_map(m2, "earse 删除");

    // erase 按迭代器删除
    auto it = m2.find(4);
    if (it != m2.end()){
        m2.erase(it);
    }
    p_map(m2, "erase 迭代器删除");

    // erase 按范围删除
    m2.erase(m2.begin(), m2.find(3));
    p_map(m2, "erase 迭代器范围删除");

    // clear 清空
    m2.clear();
    p_map(m2, "clear 清空");

    std::cout << "========= 修改 ========" << std::endl;
    std::map<int, std::string> m3 = {
        {1, "one"},
        {2, "tow"},
        {3, "thr"}
    };
    p_map(m3, "初始");
    // [] 修改, 如果元素不存在则添加
    m3[1] = "1";
    p_map(m3, "[]修改");

    // at 修改, 如果元素不存在则抛出std::out_of_range异常
    m3.at(1) = "first";
    p_map(m3, "at修改");
    std::cout << "========= 查找 ========" << std::endl;
    p_map(m3, "初始");
    // [] or at find

    std::cout << "========= 常用方法 ========" << std::endl;
    // size 
    std::cout << "size : " << m3.size() << std::endl;

    // empty
    std::cout << "empty : " << m3.empty() << std::endl;
    
    // swap 交换两个map的内容
    std::map<int, std::string> m4 = {
        {1, "ans"},
        {2, "res"}
    };
    p_map(m3, "m3");
    p_map(m4, "m4");
    m3.swap(m4);
    p_map(m3, "swaped_m3");
    p_map(m4, "swaped_m4");

    // lower_bound() 返回指向 键值不小于给的那个值的第一个元素的迭代器
    auto it3 = m3.lower_bound(4);
    std::cout << "lower_bound 查到的值 : " << it3->first << " : " << it3->second << std::endl;
    
    return 0;
}