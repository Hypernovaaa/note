#include <vector>
#include <iostream>
#include <string>
#include <algorithm>

void p_vector(const std::vector<int>& vec, std::string desc){
   std::cout << desc << ": ";
   for (auto i: vec) std::cout << i << " ";
   std::cout << std::endl;
}

int main(){
    // 初始化方法
    // 默认初始化，空vector
    std::vector<int> v1;

    // 使用列表初始化
    std::vector<int> v2 = {1, 2, 3, 4, 5};

    // 指定大小和初始值
    std::vector<int> v3(5, 10); // 5个元素，每个值为10

    // 用另一个vector初始化
    std::vector<int> v4(v2);

    // 用迭代器区间初始化
    std::vector<int> v5(v2.begin(), v2.end());

    // 打印各个vector内容
    std::vector<int> v6(3);

    std::cout << "v6 size: " << v6.size() << std::endl;
    for (int i : v6){
        std::cout << i << std::endl;
    }

    std::cout << "v1 size: " << v1.size() << std::endl;
    std::cout << "v2: ";
    for (int i : v2) std::cout << i << " ";
    std::cout << std::endl;

    std::cout << "v3: ";
    for (int i : v3) std::cout << i << " ";
    std::cout << std::endl;

    std::cout << "v4: ";
    for (int i : v4) std::cout << i << " ";
    std::cout << std::endl;

    std::cout << "v5: ";
    for (int i : v5) std::cout << i << " ";
    std::cout << std::endl;

    std::cout << "常用方法" << std::endl;
    std::vector<int> ans = {1,2,3,4,5,6,7,8};
    // 判断容器是否为空
    std::cout << "是否为空? :" << ans.empty() << std::endl;
    std::vector<int> res;

    // 逻辑上设置容器的长度, 如果比原来的长会补充默认元素
    std::cout << "resize到3: ";
    ans.resize(3);
    for (int i: ans) std::cout << i << " ";
    std::cout << std::endl;

    // 查看容器的容量, 强制缩放到逻辑长度, 这回应该释放了内存了
    std::cout << "shrink_to_fit前容量: " << ans.capacity() << std::endl;
    ans.shrink_to_fit();
    std::cout << "shrink_to_fit后容量: " << ans.capacity() << std::endl;
    // 预先分配内存, 避免重复的内存分配
    ans.reserve(100);
    std::cout << "reserve(100)后容量: " << ans.capacity() << std::endl;

    std::cout << "===========增删改查=============" << std::endl;

    std::vector<int> v = {1,2,3,4,5,6,7,8,9};
    p_vector(v, "-------> 增加初始");
    // 增
    v.push_back(10);
    p_vector(v, "push_back 10");

    v.insert(v.begin() +2, 100);
    p_vector(v, "第二个位置插入");
    
    v.emplace_back(200);
    p_vector(v, "emplace_back 200");

    v.emplace(v.begin(), 300);
    p_vector(v, "emplace 300");

    // 删除
    p_vector(v, "-------> 删除初始");

    v.pop_back();
    p_vector(v, "pop back");

    v.erase(v.begin());
    p_vector(v, "erase 第一个元素");

    v.erase(v.begin(), v.begin() + 2);
    p_vector(v, "erase 第一个元素到第三个元素");

    // v.clear();
    // p_vector(v, "clear 删除全部");

    // 修改 
    p_vector(v, "-------> 修改初始");
    v[0] = 1000;
    p_vector(v, "下标修改");

    v.at(3) = 3000;
    p_vector(v, "at修改");

    std::vector<int>::iterator it = v.begin();
    *it = 40;
    p_vector(v, "iterator改");
    it++;
    *it = 50;
    p_vector(v, "iterator改");

    // 查找
    p_vector(v, "-------> 查找初始");
    std::cout << "下标: " << v[2] << std::endl;
    std::cout << "at: " << v.at(2) << std::endl;

    //find
    v[0] = 10;
    std::vector<int>::iterator it1 = std::find(v.begin(), v.end(), 10);
    if (it1 != v.end()){
        std::cout << "查找到了10的位置" << std::distance(v.begin(), it1) << std::endl;
    }
    return 0;
}
