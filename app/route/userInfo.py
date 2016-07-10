#-*- coding: UTF-8 -*-

from flask import Blueprint
from flask import request,jsonify,json
import traceback
import sys
sys.path.append("..")
from models import User
from models import food as Food

#说明：客户端发送:page（可选）,token
#homeImgUrl数据库中没有，先返回空
#isconfirm同上
#foodImgUrl同上

userInfo_route = Blueprint('userInfo', __name__)

@userInfo_route.route('/userInfo', methods=['POST'])
def userInfo():
    perPageCount = 1
    try:
        token = request.json['token']
        user = User.query.filter_by(token =token).first()
        if user is None:
            state = "fail"
            reason="用户不存在"
            return jsonify({"state":state,
                             "reason":reason
                            })

        username = user.username
        #TODO
        homeImgUrl = ""
        isconfirm = ""

        #若有page,做分页；
        page = request.json.get("page")
        if page is None:
            foodId = 1
            foods = user.foods
        else:
            page = int(page)
            foodId = 1 + (page-1) * perPageCount
            foods = user.foods.paginate(page =page,per_page = perPageCount,error_out=False)
            foods = foods.items

        foodList = []
        for food in foods:
            if food.disable == 1:
                continue
            foodJson = {"foodid":foodId,
                                "foodname":food.name,
                                "monthSales":food.monthsales,
                                "price":food.price,
                                "description":food.description,
                                #TODO
                                "imgurl":""
                        }
            foodList.append(foodJson)
            foodId += 1

        #成功返回return
        state = "successful"
        reason = ""
        return jsonify({
            "state":state,
            "reason":reason,
            "username":username,
            "homeimgurl":homeImgUrl,
            "confirm":isconfirm,
            "foodlist":foodList
        })
    except Exception, e:
        state = "fail"
        reason = "服务器异常"
        return jsonify({
            "state":state,
            "reason":reason
        }

        )