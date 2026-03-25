#!/usr/bin/env python3
"""
校园失物招领平台 - 测试数据初始化脚本
"""
import os, sys, django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
sys.path.insert(0, '/home/ubuntu/campus_laf')
django.setup()

from django.contrib.auth import get_user_model
from items.models import Item, Message
from matches.models import Match

User = get_user_model()

print("🚀 开始初始化测试数据...")

# ─────────────────────────────────────────────
# 1. 创建测试用户
# ─────────────────────────────────────────────
users_data = [
    {
        'username': 'zhangwei',
        'password': 'test123456',
        'email': 'zhangwei@stu.campus.edu',
        'user_type': 'student',
        'department': '计算机科学与技术学院',
        'phone': '13812345678',
        'student_id': '2021010001',
    },
    {
        'username': 'lihua',
        'password': 'test123456',
        'email': 'lihua@stu.campus.edu',
        'user_type': 'student',
        'department': '外国语学院',
        'phone': '13987654321',
        'student_id': '2021020002',
    },
    {
        'username': 'wangfang',
        'password': 'test123456',
        'email': 'wangfang@stu.campus.edu',
        'user_type': 'student',
        'department': '经济管理学院',
        'phone': '15612345678',
        'student_id': '2022030003',
    },
    {
        'username': 'chenming',
        'password': 'test123456',
        'email': 'chenming@stu.campus.edu',
        'user_type': 'student',
        'department': '机械工程学院',
        'phone': '18812345678',
        'student_id': '2021040004',
    },
    {
        'username': 'teacher_liu',
        'password': 'test123456',
        'email': 'liulaoshi@campus.edu',
        'user_type': 'teacher',
        'department': '数学与统计学院',
        'phone': '13600001111',
        'student_id': '',
    },
]

created_users = {}
for ud in users_data:
    user, created = User.objects.get_or_create(username=ud['username'])
    user.set_password(ud['password'])
    user.email = ud['email']
    user.user_type = ud['user_type']
    user.department = ud['department']
    user.phone = ud['phone']
    if ud['student_id']:
        user.student_id = ud['student_id']
    user.save()
    created_users[ud['username']] = user
    status = '✅ 新建' if created else '🔄 更新'
    print(f"  {status} 用户: {ud['username']} ({ud['email']})")

# ─────────────────────────────────────────────
# 2. 创建物品（happened_at 是正确字段名）
# ─────────────────────────────────────────────
now = datetime.now()

