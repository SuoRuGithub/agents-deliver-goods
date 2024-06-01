# 实验结果展示

下图中两仓库距离较近，因此智能体较为拥挤，可以清楚地看到它们之间存在相互避让

<p align="center"> 
<img src=".\demo0.gif">
</p>
<p align="center"> 
参数：地图尺寸 10 x 10，智能体数量：4，货物数量：10
</p> 

下面是另一个同样参数条件下的示例
<p align="center"> 
<img src=".\demo1.gif">
</p>
<p align="center"> 
参数：地图尺寸 10 x 10，智能体数量：4，货物数量：10
</p> 

我们还可以改变相关参数，下面两个示例中，我扩大了地图大小，并增加了智能体和货物数量

<p align="center"> 
<img src=".\demo1.gif">
</p>
<p align="center"> 
参数：地图尺寸 32 x 32，智能体数量：8，货物数量：30
</p> 

<p align="center"> 
<img src=".\demo3.gif">
</p>
<p align="center"> 
参数：地图尺寸 64 x 64，智能体数量：10，货物数量：40
</p> 

但是本次实验还存在很多不足，下面是一些出现了问题的示例：

<p align="center"> 
<img src=".\bug0.gif">
</p>
<p align="center"> 
参数：地图尺寸 10 x 10，智能体数量：4，货物数量：10
</p> 

<p align="center"> 
<img src=".\bug1.gif">
</p>
<p align="center"> 
参数：地图尺寸 32 x 32，智能体数量：8，货物数量：20
</p> 

作者本意想让智能体在完成任务之后返回出生点，但是上面两个示例在返回出生点的路径搜索上出现了问题，因此并没有返回