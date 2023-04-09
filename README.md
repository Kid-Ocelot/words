Made by Kid_Ocelot
Kidware Word Translating,Reciting and Management System
https://kid-ocelot.github.io

总的一个就是如下
"Words 预设23 new.db"是预填充了Youdaoid与一些词语的db
	推荐复制然后把副本的文件名改短一点（）直接在main里使用
"main.py"是全英语的，开始如导入请填充完整文件名 Eg:"Words.db" 
	或者选择新建数据库 Appid和Appsecret在py文件的开头注释也有
	另外main里是有帮助（Main>>9.help）的
"README.txt"是本文件来着（）
"mainCN.py"是中文手动翻译（雾），可能会看着不顺眼？毕竟我是根据已经写好的英语翻的
"mainCN.exe"和"main.exe"是打包成exe的命令行文件！ 对于这个程序 db的位置还是在同目录捏
"Install.bat"是为py运行提供环境（requests）的pip程序！ 需求先装好py*  不会有人不装py吧，不会吧不会吧
"requirements.txt"里是"Install.bat"调用的pip包目录 实际上就一个requests