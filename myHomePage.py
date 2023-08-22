import streamlit as st
import pandas as pd
import requests
import base64
from datetime import datetime
import tensorflow as tf
from tensorflow import keras


def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

def main():
    # 세션 상태 변수를 초기화합니다.
    if 'page' not in st.session_state:
        st.session_state['page'] = 'login_page'

    # 현재 페이지를 보여줍니다.
    if st.session_state['page'] == 'login_page':
        login_page()
    elif st.session_state['page'] == 'main_page':
        main_page()
    elif st.session_state['page'] == 'sign_up_page':
        sign_up_page()
    elif st.session_state['page'] == 'modify_page':
        modify_page()
    elif st.session_state['page'] == 'test_image_page':
        test_image_page()

# 로그인 페이지
def login_page():
    #set_background('c:/streamlit_projects/images/city1.jpg')
    st.title("")
    st.title("2023KEB_구름빵 :sunglasses:")
    st.caption("Streamlit WebPage - Welcome !!! :smile:")
    st.title("")
    st.title("")
    st.title("")
    st.subheader("Sign In")

    # 사용자 입력 필드
    userId = st.text_input("아이디", key='email', max_chars=32)
    userPassword = st.text_input("비밀번호", type='password', key='password', max_chars=16)

    # 2개의 컬럼 생성
    col1, col2 = st.columns(2)
    
    # 로그인 버튼 클릭 시 동작
    if col1.button(":green[로그인]"):
        if len(userId) == 0 or len(userPassword) == 0:
            st.error("아이디 또는 비밀번호를 입력하세요.", icon="⚠️")
        else:            
            data = {"user_id": userId, "user_password": userPassword}
            response = requests.post("http://localhost:5000/login", json=data)
            result = response.json()

            if result["status"] == "success":
                st.session_state["user_key"] = result["user_key"]
                st.session_state["user_id"] = result["user_id"]
                st.session_state["user_password"] = result["user_password"]
                st.session_state["user_name"] = result["user_name"]
                st.session_state["user_birth"] = result["user_birth"]
                st.session_state["user_tel"] = result["user_tel"]
                st.session_state["user_use_yn"] = result["user_use_yn"]
                st.session_state["user_reg_dt"] = result["user_reg_dt"]
                st.session_state["user_mod_dt"] = result["user_mod_dt"]
                st.session_state['page'] = 'main_page'            
                st.experimental_rerun()
            else:
                st.error(result["message"], icon="⚠️")
    elif col2.button(":blue[회원가입]"):
        st.session_state['page'] = 'sign_up_page'
        st.experimental_rerun()

# 회원가입 페이지
def sign_up_page():
    #set_background('c:/streamlit_projects/images/natural2.jpg')
    st.header("")
    st.title("2023KEB_구름빵 :sunglasses:")
    st.caption("Streamlit WebPage - Welcome !!! :smile:")
    st.header("")
    st.header("")
    st.subheader("Sign Up")

    # 사용자 입력 필드
    col1, col2 = st.columns(2)
    input_id = col1.text_input("아이디", max_chars=32)
    duplicateChk = st.button(":blue[중복 확인]")
    if duplicateChk:
        if len(input_id) == 0:
            col2.error("아이디를 입력하세요.", icon="⚠️")
        else:
            data = {"user_id": input_id}
            response = requests.post("http://localhost:5000/duplicateCheck", json=data)
            
            result = response.json()
            if result["status"] == "success":
                col2.success(result["message"], icon="✅")
            else:
                col2.error(result["message"], icon="⚠️")

    col1, col2 = st.columns(2)
    with col1:
        input_pw = st.text_input("비밀번호", type='password', key='password', max_chars=16)
    with col2:
        input_pw2 = st.text_input("비밀번호 확인", type='password', key='passwordConfirm', max_chars=16)

    col1, col2 = st.columns(2)
    with col2:
        passwdChk = st.button(":blue[비밀번호 확인]")

    if passwdChk:
            if len(input_pw) > 0 and input_pw == input_pw2:
                with col1:
                    st.success("비밀번호를 일치합니다.", icon="✅")
            elif len(input_pw) == 0:
                with col1:
                    st.error("비밀번호를 입력하세요.", icon="⚠️")
            else:
                with col1:
                    st.error("비밀번호가 일치하지 않습니다.", icon="⚠️")

    col1, col2 = st.columns(2)
    with col1:
        input_name = st.text_input("이름")
    with col2:
        input_birth = st.date_input("생년월일")
    
    col1, col2, col3 = st.columns(3)
    input_tel = col1.text_input("연락처 ('-' 제외하고 입력하세요.)", value="010", max_chars=3, key="tel1")
    input_tel += col2.text_input("", max_chars=4, key="tel2")
    input_tel += col3.text_input("", max_chars=4, key="tel3")

    col1, col2 = st.columns(2)  # 새로운 컬럼 생성
    if col1.button(":green[회원가입]"):  # 첫번째 컬럼에 버튼 배치
        data = {"user_id": input_id, 
                "user_password": input_pw2,
                "user_name": input_name,
                "user_birth": input_birth.isoformat(),
                "user_tel": input_tel,
                "user_use_yn": "Y"}

        response = requests.post("http://localhost:5000/insert", json=data)
        result = response.json()

        if result["status"] == "success":
            st.session_state['page'] = 'login_page'  # 페이지 전환을 여기서 설정
            st.experimental_rerun()
        elif result["status"] == "error":
            st.error(result["message"])

    elif col2.button(":red[돌아가기]"):  # 두번째 컬럼에 버튼 배치
        st.session_state['page'] = 'login_page'  # 페이지 전환을 여기서 설정
        st.experimental_rerun()

