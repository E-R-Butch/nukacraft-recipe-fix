#!/usr/bin/env python3
"""Patch translations: missed keys + attribute-unlock lists (round 2 hand work)."""

FIX = {
# ===== archive: 属性解锁列表 =====
"archive.nukacraft.special_agi_desc": "敏捷衡量你的整体灵巧度与反应速度。身手敏捷的幸存者解锁：\n\n[>1] 行动男孩/女孩：你的饥饿/疲劳消耗慢得多。\n[10] 闪避：5%%几率完全抵消来袭伤害。\n[25] 步履轻盈：坠落伤害减半。\n[50] 马拉松选手：疾跑不再消耗饥饿！\n[100] 忍者：闪避几率提升至15%%。",
"archive.nukacraft.special_cha_desc": "魅力是你迷住并说服他人的能力。能说会道的幸存者解锁：\n\n[10] 银舌：10%%几率让废土商人直接免费送你物品！\n[25] 感召力：你的驯服同伴在你附近时被动回复生命值。\n[50] 交易大师：从商人处购买的物品有15%%几率凭空翻倍进入你的背包！\n[100] 废土低语者：尝试安抚并驯服敌对生物！蹲下并空手互动来尝试。",
"archive.nukacraft.special_end_desc": "耐力衡量你的整体体能与对废土恐怖的抵抗力。强健的幸存者解锁：\n\n[10] 快速再生：食物条满时缓慢回复生命。\n[25] 抗药体质：有害药水效果持续时间减半！\n[50] 铁皮：受到的所有伤害降低10%%。\n[100] 回光返照：拒绝死亡！每5分钟一次，致命伤害将只把你打到1点生命值。",
"archive.nukacraft.special_int_desc": "智力衡量你的整体心智敏锐度。天才们解锁：\n\n[>1] 快速学习：被动提升所有经验球数值。\n[25] 拾荒者：15%%几率让制作成品翻倍。\n[50] 书呆之怒！：生命值低于25%%时造成20%%额外伤害。\n[100] 物品磁铁：通过快捷键切换此辅助能力，隔空吸取附近的经验球！",
"archive.nukacraft.special_luc_desc": "运气衡量你的整体好运！幸运的幸存者解锁：\n\n[>1] 搜刮者：被动为你的所有击杀增加拾取加成。\n[10] 寻财者：10%%几率让生物掉落额外战利品！\n[25] 钓鱼天堂：钓上来的所有物品都会翻倍！\n[100] 头奖：3%%几率让生物死亡时爆炸成漫天翻倍战利品雨！",
"archive.nukacraft.special_per_desc": "感知衡量你的环境觉察力和「第六感」。目光犀利的幸存者解锁：\n\n[10] 感知聚焦：按下快捷键（查看控制设置）切换高亮显示附近所有敌对威胁！\n[25] 狙击手：对生命值低于一半的目标，弹丸伤害提升25%%。\n[50] 闪避：抵挡15%%的来袭远程伤害。",
"archive.nukacraft.special_str_desc": "力量衡量你的原始体能！除了砸得更快更狠，真正的肌肉猛男还解锁以下辅助能力：\n\n[10] 重击：你的攻击造成150%%击退！\n[25] 强击手：10%%几率造成500%%击退！挖掘时还有15%%几率让方块掉落物翻倍。\n[50] 震荡打击：非弹丸攻击对目标施加虚弱。\n[100] 处刑人：对损失生命值的目标造成双倍伤害。",

# ===== 漏翻方块/物品 =====
"block.nukacraft.gray_tile": "灰色瓷砖",
"block.nukacraft.raw_aluminium_block": "未处理铝块",
"block.nukacraft.raw_black_titan_block": "未处理黑钛块",
"block.nukacraft.raw_lead_block": "未处理铅块",
"block.nukacraft.raw_silver_block": "未处理银块",
"block.nukacraft.raw_uranium_block": "未处理铀块",
"item.nukacraft.coral_leaf": "珊瑚树叶",
"item.nukacraft.dogwood": "山茱萸",
"item.nukacraft.lamp": "电子矿灯",
"item.nukacraft.raw_black_titanium": "未处理黑钛",

# ===== 状态效果（带官方色码）=====
"effect.nukacraft.frost_resist": "§b抗冻",
"effect.nukacraft.quant_shield": "§6量子护盾",
"effect.nukacraft.speed": "§9速度 ",
"effect.nukacraft.health": "§9生命值 ",
"effect.nukacraft.glowing": "§2发光！",
"effect.nukacraft.deadly_freezing": "§b致命冻伤",
"effect.nukacraft.rad_shield": "§9辐射抗性 ",
"info.nukacraft.power": "§3电力：$s",
"item.nukacraft.fatman": "§c胖子核弹发射器",

# ===== 剩余皮肤 =====
"skin.black": "§b§o黑色颜料",
"skin.blue": "§b§o蓝色颜料",
"skin.brown": "§b§o棕色颜料",
"skin.clean": "§7§o清洁",
"skin.default": "§7§o默认",
"skin.gray": "§b§o灰色颜料",
"skin.light_blue": "§b§o淡蓝色颜料",
"skin.orange": "§b§o橙色颜料",
"skin.pink": "§b§o粉红色颜料",
"skin.red": "§b§o红色颜料",

# ===== 全息磁带配色提示 =====
"tooltip.nukacraft.holotape#cyan": "§7配色方案：§b青色",
"tooltip.nukacraft.holotape#gold": "§7配色方案：§e金色",
"tooltip.nukacraft.holotape#green": "§7配色方案：§2绿色",
"tooltip.nukacraft.holotape#orange": "§7配色方案：§6橙色",
"tooltip.nukacraft.holotape#red": "§7配色方案：§c红色",
"tooltip.nukacraft.holotape#violet": "§7配色方案：§d紫色",
"tooltip.nukacraft.holotape#white": "§7配色方案：§f白色",
}