items_data = [
    # ── 失物招领（found）──
    {
        'user': created_users['zhangwei'],
        'type': 'found',
        'title': '捡到一张学生证（李华）',
        'category': 'id_card',
        'location': '图书馆一楼自习区',
        'happened_at': now - timedelta(days=1, hours=2),
        'description': '在图书馆一楼靠窗自习区的桌子上捡到一张学生证，姓名李华，外国语学院，照片清晰。学生证外有一个蓝色卡套。',
        'contact_phone': '13812345678',
        'contact_wechat': 'zhangwei_2024',
        'status': 'active',
        'is_approved': True,
    },
    {
        'user': created_users['wangfang'],
        'type': 'found',
        'title': '捡到黑色华为手机一部',
        'category': 'electronics',
        'location': '教学楼B栋203教室',
        'happened_at': now - timedelta(hours=5),
        'description': '下课后在B203教室最后一排座位上捡到一部黑色华为Mate60手机，屏幕有轻微划痕，手机壳是深蓝色磨砂材质，锁屏壁纸是一只猫。',
        'contact_phone': '15612345678',
        'contact_wechat': 'wangfang_stu',
        'status': 'active',
        'is_approved': True,
    },
    {
        'user': created_users['chenming'],
        'type': 'found',
        'title': '捡到一串钥匙（含宿舍钥匙）',
        'category': 'keys',
        'location': '操场东门附近',
        'happened_at': now - timedelta(days=2),
        'description': '在操场东门附近草坪捡到一串钥匙，共3把，其中一把是宿舍楼门禁卡式钥匙，另外两把是普通钥匙，钥匙扣是一个小熊猫挂件。',
        'contact_phone': '18812345678',
        'status': 'active',
        'is_approved': True,
    },
    {
        'user': created_users['teacher_liu'],
        'type': 'found',
        'title': '捡到《高等数学》教材一本',
        'category': 'books',
        'location': '第三教学楼305教室',
        'happened_at': now - timedelta(days=3),
        'description': '在三教305教室讲台旁边捡到一本《高等数学》（同济大学第七版），书内有大量铅笔笔记，扉页写有"陈明"二字，目前放在数学学院办公室。',
        'contact_phone': '13600001111',
        'status': 'active',
        'is_approved': True,
    },
    {
        'user': created_users['zhangwei'],
        'type': 'found',
        'title': '捡到棕色真皮钱包',
        'category': 'wallet',
        'location': '学生食堂二楼',
        'happened_at': now - timedelta(hours=8),
        'description': '在学生食堂二楼靠近收银台的座位上捡到一个棕色真皮钱包，内有现金约200元、银行卡2张、校园一卡通1张，无身份证。',
        'contact_phone': '13812345678',
        'contact_wechat': 'zhangwei_2024',
        'status': 'active',
        'is_approved': True,
    },
    {
        'user': created_users['lihua'],
        'type': 'found',
        'title': '捡到白色苹果AirPods耳机',
        'category': 'electronics',
        'location': '图书馆二楼阅览室',
        'happened_at': now - timedelta(days=1),
        'description': '在图书馆二楼阅览室靠近窗户的位置捡到一个白色苹果AirPods Pro耳机盒（第二代），充电盒内有耳机，电量约60%，盒子背面有一个小贴纸。',
        'contact_phone': '13987654321',
        'status': 'active',
        'is_approved': True,
    },
    {
        'user': created_users['wangfang'],
        'type': 'found',
        'title': '捡到黑色耐克双肩包',
        'category': 'other',
        'location': '体育馆更衣室',
        'happened_at': now - timedelta(days=4),
        'description': '在体育馆更衣室捡到一个黑色耐克双肩包，包内有运动衣一套、毛巾一条、水杯一个（蓝色保温杯），包侧面有白色耐克logo。',
        'contact_phone': '15612345678',
        'status': 'matched',
        'is_approved': True,
    },
    {
        'user': created_users['chenming'],
        'type': 'found',
        'title': '捡到女生白色羽绒服一件',
        'category': 'clothing',
        'location': '女生宿舍楼门口',
        'happened_at': now - timedelta(days=1, hours=5),
        'description': '在女生宿舍楼门口捡到一件白色羽绒服，品牌是波司登，M码，左胸口袋内有一张图书馆借阅卡，衣服干净完好。',
        'contact_phone': '18812345678',
        'status': 'active',
        'is_approved': True,
    },

    # ── 寻物启事（lost）──
    {
        'user': created_users['lihua'],
        'type': 'lost',
        'title': '寻找丢失的学生证',
        'category': 'id_card',
        'location': '图书馆或教学楼B栋',
        'happened_at': now - timedelta(days=1),
        'description': '本人李华，外国语学院大三学生，昨天在图书馆自习后发现学生证丢失，学生证外有蓝色卡套，照片是短发，非常重要，急需找回，谢谢！',
        'contact_phone': '13987654321',
        'contact_wechat': 'lihua_english',
        'status': 'matched',
        'is_approved': True,
    },
    {
        'user': created_users['chenming'],
        'type': 'lost',
        'title': '丢失黑色华为Mate60手机',
        'category': 'electronics',
        'location': '教学楼B栋附近',
        'happened_at': now - timedelta(hours=6),
        'description': '今天下午在B栋上完课后发现手机不见了，黑色华为Mate60，深蓝色磨砂手机壳，锁屏是一只橘猫的壁纸，手机内有重要资料，急寻！悬赏200元！',
        'contact_phone': '18812345678',
        'contact_wechat': 'chenming_mech',
        'status': 'active',
        'is_approved': True,
    },
    {
        'user': created_users['teacher_liu'],
        'type': 'lost',
        'title': '寻找遗失的U盘（内含重要课件）',
        'category': 'electronics',
        'location': '第三教学楼305教室',
        'happened_at': now - timedelta(days=2),
        'description': '本人刘老师，在三教305上完课后发现一个红色金士顿U盘遗失，容量32G，内含本学期所有课件和考试资料，非常重要！找到者请联系，必有重谢！',
        'contact_phone': '13600001111',
        'status': 'active',
        'is_approved': True,
    },
    {
        'user': created_users['wangfang'],
        'type': 'lost',
        'title': '丢失黑色钱包（内有银行卡）',
        'category': 'wallet',
        'location': '学生食堂或超市',
        'happened_at': now - timedelta(hours=10),
        'description': '今天中午在食堂吃饭后发现钱包不见了，黑色长款钱包，内有现金约200元、工商银行卡1张、校园一卡通1张，钱包内侧有一张家人合照，非常重要！',
        'contact_phone': '15612345678',
        'status': 'active',
        'is_approved': True,
    },
    {
        'user': created_users['zhangwei'],
        'type': 'lost',
        'title': '寻找遗失的宿舍钥匙',
        'category': 'keys',
        'location': '操场或宿舍楼附近',
        'happened_at': now - timedelta(days=2, hours=3),
        'description': '丢失一串钥匙，共3把，其中一把是宿舍楼门禁卡式钥匙，另外两把是普通钥匙，钥匙扣是一个熊猫挂件，在操场跑步时可能掉落，急需找回！',
        'contact_phone': '13812345678',
        'status': 'matched',
        'is_approved': True,
    },
    {
        'user': created_users['lihua'],
        'type': 'lost',
        'title': '丢失白色AirPods Pro耳机',
        'category': 'electronics',
        'location': '图书馆二楼',
        'happened_at': now - timedelta(days=1, hours=3),
        'description': '昨天在图书馆二楼阅览室学习时，AirPods Pro耳机盒不见了，白色充电盒，第二代，盒子背面贴了一个小星星贴纸，里面有耳机，价值较高，请好心人联系！',
        'contact_phone': '13987654321',
        'status': 'active',
        'is_approved': True,
    },
    {
        'user': created_users['chenming'],
        'type': 'lost',
        'title': '丢失《机械设计》课本及笔记本',
        'category': 'books',
        'location': '机械工程学院实验楼',
        'happened_at': now - timedelta(days=5),
        'description': '丢失一本《机械设计》教材（第五版）和一本A4黑色笔记本，教材封面有我自己画的小图，笔记本内有整学期的实验记录，对我很重要，请联系！',
        'contact_phone': '18812345678',
        'status': 'active',
        'is_approved': True,
    },
    {
        'user': created_users['wangfang'],
        'type': 'lost',
        'title': '寻找丢失的身份证',
        'category': 'id_card',
        'location': '行政楼或图书馆',
        'happened_at': now - timedelta(days=3),
        'description': '本人王芳，经管学院，在行政楼办理手续时可能遗失了身份证，身份证照片是长发，非常重要，如有人捡到请联系，感激不尽！',
        'contact_phone': '15612345678',
        'status': 'active',
        'is_approved': True,
    },
]

