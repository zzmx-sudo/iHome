# coding:utf-8


from . import api
from ihome.utils.commons import login_required
from ihome.models import Order
from flask import current_app, jsonify, g, request
from ihome.utils.response_code import RET
from alipay import AliPay
import os
from ihome import constants, db

@api.route("/orders/<int:order_id>/payment", methods=["POST"])
@login_required
def order_pay(order_id):
    """发起支付宝支付"""
    user_id = g.user_id

    # 判断订单状态
    try:
        order = Order.query.filter(Order.id == order_id, Order.user_id == user_id, Order.status == 'WAIT_PAYMENT').first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='数据库异常')
    if order is None:
        return jsonify(errno=RET.NODATA, errmsg='订单数据有误')

    # 创建支付宝SDK的工具对象
    alipay_client = AliPay(
        appid="2016102100732598",
        app_notify_url=None,  # 默认回调url
        app_private_key_path=os.path.join(os.path.dirname(__file__),"keys/app_private_key.pem"),  # 应用公钥
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥
        alipay_public_key_path=os.path.join(os.path.dirname(__file__),"keys/alipay_public_key.pem"),  # 支付宝公钥
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=True  # 默认False
    )

    order_string = alipay_client.api_alipay_trade_wap_pay(
        out_trade_no=order.id,  # 订单编号
        total_amount=str(order.amount/100.0),
        subject='爱家租房:%s' % order.id,  # 订单标题
        return_url="http://127.0.0.1:5000/payComplete.html",  # 返回的链接地址
        notify_url=None,
    )

    pay_url = constants.ALIPAY_URL_PREFIX + order_string
    return jsonify(errno=RET.OK, errmsg='OK', data={"pay_url":pay_url})

@api.route("/order/payment",methods=["PUT"])
def save_order_payment_result():
    """保存订单支付结果"""
    alipay_dict = request.form.to_dict()

    # 对支付宝的数据进行分离  提取出支付宝的签名参数sign 和剩下的其他数据
    alipay_sign = alipay_dict.pop("sign")

    # 创建支付宝SDK的工具对象
    alipay_client = AliPay(
        appid="2016102100732598",
        app_notify_url=None,  # 默认回调url
        app_private_key_path=os.path.join(os.path.dirname(__file__), "keys/app_private_key.pem"),  # 应用公钥
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥
        alipay_public_key_path=os.path.join(os.path.dirname(__file__), "keys/alipay_public_key.pem"),  # 支付宝公钥
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=True  # 默认False
    )

    # 借助工具验证参数的合法性
    # 如果确定参数是支付宝的，返回True，否则返回false
    result = alipay_client.verify(alipay_dict, alipay_sign)
    if result:
        # 修改数据库的订单状态信息
        order_id = alipay_dict.get("out_trade_no")
        trade_no = alipay_dict.get("trade_no")  # 支付宝的交易号

        try:
            Order.query.filter_by(id=order_id).update({"status":"WAIT_COMMENT", "trade_no":trade_no})
            db.session.commit()
        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()

    return jsonify(errno=RET.OK, errmsg='OK')
