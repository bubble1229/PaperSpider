# PaperSpider（爬取IEEE论文信息）

## 项目说明

### 功能说明
 
- 本项目实现了爬取[IEEE官网](http://ieeexplore.ieee.org/Xplore/home.jsp) 关于"Data Mining"相关的论文的信息，爬取的信息如下
    - 题目
    - 作者（文本格式存储中，多个作者以 ' | ' 分割）
    - 摘要
    - 收录刊物/会议名称
    - 收录时间/会议召开时间
    - 关键字（文本格式存储中，多个关键字以 ' | ' 分割）
    - 参考文献（文本格式存储中，多个参考文献以 ' | ' 分割）

### 环境说明

- 开发语言：Python
- 爬虫框架：scrapy
- 开发平台：ubuntu14.04

	更多关于scrapy的学习资料可以参考我们的博客[http://cilab-undefine.github.io/](http://cilab-undefine.github.io/)或者我的个人博客[www.we666.net](www.we666.net)



### 使用说明

1. 以Json/xml/csv等数据格式进行存储
	
	- `setting.py`中注释掉如下所示代码即可

			'paper.pipelines.MySQLStorePaperPipline':300,
	
	- 在项目根目录下执行如下命令运行

			scrapy crawl IEEESpider -o youDataFileName.json#请自行选定存储格式

2. 以MySQL的方式进行存储

	-  新建数据库和表，新建一个名为`paper`的数据库（为了保持良好习惯，数据编码请选择UFT-8），然后执行如下语句建表
		
			SET FOREIGN_KEY_CHECKS=0;
			
			-- ----------------------------
			-- Table structure for paper_authors
			-- ----------------------------
			DROP TABLE IF EXISTS `paper_authors`;
			CREATE TABLE `paper_authors` (
			  `id` int(11) NOT NULL AUTO_INCREMENT,
			  `systemId` int(11) NOT NULL,
			  `author` varchar(255) NOT NULL,
			  PRIMARY KEY (`id`)
			) ENGINE=InnoDB DEFAULT CHARSET=utf8;
			
			-- ----------------------------
			-- Table structure for paper_basic_info
			-- ----------------------------
			DROP TABLE IF EXISTS `paper_basic_info`;
			CREATE TABLE `paper_basic_info` (
			  `id` int(11) NOT NULL AUTO_INCREMENT,
			  `systemId` int(11) NOT NULL,
			  `title` varchar(255) NOT NULL,
			  `publishTime` varchar(100) NOT NULL,
			  `publishIn` varchar(255) NOT NULL,
			  `abstract` text NOT NULL,
			  `source` varchar(20) NOT NULL,
			  PRIMARY KEY (`id`)
			) ENGINE=InnoDB DEFAULT CHARSET=utf8;
			
			-- ----------------------------
			-- Table structure for paper_keywords
			-- ----------------------------
			DROP TABLE IF EXISTS `paper_keywords`;
			CREATE TABLE `paper_keywords` (
			  `id` int(11) NOT NULL AUTO_INCREMENT,
			  `systemId` int(11) NOT NULL,
			  `keyword` varchar(100) NOT NULL,
			  PRIMARY KEY (`id`)
			) ENGINE=InnoDB DEFAULT CHARSET=utf8;
			
			-- ----------------------------
			-- Table structure for paper_references
			-- ----------------------------
			DROP TABLE IF EXISTS `paper_references`;
			CREATE TABLE `paper_references` (
			  `id` int(11) NOT NULL AUTO_INCREMENT,
			  `systemId` int(11) NOT NULL,
			  `reference` text NOT NULL,
			  PRIMARY KEY (`id`)
			) ENGINE=InnoDB DEFAULT CHARSET=utf8;
			
	- 修改对应的**数据库连接、用户名、密码**信息
	- 输入如下命令运行
			
			scrapy crawl IEEESpider

---

<center>代码持续修改中，有bug请提出，自会及时修改。谢谢！</center>

---