created_items = []
for item_data in items_data:
    item = Item.objects.create(**item_data)
    created_items.append(item)
    type_label = '失物招领' if item_data['type'] == 'found' else '寻物启事'
    print(f"  ✅ [{type_label}] {item_data['title']}")

print(f"\n  共创建 {len(created_items)} 条物品信息")

# ─────────────────────────────────────────────
# 3. 创建留言
# ─────────────────────────────────────────────
messages_data = [
    # 张伟捡到学生证 → 李华留言认领
    {'item': created_items[0], 'from_user': created_users['lihua'], 'to_user': created_users['zhangwei'],
     'content': '你好！我就是李华，外国语学院的，我的学生证丢了！请问方便联系一下吗？我的微信是 lihua_english，非常感谢你！'},
    {'item': created_items[0], 'from_user': created_users['zhangwei'], 'to_user': created_users['lihua'],
     'content': '好的，已加你微信，你来图书馆门口取一下吧，我今晚7点在那里。'},
    {'item': created_items[0], 'from_user': created_users['lihua'], 'to_user': created_users['zhangwei'],
     'content': '太感谢了！我准时到！'},

    # 王芳捡到华为手机 → 陈明留言认领
    {'item': created_items[1], 'from_user': created_users['chenming'], 'to_user': created_users['wangfang'],
     'content': '请问是黑色Mate60吗？深蓝色手机壳？那应该是我的！我今天下午在B203上课，下课后发现手机不见了，能联系一下吗？'},
    {'item': created_items[1], 'from_user': created_users['wangfang'], 'to_user': created_users['chenming'],
     'content': '对的，就是这个描述！你来学生活动中心找我，今天下午3点，记得带学生证核实一下身份哦。'},
    {'item': created_items[1], 'from_user': created_users['chenming'], 'to_user': created_users['wangfang'],
     'content': '太好了！谢谢你！我马上过去，3点见！'},

    # 陈明捡到钥匙 → 张伟留言认领
    {'item': created_items[2], 'from_user': created_users['zhangwei'], 'to_user': created_users['chenming'],
     'content': '你好，我的钥匙丢了！钥匙扣是熊猫挂件，应该是我的！请问现在方便吗？'},
    {'item': created_items[2], 'from_user': created_users['chenming'], 'to_user': created_users['zhangwei'],
     'content': '好的，我现在在宿舍，你来南区3号楼101找我，记得告诉我你的宿舍号验证一下。'},
    {'item': created_items[2], 'from_user': created_users['zhangwei'], 'to_user': created_users['chenming'],
     'content': '我是南区5号楼302，马上过来！'},

    # 刘老师捡到书 → 陈明留言
    {'item': created_items[3], 'from_user': created_users['chenming'], 'to_user': created_users['teacher_liu'],
     'content': '刘老师好！那本书应该是我的，扉页写了我的名字，我什么时候可以去办公室取？'},
    {'item': created_items[3], 'from_user': created_users['teacher_liu'], 'to_user': created_users['chenming'],
     'content': '陈明同学，明天上午10点我在数学学院308办公室，你来取吧，记得带学生证。'},
    {'item': created_items[3], 'from_user': created_users['chenming'], 'to_user': created_users['teacher_liu'],
     'content': '好的刘老师，明天10点准时到，谢谢您！'},

    # 张伟捡到钱包 → 王芳询问
    {'item': created_items[4], 'from_user': created_users['wangfang'], 'to_user': created_users['zhangwei'],
     'content': '你好，我今天在食堂丢了钱包，请问你捡到的是黑色长款的吗？'},
    {'item': created_items[4], 'from_user': created_users['zhangwei'], 'to_user': created_users['wangfang'],
     'content': '不好意思，我捡到的是棕色短款的，可能不是你的，你再找找看。'},
    {'item': created_items[4], 'from_user': created_users['wangfang'], 'to_user': created_users['zhangwei'],
     'content': '好的，谢谢你！那我再去食堂前台问问。'},

    # 李华捡到AirPods → 王芳询问
    {'item': created_items[5], 'from_user': created_users['wangfang'], 'to_user': created_users['lihua'],
     'content': '你好，请问那个AirPods盒子背面的贴纸是什么图案？'},
    {'item': created_items[5], 'from_user': created_users['lihua'], 'to_user': created_users['wangfang'],
     'content': '是一个小星星贴纸，金色的，贴在充电口旁边。'},

    # 李华寻学生证 → 张伟回复
    {'item': created_items[8], 'from_user': created_users['zhangwei'], 'to_user': created_users['lihua'],
     'content': '李华你好，我在图书馆捡到一张学生证，蓝色卡套，应该是你的！我已经在失物招领那边发布了，你去看看。'},
    {'item': created_items[8], 'from_user': created_users['lihua'], 'to_user': created_users['zhangwei'],
     'content': '太好了！谢谢你！我马上去看！'},

    # 陈明寻手机 → 王芳回复
    {'item': created_items[9], 'from_user': created_users['wangfang'], 'to_user': created_users['chenming'],
     'content': '你好，我在B203捡到一部黑色华为手机，深蓝色壳，应该是你的！我在失物招领那边发布了，快来认领！'},
    {'item': created_items[9], 'from_user': created_users['chenming'], 'to_user': created_users['wangfang'],
     'content': '真的吗！！太感谢了，我马上去看！'},

    # 刘老师寻U盘
    {'item': created_items[10], 'from_user': created_users['zhangwei'], 'to_user': created_users['teacher_liu'],
     'content': '刘老师，我下午在305教室上课，没有看到U盘，您去教务处问问有没有人上交。'},
    {'item': created_items[10], 'from_user': created_users['teacher_liu'], 'to_user': created_users['zhangwei'],
     'content': '谢谢同学，我去问问，如果你们有看到请一定联系我！'},

    # 李华寻AirPods
    {'item': created_items[13], 'from_user': created_users['wangfang'], 'to_user': created_users['lihua'],
     'content': '我昨天在图书馆二楼好像看到桌子上有个白色耳机盒，但我没注意是不是AirPods，你去图书馆前台问问有没有人上交。'},
    {'item': created_items[13], 'from_user': created_users['lihua'], 'to_user': created_users['wangfang'],
     'content': '好的，我去问问，谢谢你！'},
]

