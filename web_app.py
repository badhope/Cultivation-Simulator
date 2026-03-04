#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修仙模拟器 - Web版本
使用Flask + HTML + CSS + JavaScript实现
"""

from flask import Flask, render_template, request, jsonify, session, redirect
import json
import os
import random
from core.game_engine import GameEngine
from core.player import Player
from core.world import World

app = Flask(__name__)
app.secret_key = 'cultivation_simulator_secret_key'

# 游戏引擎实例
game_engine = None
player = None
world = None

# 确保存档目录存在
SAVE_DIR = 'saves'
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

@app.route('/')
def index():
    """首页"""
    return render_template('index.html')

@app.route('/start', methods=['GET', 'POST'])
def start_game():
    """开始游戏"""
    if request.method == 'POST':
        player_name = request.form['player_name']
        stats = {
            '体质': int(request.form['体质']),
            '灵根': int(request.form['灵根']),
            '悟性': int(request.form['悟性']),
            '机缘': int(request.form['机缘'])
        }
        
        # 初始化游戏
        global game_engine, player, world
        game_engine = GameEngine()
        player = Player(player_name)
        player.stats.update(stats)
        world = World()
        
        # 保存到会话
        session['player_name'] = player_name
        session['stats'] = stats
        
        return jsonify({'success': True, 'message': '游戏开始成功！'})
    return render_template('character_creation.html')

@app.route('/game')
def game_interface():
    """游戏界面"""
    if 'player_name' not in session:
        return redirect('/')
    return render_template('game.html')

@app.route('/api/player_info')
def get_player_info():
    """获取玩家信息"""
    if player:
        return jsonify({
            'name': player.name,
            'realm': player.realm,
            'cultivation': player.cultivation,
            'lifetime': player.lifetime,
            'stats': player.stats,
            'resources': player.resources
        })
    return jsonify({'error': '玩家未初始化'})

@app.route('/api/world_info')
def get_world_info():
    """获取世界信息"""
    if world:
        seasons = ["春季", "夏季", "秋季", "冬季"]
        weathers = ["晴朗", "多云", "下雨", "下雪"]
        
        season = seasons[world.world_time % 4]
        weather = random.choice(weathers)
        spirit = random.randint(30, 80)
        
        return jsonify({
            'season': season,
            'weather': weather,
            'spirit': spirit
        })
    return jsonify({'error': '世界未初始化'})

@app.route('/api/cultivate')
def cultivate():
    """修炼"""
    if player:
        player.cultivate()
        return jsonify({
            'success': True,
            'cultivation': player.cultivation,
            'message': '修炼成功！' if player.cultivation < 100 else '修为已满！可以尝试突破了！'
        })
    return jsonify({'error': '玩家未初始化'})

@app.route('/api/explore/<location>')
def explore(location):
    """探索地点"""
    if player:
        # 模拟探索结果
        results = [
            f"在{location}发现了灵石矿脉！获得灵石 x50",
            f"在{location}遇到了一位前辈，获得指点，悟性 +1",
            f"在{location}发现一株千年灵草！获得灵药 x1",
            f"在{location}遭遇妖兽袭击！经过激战成功逃脱",
            f"在{location}一无所获，但增长了见识"
        ]
        
        result = random.choice(results)
        
        # 更新资源和属性
        if "灵石" in result:
            player.add_resource("灵石", 50)
        elif "灵草" in result:
            player.add_resource("灵药", 1)
        elif "悟性" in result:
            player.stats["悟性"] += 1
        
        return jsonify({
            'success': True,
            'result': result,
            'resources': player.resources,
            'stats': player.stats
        })
    return jsonify({'error': '玩家未初始化'})

@app.route('/api/alchemy')
def alchemy():
    """炼丹"""
    if player:
        if player.resources.get('灵药', 0) > 0:
            # 模拟炼丹结果
            success = random.random() > 0.3  # 70%成功率
            player.resources['灵药'] -= 1
            
            if success:
                player.add_resource('丹药', 1)
                result = "炼丹成功！获得丹药 x1"
            else:
                result = "炼丹失败，材料浪费了"
            
            return jsonify({
                'success': True,
                'result': result,
                'resources': player.resources
            })
        else:
            return jsonify({'error': '没有足够的灵药！'})
    return jsonify({'error': '玩家未初始化'})

@app.route('/api/save')
def save_game():
    """保存游戏"""
    if player and game_engine:
        try:
            save_data = {
                'player': player.to_dict(),
                'world': world.to_dict() if world else None,
                'game_time': game_engine.game_time if game_engine else 0
            }
            save_file = os.path.join(SAVE_DIR, f"{player.name}.json")
            with open(save_file, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
            return jsonify({'success': True, 'message': '游戏已保存！'})
        except Exception as e:
            return jsonify({'error': f'保存失败：{e}'})
    return jsonify({'error': '游戏未初始化'})

@app.route('/api/load/<player_name>')
def load_game(player_name):
    """加载游戏"""
    global game_engine, player, world
    try:
        save_file = os.path.join(SAVE_DIR, f"{player_name}.json")
        with open(save_file, 'r', encoding='utf-8') as f:
            save_data = json.load(f)
        
        player = Player.from_dict(save_data['player'])
        if save_data['world']:
            world = World.from_dict(save_data['world'])
        game_engine = GameEngine()
        if hasattr(game_engine, 'game_time'):
            game_engine.game_time = save_data.get('game_time', 0)
        
        session['player_name'] = player_name
        session['stats'] = player.stats
        
        return jsonify({'success': True, 'message': '游戏加载成功！'})
    except Exception as e:
        return jsonify({'error': f'加载失败：{e}'})

@app.route('/api/saves')
def list_saves():
    """列出所有存档"""
    saves = []
    for file in os.listdir(SAVE_DIR):
        if file.endswith('.json'):
            try:
                save_file = os.path.join(SAVE_DIR, file)
                with open(save_file, 'r', encoding='utf-8') as f:
                    save_data = json.load(f)
                saves.append({
                    'name': file.replace('.json', ''),
                    'player_name': save_data.get('player', {}).get('name', ''),
                    'realm': save_data.get('player', {}).get('realm', ''),
                    'lifetime': save_data.get('player', {}).get('lifetime', 0)
                })
            except:
                pass
    return jsonify(saves)

@app.route('/api/quit')
def quit_game():
    """退出游戏"""
    global game_engine, player, world
    game_engine = None
    player = None
    world = None
    session.clear()
    return jsonify({'success': True, 'message': '游戏已退出！'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
