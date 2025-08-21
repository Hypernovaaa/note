# css选择器和xpath选择器的对比
1. 选中文档中的任意节点
    - css ele
    - xpath //ele

2. 选中两个元素
    - css ele1,ele2
    - xpath 无

3. 选中子元素
    - css ele1>ele2
    - xpath ele1 会选中所有子节点中的ele1元素

4. 选中兄弟元素
    - css ele1+ele2 
    - xpath 无

5. 根据属性选择元素
    ```html
    <a id="ans" class="reference"></a> 
    ```
    - 如果是class属性
        - css a.reference.ans 
        - xpath //a[contains(@class 'ref') and contains(@class 'ans')]
    
    - 如果是id属性
        - css a#ans
        - xpath //a[@id='ans']

    - 根据是否包含属性选择元素
        - css a[id][class]
        - xpath //a[@id and @class]

    - 根据属性值选择元素
        - css a[id="ans"][class="reference"]
        - xpath //a[@id="ans" and @class="reference"]
    
    - 根据属性值模糊选择元素
        - css a[id="ans"][class*="refer"]
        - xpath //a[@id="ans" and contains(@class, "refer")]

    - 这么一看在根据属性选择元素这方面,css是xpath的上位替代啊, xpath需要写在一个方括号里, css可以堆叠筛选条件

6. 提取属性或者文本内容
    - 提取属性内容 <a id="ans" class="reference"></a>
        - css a::attr(id).getall()
        - xpath //a/@id
        - 都是只支持单个属性的提取,需要多个属性的时候直接获取attrib字典比较方便

    - 提取文本内容 <a id="ans">text</a>
        - css a::text
        - xpath //a/text()

7. xpath string函数可以拼接文本
8. css可以按照范围选择子节点
9. xpath 可以根据文本内容选择元素
    - //a[contains(text(), "ans")]
    - //a[text()="ans"]