# 메인 페이지
def main_page():
    #set_background('c:/streamlit_projects/images/natural1.jpg')
    st.header("")
    st.title("2023KEB_구름빵 :sunglasses:")
    st.caption("Streamlit WebPage - Welcome !!! :smile:")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(':green[' + st.session_state["user_name"] + ']님 환영합니다. 🙋‍♂️')
    with col2:
        # 페이지 전환 버튼
        if st.button(":red[로그아웃]"):
            st.session_state["user_key"] = ""
            st.session_state["user_id"] = ""
            st.session_state["user_password"] = ""
            st.session_state["user_name"] = ""
            st.session_state["user_birth"] = ""
            st.session_state["user_tel"] = ""
            st.session_state["user_use_yn"] = ""
            st.session_state["user_reg_dt"] = ""
            st.session_state["user_mod_dt"] = ""
            st.session_state['page'] = 'login_page'  # 페이지 전환을 여기서 설정
            st.experimental_rerun()
    
    st.header("")
    st.header("")
    st.header("회원 목록")
    st.caption("가입된 회원 목록 입니다.")
    response = requests.post("http://localhost:5000/userList")
    result = response.json()
    df = pd.DataFrame(result)

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.markdown("회원 번호")
    col2.markdown("아이디")   
    col3.markdown("이름")
    col4.markdown("생년월일")
    col5.markdown("수정")

    col1, col2, col3, col4, col5 = st.columns(5)
    for j in range(len(df)):
        with col1:
            st.markdown(df.at[j, '회원 번호'])
        with col2:
            st.markdown(df.at[j, '아이디'])
        with col3:
            st.markdown(df.at[j, '이름'])
        with col4:
            st.markdown(df.at[j, '생년월일'])
        with col5:
            if st.button(':blue[수정]', key=df.at[j, '회원 번호']):
                st.session_state["modify_user_key"] = df.at[j, '회원 번호']
                st.session_state["modify_user_id"] = df.at[j, '아이디']
                st.session_state["modify_user_password"] = df.at[j, '비밀번호']
                st.session_state["modify_user_name"] = df.at[j, '이름']
                st.session_state["modify_user_birth"] = df.at[j, '생년월일']
                st.session_state["modify_user_tel"] = df.at[j, '연락처']
                st.session_state["modify_user_use_yn"] = df.at[j, '유효상태']
                st.session_state["modify_user_reg_dt"] = df.at[j, '등록일']
                st.session_state["modify_user_mod_dt"] = df.at[j, '수정일']
                st.session_state['page'] = 'modify_page'
                st.experimental_rerun()
    if st.button(":purple[양품 판별해보기]"):
        st.session_state['page'] = 'test_image_page'
        st.experimental_rerun()
    

