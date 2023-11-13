from django.utils import timezone

# tensorflow 관련
import tensorflow as tf
import numpy as np
import os
from keras.preprocessing import image
from PIL import Image


# is_harvested 를 결정하는 함수
def determine_is_harvested(harvested_at):
    """
    날짜가 제공되면 True, 그렇지 않으면 False를 반환한다.
    """
    return harvested_at is not None


# growth_level을 결정하는 함수
def calculate_growth_level(plant_type, planted_at):
    """
    planted_at으로부터 오늘까지의 날짜를 계산해서
    발아기(germination), 성장기(growth), 수확기(harvest) 단계를 반환한다.
    모든 경우가 아닐 경우, 비활성기(nothing)을 반환한다.
    """
    today = timezone.now().date()
    days_since_planted = (today - planted_at.date()).days
    
    if plant_type.germination_period_start <= days_since_planted <= plant_type.germination_period_end:
            return 'germination'
    elif plant_type.growth_period_start <= days_since_planted <= plant_type.growth_period_end:
        return 'growth'
    elif plant_type.harvest_period_start <= days_since_planted <= plant_type.harvest_period_end:
        return 'harvest'
    else:
        return 'nothing'
    
    
# 수정하고자 하는 정보가 빈칸인지 확인
def is_blank(data):
    return data.strip() == ''


# tensorflow 관련 code
def resnet_AI_to_check_disease(diagnose_photo_url):
    height,width=180,180

    class_names = [ 
        'Corn___Common_rust', 
        'Corn___Gray_leaf_spot', 
        'Corn___Northern_Leaf_Blight', 
        'Corn___healthy', 
        'Potato___Early_blight', 
        'Potato___Late_blight', 
        'Potato___healthy', 
        'Strawberry___Leaf_scorch', 
        'Strawberry___healthy', 
        'Tomato___Early_blight', 
        'Tomato___Late_blight',
        'Tomato___Target_Spot', 
        'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 
        'Tomato___healthy'
    ]
        
    # 로컬 이미지 경로 설정
    url = diagnose_photo_url

    os.system("curl " + url + " > test2.jpg")

    # 이미지 불러오기
    local_image_path = "./test2.jpg"

    # 이미지 불러오기
    img = image.load_img(local_image_path, target_size=(height, width))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # 배치 차원 추가
    
    PATH_TO_MODEL = 'plants/model.tflite'

    interpreter = tf.lite.Interpreter(model_path=PATH_TO_MODEL)
    interpreter.allocate_tensors()

    # Get input and output tensors.
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # Test the model on random input data.
    input_shape = input_details[0]['shape']
    input_data = np.array(np.random.random_sample(input_shape), dtype=np.float32)
    interpreter.set_tensor(input_details[0]['index'], input_data)

    interpreter.invoke()
    
    classify_lite = interpreter.get_signature_runner('serving_default')

    predictions_lite = classify_lite(resnet50_input = img_array)['dense_1']

    # 클래스 이름과 신뢰도 출력
    print(
        "This image most likely belongs to {} with a {:.2f} percent confidence."
        .format(class_names[np.argmax(predictions_lite)], 100 * np.max(predictions_lite))
    )
    
    predicted_class = class_names[np.argmax(predictions_lite)]
    predicted_status = ""
    disease_type_id = ""
    
    if predicted_class == 'Corn___Common_rust':
        predicted_status = 'Corn common rust'
        disease_type_id = '1'
    elif predicted_class == 'Corn___Gray_leaf_spot':
        predicted_status = 'Corn gray leaf spot'
        disease_type_id = '2'
    elif predicted_class == 'Corn___Northern_Leaf_Blight':
        predicted_status = 'Corn northern leaf blight'
        disease_type_id = '3'
    elif predicted_class == 'Corn___healthy':
        predicted_status = 'Corn healthy'
        disease_type_id = '4'
    elif predicted_class == 'Potato___Early_blight':
        predicted_status = 'Potato early blight'
        disease_type_id = '5'
    elif predicted_class == 'Potato___Late_blight':
        predicted_status = 'Potato late blight'
        disease_type_id = '6'
    elif predicted_class == 'Potato___healthy':
        predicted_status = 'Potato healthy'
        disease_type_id = '7'
    elif predicted_class == 'Strawberry___Leaf_scorch':
        predicted_status = 'Strawberry leaf scorch'
        disease_type_id = '8'
    elif predicted_class == 'Strawberry___healthy':
        predicted_status = 'Strawberry healthy'
        disease_type_id = '9'
    elif predicted_class == 'Tomato___Early_blight':
        predicted_status = 'Tomato early blight'
        disease_type_id = '10'
    elif predicted_class == 'Tomato___Late_blight':
        predicted_status = 'Tomato late blight'
        disease_type_id = '11'
    elif predicted_class == 'Tomato___Target_Spot':
        predicted_status = 'Tomato target spot'
        disease_type_id = '12'
    elif predicted_class == 'Tomato___Tomato_Yellow_Leaf_Curl_Virus':
        predicted_status = 'Tomato yellow leaf curl virus'
        disease_type_id = '13'
    elif predicted_class == 'Tomato___healthy':
        predicted_status = 'Tomato healthy'
        disease_type_id = '14'
        
    return predicted_status, disease_type_id