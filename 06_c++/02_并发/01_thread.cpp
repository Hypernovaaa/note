#include <iostream>
#include <thread>
#include <string>

void say_something(std::string name){
    std::cout << "in thread : " << name << std::endl;
}

int main(){
    std::thread t1(say_something, "t1");
    t1.join();
    return 0;
}