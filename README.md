# 2-player poker game.

## Author
| Author |
| ------------- |
| Damian Li | 
| William Ding | 
| Barry Niu | 

## BlackJack 
### 开始游戏
* `git clone https://github.com/kkli08/WhoRunsFast.git`
* `cd WhoRunsFast`

#### GUI Version:
* `cd bj-gui-test`
* `pip install requirements.txt`  
* `python BlackjackGUI.py`

#### Command line version:
* `python main.py`

### 规则
当你开始一局21点（Blackjack）时，你将和一名电脑玩家竞技。你们每个人都会收到1张牌，你的牌面朝上，电脑玩家的牌面朝下。你需要通过抽牌来使你的牌的总点数接近21点，但不能超过21点。如果你选择“Stay”，游戏玩家将抽牌。如果电脑玩家的牌的总点数超过21点，它就破产了，你将赢得这局游戏。否则，比较你的牌和电脑玩家的牌，点数更接近21点的人获胜。

每张牌的点数如下：

Ace（A）可以被计为1或11点
十点牌（10、J、Q和K）计为10点
其他牌的点数等于它们的面值（例如，2到9牌计为2到9点）
当你抽牌时，你可以选择抽一张新牌，也可以停止抽牌。如果你的牌的总点数超过21点，你就破产了，你将输掉这局游戏。如果你停止抽牌，那么电脑玩家将抽牌，直到它的牌的总点数至少为17点为止。如果电脑玩家的牌的总点数超过21点，它就破产了，你将赢得这局游戏。否则，比较你的牌和电脑玩家的牌，点数更接近21点的人获胜。

如果你抽到一个A牌和一个点数为10的牌，这被称为“Blackjack”，你将立即赢得这局游戏，即使电脑玩家的牌的总点数也为21点。如果你和电脑玩家的牌的总点数相同，这被称为“平局”，你将与电脑玩家分享这局游戏的胜利。

### 致谢
Thanks to [Barry Niu](https://github.com/KexunNiu):
* Participated in the design of bj's bot strategy algorithm
* Participate in the design of bj's GUI
* Add background music for bj
* Participated in the design of the bj game script facing process development by using PyQt

## WhoRunsFast Rules
### 胜利规则
先出完自己手中的牌为赢家。

### 出牌规则
1. 第一局游戏由第一个游戏者发，以后每局游戏都由上局赢的游戏者发牌。
2. 游戏者依次轮流出牌，后一家打出的牌必须比前一家打出的牌大，如没有可以弃权（Pass）。
3. 如果其他游戏者都Pass，则最后出牌的一方可以出新的牌型，到某个游戏者手中牌全部出完。
4. 选择Pass的游戏者会被随机增加1张手牌 。  

#### 牌的大小比较
1. 本游戏的牌点由大到小排列为：大王、小王、2、A、K、Q、J、10、9、8、7、6、5、4、3。
2. 单张、对、三同张、连对、连三同张、顺子等牌型，直接根据牌点确定大小，但要求出牌的数量必须相同。
3. 大王、小王、2 无法参与连对、连三同张、顺子等牌型


### 随机发牌规则
1. 牌堆一共54张牌，随机将牌打乱并分成三份，一份发给bot，一份发给用户。

### 牌型
#### 单张
单张扑克牌

#### 对
两张相同大小的牌组成一个对子

#### 三同张
三张相同大小的牌组成一个三同张

#### 顺子
（最少）五张连续的牌组成一个顺子（例：3、4、5、6、7）

#### 炸弹
四张一样的牌组成一个炸弹

## Bot Decision making Algorithm