# 회원정보 수정 페이지
def modify_page():
    #set_background('c:/streamlit_projects/images/natural3.jpg')
    st.header("")
    st.title("2023KEB_구름빵 :sunglasses:")
    st.caption("Streamlit WebPage - Welcome !!! :smile:")
    st.header("")
    st.header("")
    st.subheader("Member Info.")

    # 사용자 입력 필드
    col1, col2 = st.columns(2)
    input_id = col1.text_input("아이디", value=st.session_state["modify_user_id"])
    duplicateChk = st.button(":blue[중복 확인]")
    if duplicateChk:
        if len(input_id) == 0:
            col2.error("아이디를 입력하세요.", icon="⚠️")
        else:
            data = {"user_id": input_id}
            response = requests.post("http://localhost:5000/duplicateCheck", json=data)
            result = response.json()
            if result["status"] == "success":
                col2.success(result["message"], icon="✅")
            else:
                col2.error(result["message"], icon="⚠️")
    col1, col2 = st.columns(2)
    with col1:
        input_pw = st.text_input("새 비밀번호", type='password', key='password', max_chars=16)
    with col2:
        input_pw2 = st.text_input("새 비밀번호 확인", type='password', key='passwordConfirm', max_chars=16)

    col1, col2 = st.columns(2)
    with col2:
        passwdChk = st.button(":blue[비밀번호 확인]")

    if passwdChk:
            if len(input_pw) > 0 and input_pw == input_pw2:
                with col1:
                    st.success("비밀번호를 일치합니다.", icon="✅")
            elif len(input_pw) == 0:
                with col1:
                    st.error("비밀번호를 입력하세요.", icon="⚠️")
            else:
                with col1:
                    st.error("비밀번호가 일치하지 않습니다.", icon="⚠️")

    col1, col2 = st.columns(2)
    with col1:
        input_name = st.text_input("이름", value=st.session_state["modify_user_name"])
    with col2:
        input_birth = st.date_input("생년월일", value=datetime.strptime(st.session_state["modify_user_birth"], "%Y-%m-%d").date())
    
    col1, col2, col3 = st.columns(3)
    tel_number = st.session_state["modify_user_tel"]
    tel_number1 = f"{tel_number[:3]}"
    tel_number2 = f"{tel_number[3:7]}"
    tel_number3 = f"{tel_number[7:]}"
    input_tel = col1.text_input("연락처 ('-' 제외하고 입력하세요.)", value=tel_number1, max_chars=3, key="tel1")
    input_tel += col2.text_input("", max_chars=4, value=tel_number2, key="tel2")
    input_tel += col3.text_input("", max_chars=4, value=tel_number3, key="tel3")

    col1, col2, col3 = st.columns(3)  # 새로운 컬럼 생성
    if col1.button(":green[수정]"):  # 첫번째 컬럼에 버튼 배치
        if len(input_pw) > 0 and input_pw == input_pw2:
            data = {"user_key": str(st.session_state["modify_user_key"]), 
                    "user_id": input_id, 
                    "user_password": input_pw2,
                    "user_name": input_name,
                    "user_birth": input_birth.isoformat(),
                    "user_tel": input_tel,
                    "user_use_yn": "Y"}

            response = requests.post("http://localhost:5000/update", json=data)
            result = response.json()            

            if result["status"] == "success":
                st.session_state['page'] = 'main_page'  # 페이지 전환을 여기서 설정
                st.experimental_rerun()
            elif result["status"] == "error":
                st.error(result["message"])
        else:
            st.error("새 비밀번호를 입력해 주세요.")
    elif col2.button(":red[회원 삭제]"):
        data = {"user_key": str(st.session_state["modify_user_key"])}

        response = requests.post("http://localhost:5000/delete", json=data)
        result = response.json()

        if result["status"] == "success":
                st.session_state['page'] = 'main_page'  # 페이지 전환을 여기서 설정
                st.experimental_rerun()
        elif result["status"] == "error":
            st.error(result["message"])

    elif col3.button(":blue[돌아가기]"):  # 두번째 컬럼에 버튼 배치
        st.session_state['page'] = 'main_page'  # 페이지 전환을 여기서 설정
        st.experimental_rerun()   

def test_image_page():

    st.title("이미지 분류 예제")
    
    model = keras.models.load_model("C:/streamlit_projects/New_quality_model_epoch50.h5")

    # 이미지 업로드
    uploaded_image = st.file_uploader("이미지를 업로드하세요.", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        # 이미지 표시
        st.image(uploaded_image, caption="업로드한 이미지", use_column_width=True)

        # 이미지 전처리 및 예측
        image = tf.keras.utils.load_img(uploaded_image, target_size=(256,256))
        image_array = tf.keras.utils.img_to_array(image)
        image_array = tf.expand_dims(image_array, 0)  # 배치 차원 추가

        # 모델에 이미지 전달하여 예측
        predictions = model.predict(image_array)
        score = float(predictions[0])
        
        # 예측 결과 표시
        st.write("예측 결과:")
        if score > 0.5:
            st.write("정상 이미지")
            #st.write(f"정상 이미지 (정확도: {100 * score:.2f}%)")
        else:
            st.write("불량 이미지") 
            #st.write(f"불량 이미지 (정확도: {100 * (1 - score):.2f}%)") 

if __name__ == "__main__":
    main()
