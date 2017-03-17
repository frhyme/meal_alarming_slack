import pandas as pd
import datetime as dt
import requests

def read_table_as_dataframe_from_url(url):
    r = requests.get(url)
    r.encoding = "utf-8"
    start_str="<!--  목록 시작 -->"
    end_str="</td></tr></table>"
    text = r.text[r.text.find(start_str)+len(start_str)+1:r.text.find(end_str)+len(end_str)]
    # 복잡해서 보니까, 대충 위의 두 스트링으로 골라내면 대충 될것 같았음
    #print(text)
    # 생각해보니, 왠지 html의 테이블을 쉽게 긁어오는 누가 해놓은 코드가 이미 있지 않을까?

    raw_data = pd.read_html(text)
    raw_data = raw_data[1]
    return raw_data


# In[274]:

def read_student_meal_from_df(raw_data):
    raw_data = raw_data[raw_data.index %3==0] # drop useless row
    raw_data = raw_data[1:] # drop useless row

    raw_data= raw_data.drop(5, axis=1) # drop useless column
    raw_data = raw_data.drop(6, axis=1) # drop useless column

    # index => date, column => 조식 중식 석식
    # 각 셀의 영어 날려버릴 것
    date_str_lst = [ x[:len(x)-4] for x in raw_data[0]]
    date_lst = [dt.datetime.strptime(str(dt.date.today().year)+date_str, "%Y%m-%d") for date_str in date_str_lst]
    date_lst = [x.date() for x in date_lst]
    raw_data.index = date_lst
    raw_data = raw_data.drop(0, axis=1)

    raw_data.columns = ["breakfast", "breakfast_special", "lunch", "dinner"]

    for i in raw_data.index:
        for j in raw_data.columns:
            for k in range(0, len(raw_data[j][i])):
                if ord(raw_data[j][i][k]) in range(1, ord("~")):
                    #non-korean delete
                    raw_data[j][i]=raw_data[j][i].replace(raw_data[j][i][k], " ")
            while "  " in raw_data[j][i]:
                # delete whitespace
                raw_data[j][i]=raw_data[j][i].replace("  ", " ").strip()
            raw_data[j][i]=raw_data[j][i].replace(" ", ", ")
    return raw_data

def read_faculty_meal_from_df(raw_data):
    raw_data = raw_data[raw_data.index%3==2]
    date_str_lst = [ x[:len(x)-4] for x in raw_data[0]]
    date_lst = [dt.datetime.strptime(str(dt.date.today().year)+date_str, "%Y%m-%d") for date_str in date_str_lst]
    date_lst = [x.date() for x in date_lst]
    raw_data.index = date_lst
    raw_data = raw_data.drop(0, axis=1)
    raw_data.columns = ["lunch"]

    for i in raw_data.index:
        for j in raw_data.columns:
            for k in range(0, len(raw_data[j][i])):
                if ord(raw_data[j][i][k]) in range(1, ord("~")):
                    #non-korean delete
                    raw_data[j][i]=raw_data[j][i].replace(raw_data[j][i][k], " ")
            while "  " in raw_data[j][i]:
                # delete whitespace
                raw_data[j][i]=raw_data[j][i].replace("  ", " ").strip()
            raw_data[j][i]=raw_data[j][i].replace(" ", ", ")
    return raw_data

student_meal_url="http://fd.postech.ac.kr/bbs/board_menu.php?bo_table=weekly"
faculty_meal_url="http://fd.postech.ac.kr/bbs/board_menu.php?bo_table=weekly&sca=%EA%B5%90%EC%A7%81%EC%9B%90"

student_meal_df = read_student_meal_from_df( read_table_as_dataframe_from_url(student_meal_url) )
faculty_meal_df = read_faculty_meal_from_df( read_table_as_dataframe_from_url(faculty_meal_url) )

if dt.date.today() in student_meal_df.index:
    print("breakfast", student_meal_df["breakfast"][dt.date.today()])
else:
    print("not yet uploaded")

if dt.date.today() in faculty_meal_df.index:
    print("breakfast", faculty_meal_df["lunch"][dt.date.today()])
else:
    print("not yet uploaded")
