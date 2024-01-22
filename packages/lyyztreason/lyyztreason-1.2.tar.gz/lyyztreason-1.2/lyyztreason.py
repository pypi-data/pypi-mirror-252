import sys, os
import requests, json
from datetime import datetime
import pymysql
from sqlalchemy import create_engine, text
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy import select, func
import requests
import time
import pandas as pd


# pyinstaller -D -n ztreason_jiucai --distpath  "D:\Soft\_lyysoft" D:\UserData\Documents\PythonCode\archive\ztreason_jiucai.py --noconfirm


con = pymysql.connect(host="rm-7xvcw05tn97onu88s7o.mysql.rds.aliyuncs.com", user="cy", passwd="Yc124164", port=3306, db="fpdb", charset="utf8")
cur = con.cursor()


def today_reason(debug=False):
    url = "https://flash-api.xuangubao.cn/api/surge_stock/reason/today"
    headers = {
        "Host": "flash-api.xuangubao.cn",
        "Connection": "keep-alive",
        "Access-Control-Request-Method": "GET",
        "Access-Control-Request-Headers": "x-ivanka-token",
        "Origin": "<https://xuangubao.cn>",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Dest": "empty",
        "Referer": "<https://xuangubao.cn/zhutiku>",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Accept": "*/*",
    }

    response = requests.get(url, headers=headers)
    if debug:
        print("url=", url, ",headers=", headers)
    if debug:
        print("today_reason_result::", response.text)
    return response.text


def html2mysql_today(json_str, debug=False):
    total_effect = 0
    # if debug: print(json_str)
    data = json.loads(json_str)
    surge_reason = data["data"]["surge_reason"]
    for item in range(len(surge_reason)):
        print(" for item in range(len( surge_reason)) item=", item)
        stk_code_num = surge_reason[list(surge_reason)[item]]["symbol"].replace(".", "").replace("S", "").replace("Z", "").replace("H", "")
        stk_code_num = int(stk_code_num)

        stock_reason = surge_reason[list(surge_reason)[item]]["stock_reason"]
        date_int = datetime.now().strftime("%Y%m%d")
        related_plates = surge_reason[list(surge_reason)[item]]["related_plates"]
        for plate in related_plates:
            if "plate_id" in plate:
                plate_id = plate["plate_id"]
            if "plate_name" in plate:
                plate_name = plate["plate_name"]
            if "plate_reason" in plate:
                plate_reason = plate["plate_reason"]
            else:
                plate_reason = ""

        print(f" 取出的数据为：{date_int}：'{stk_code_num}'：{plate_name}: {stock_reason}")

        sql = f"SELECT name FROM stock_all_codes WHERE code='{stk_code_num}'"
        print("查询code,seach=", sql)
        cur.execute(sql)
        result = cur.fetchone()
        if result:
            stk_name = result[0]
            print("数据库中查到的name=", stk_name)
        else:
            stk_name = ""
            print("数据库中查不到名字，请检查是代码错了，还是没更新。：stk_name=", stk_name)

        # 查询数据库表中是否已经存在相同数据
        sql = f"SELECT count(*) FROM stock_zt_reason WHERE code='{stk_code_num}'"
        print("seach=", sql)
        cur.execute(sql)
        result = cur.fetchone()
        print(result, "dfsafdsafdsa")
        if result:
            print("有相同值，尝试删除")
            del_sql = f"delete from stock_zt_reason where code='{stk_code_num}'"
            cur.execute(del_sql)
            print(cur.rowcount, "record(s) removed.")
        else:
            print("无结果")

        # 无论是否相同数据，都执行插入操作
        sql_insert = f"insert into stock_zt_reason(date, code, name, plate_id,plate_name,plate_reason,reason) \
            values({date_int}, '{stk_code_num}', '{stk_name}','{plate_id}','{plate_name}','{plate_reason}', '{stock_reason}')"
        print("insert=", sql_insert)
        cur.execute(sql_insert)
        print(cur.rowcount, "record inserted.")
        total_effect = total_effect + cur.rowcount
        con.commit()
        # import time;time.sleep(3333)
    return total_effect


def 韭菜公社(date_str, debug=False):
    url = "https://app.jiuyangongshe.com/jystock-app/api/v1/action/field"
    headers = {"cookie": "Hm_lvt_58aa18061df7855800f2a1b32d6da7f4=1696917396; UM_distinctid=18b182899a927d-0fe36fe5c5cc2-26031e51-1fa400-18b182899aa115e; Hm_lpvt_58aa18061df7855800f2a1b32d6da7f4=1696922120", "origin": "https://www.jiuyangongshe.com", "Platform": "3", "Referer": "https://www.jiuyangongshe.com/", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36", "Token": "fd611dcef77bc69b8b83d2c9a17f52c2", "Sec-Ch-Ua": '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"', "Host": "app.jiuyangongshe.com", "Timestamp": f"{int(time.time()*1000)}"}
    data = {"date": date_str, "pc": 1}
    r = requests.post(url, headers=headers, json=data).json()

    r_data = r["data"]
    # print("rdata=", r_data)
    return r_data[1:]


def get_reason_from_list(r_list, code_my=None):
    print("lenoflsi=", len(r_list))
    print(r_list[1])
    r_list = r_list[1]["list"]

    print(r_list)
    print("--------------------------------------------")
    r = r["data"]

    code_lis, name_lis, price_lis, expound_lis, share_range_lis, time_lis = [], [], [], [], [], []

    for i in r[1:]:
        lis = i.get("list")
        for j in lis:
            code = j["code"]
            if code_my in code:
                # print(j)
                name = j["name"]
                price = float(j["article"]["action_info"]["price"]) / 100
                expound = j["article"]["action_info"]["expound"]
                shares_range = float(j["article"]["action_info"]["shares_range"]) / 100
                time_ = j["article"]["action_info"]["time"]
                code_lis.append(code)
                name_lis.append(name)
                price_lis.append(price)
                expound_lis.append(expound)
                share_range_lis.append(shares_range)
                time_lis.append(time_)
    df = pd.DataFrame({"代码": code_lis, "名称": name_lis, "价格": price_lis, "解析": expound_lis, "跌涨幅": share_range_lis, "时间": time_lis})
    # return j
    df.to_csv("200_yidong.csv", index=False, encoding="utf_8_sig")


def insert_dict_to_table(conn, data_dict):
    print(data_dict.keys(), "keys()")
    # dict_keys(['code', 'name', 'date', 'plate_name', 'reason']) keys()
    rowcount = 0
    try:
        # 构建插入语句
        keys = ", ".join(data_dict.keys())
        values = ", ".join([":" + key for key in data_dict.keys()])
        insert_statement = text(f"INSERT INTO stock_jiucai ({keys}) VALUES ({values})")

        columns = ", ".join(data_dict.keys())  # 获取要检查的列名
        query = f"SELECT COUNT(*) FROM stock_jiucai WHERE code={data_dict['code']} and date={data_dict['date']}"
        result = conn.execute(text(query))  # 使用execute方法执行查询
        rowcount = result.fetchone()[0]
        print("query", query)

        if rowcount > 0:
            print("Duplicate values detected. Skipping insertion.")
            return rowcount  # 如果存在重复值，则返回已插入的行数，以便稍后进行相应的处理
        else:
            # 插入操作
            result = conn.execute(insert_statement, data_dict)
            conn.commit()
            return result.rowcount

    except Exception as e:
        print(e)


def get_old_date(days):
    total_effect_rows = 0
    for dayn in range(days):
        d = cal.tc_before_today(days - 1 - dayn)
        d = str(d)
        print(d)
        date = d[:4] + "-" + d[4:6] + "-" + d[6:8]
        print("date=", date)

        reasons_list = 韭菜公社(date)

        for lst in reasons_list:
            data = lst["list"]
            for item in data:
                print("item=", item)
                new_dict = {}
                new_dict["code"] = item["code"].replace("sh", "").replace("sz", "").replace("bj", "")
                new_dict["name"] = item["name"]
                new_dict["date"] = item["article"]["create_time"][:10].replace("-", "")
                plate_reason_and_reson = item["article"]["action_info"]["expound"].split("\n", 1)
                if len(plate_reason_and_reson) == 2:
                    new_dict["plate_name"], new_dict["reason"] = plate_reason_and_reson
                else:
                    new_dict["plate_name"] = ""
                    new_dict["reason"] = plate_reason_and_reson[0]

                print(new_dict)
                total_effect_rows += insert_dict_to_table(conn, new_dict)
        time.sleep(5)
    print(f"Congratulations! Total added {total_effect_rows} row( including existing item)")


def get_last_date_in_db(engine):
    # 创建连接
    conn = engine.connect()
    metadata = MetaData()
    metadata.reflect(bind=engine)
    Stock_Jiucai = Table("stock_jiucai", metadata, autoload_with=engine)

    # 执行SQL查询语句
    result = conn.execute(func.max(Stock_Jiucai.c.date))

    # 获取查询结果
    last_date = result.scalar()
    # 关闭连接
    conn.close()
    return last_date


if __name__ == "__main__":
    import lyycalendar

    cal = lyycalendar.lyycalendar_class()
    db_string = "mysql+pymysql://cy:Yc124164@rm-7xvcw05tn97onu88s7o.mysql.rds.aliyuncs.com:3306/fpdb?charset=utf8"

    if not "engine" in locals():
        engine = create_engine(db_string)
        conn = engine.connect()
    #     reasons_list = 韭菜公社("2023-11-06")

    # 创建数据库引擎
    engine = create_engine(db_string)
    last_date = get_last_date_in_db(engine)
    today_int = lyycalendar.get_today_int()
    相差天数 = cal.计算相隔天数_byIndex(last_date, today_int)
    相差天数 = 相差天数 + 1 if 相差天数 == 0 else 相差天数
    get_old_date(相差天数)
    from lyylog import log

    log("ztreason_jiucai result=", 相差天数)
    # 连接数据库

    conn.close()
    # print(韭菜公社("300280"))


if __name__ == "__main__":
    # 使用已有的engine和conn
    engine = create_engine("mysql+pymysql://cy:Yc124164@rm-7xvcw05tn97onu88s7o.mysql.rds.aliyuncs.com:3306/fpdb?charset=utf8")
    conn = engine.connect()
    html_today = today_reason()
    print(html_today)
    effected = html2mysql_today(html_today)