for msg_data in messages_data:
    Message.objects.create(**msg_data)

print(f"  ✅ 创建留言 {len(messages_data)} 条")

# ─────────────────────────────────────────────
# 4. 创建匹配记录
# ─────────────────────────────────────────────
matches_data = [
    {
        'found_item': created_items[0],   # 捡到学生证
        'lost_item': created_items[8],    # 李华寻学生证
        'score': 98,
        'reason': '物品类型完全一致（学生证），失主姓名与捡到物品上的姓名完全吻合（李华），丢失时间与拾取时间相差不足2小时，地点均在图书馆区域，外观描述（蓝色卡套）完全一致，高度匹配。',
        'status': 'confirmed',
    },
    {
        'found_item': created_items[1],   # 捡到华为手机
        'lost_item': created_items[9],    # 陈明寻手机
        'score': 95,
        'reason': '物品类型一致（华为手机），颜色描述吻合（黑色），手机壳颜色一致（深蓝色磨砂），锁屏壁纸描述一致（猫），丢失地点与拾取地点均为B203教室，时间相差约1小时，高度匹配。',
        'status': 'confirmed',
    },
    {
        'found_item': created_items[2],   # 捡到钥匙
        'lost_item': created_items[12],   # 张伟寻钥匙
        'score': 92,
        'reason': '物品类型一致（钥匙串），数量一致（3把），钥匙扣描述完全吻合（熊猫挂件），丢失地点（操场）与拾取地点（操场东门）高度吻合，时间相差约3小时，匹配度极高。',
        'status': 'confirmed',
    },
    {
        'found_item': created_items[4],   # 捡到棕色钱包
        'lost_item': created_items[11],   # 王芳寻黑色钱包
        'score': 45,
        'reason': '物品类型一致（钱包），地点相近（均在食堂），时间相近，但颜色不符（棕色 vs 黑色），款式不符（短款 vs 长款），匹配度较低，建议核实。',
        'status': 'rejected',
    },
    {
        'found_item': created_items[5],   # 捡到AirPods
        'lost_item': created_items[13],   # 李华寻AirPods
        'score': 96,
        'reason': '物品类型完全一致（AirPods Pro耳机），颜色一致（白色），地点完全一致（图书馆二楼阅览室），时间相差约3小时，外观特征吻合（贴纸），高度匹配。',
        'status': 'pending',
    },
    {
        'found_item': created_items[3],   # 捡到高数书
        'lost_item': created_items[14],   # 陈明寻机械设计书
        'score': 30,
        'reason': '物品类型一致（书籍），但书名不同（高等数学 vs 机械设计），扉页姓名相同（陈明），地点不同（三教 vs 机械楼），综合判断为同一人遗失的不同书籍，匹配度低。',
        'status': 'rejected',
    },
]

for match_data in matches_data:
    Match.objects.create(**match_data)

print(f"  ✅ 创建匹配记录 {len(matches_data)} 条")

# ─────────────────────────────────────────────
# 5. 汇总输出
# ─────────────────────────────────────────────
from django.contrib.auth import get_user_model
User = get_user_model()

print("\n" + "="*65)
print("✅ 测试数据初始化完成！")
print("="*65)
print(f"  用户数：{User.objects.count()} 个（含管理员）")
print(f"  物品数：{Item.objects.count()} 条（失物招领 + 寻物启事）")
print(f"  留言数：{Message.objects.count()} 条")
print(f"  匹配数：{Match.objects.count()} 条")
print("\n📋 测试账号列表：")
print(f"  {'用户名':<15} {'密码':<15} {'身份':<8} {'院系'}")
print(f"  {'-'*65}")
print(f"  {'admin':<15} {'admin123456':<15} {'管理员':<8} 超级管理员")
for ud in users_data:
    utype = '教职工' if ud['user_type'] == 'teacher' else '学生'
    print(f"  {ud['username']:<15} {'test123456':<15} {utype:<8} {ud['department']}")
